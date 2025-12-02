# main.py – FastAPI Model Inference API
# Now with request ID middleware, structured logging, and /models endpoints.

from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import uuid
import logging

from registry import ModelRegistry


# ------------------------------------------------------------------------------
# Logging Setup (simple structured logging)
# ------------------------------------------------------------------------------
logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)

logger = logging.getLogger("python-api")


# ------------------------------------------------------------------------------
# Request Models
# ------------------------------------------------------------------------------
class PredictRequest(BaseModel):
    text: str
    version: Optional[str] = None


class ModelInfo(BaseModel):
    version: str
    metadata: Dict[str, Any]


class LatestModelInfo(BaseModel):
    version: str
    metadata: Dict[str, Any]


# ------------------------------------------------------------------------------
# FastAPI App + Registry
# ------------------------------------------------------------------------------
app = FastAPI(title="Text Classifier API", version="0.1.0")
registry = ModelRegistry()


# ------------------------------------------------------------------------------
# Helper: request ID generator
# ------------------------------------------------------------------------------
def generate_request_id():
    return f"py-{uuid.uuid4().hex[:12]}"


# ------------------------------------------------------------------------------
# Middleware: attach requestId to every request + log start/end
# ------------------------------------------------------------------------------
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    # Read incoming ID from Fastify or generate a new one
    incoming = request.headers.get("x-request-id")
    request_id = incoming if incoming else generate_request_id()

    start = time.time()

    # Log request start
    logger.info({
        "msg": "Incoming request",
        "path": request.url.path,
        "method": request.method,
        "requestId": request_id
    })

    # Process request
    response = await call_next(request)

    # Add header to response
    response.headers["x-request-id"] = request_id

    duration_ms = round((time.time() - start) * 1000, 2)

    # Log request completion
    logger.info({
        "msg": "Completed request",
        "path": request.url.path,
        "method": request.method,
        "durationMs": duration_ms,
        "requestId": request_id
    })

    return response


# ------------------------------------------------------------------------------
# Health Endpoint
# ------------------------------------------------------------------------------
@app.get("/health")
def health(request: Request):
    request_id = request.headers.get("x-request-id", "unknown")

    logger.info({
        "msg": "Handling /health",
        "requestId": request_id
    })

    return {
        "status": "ok",
        "detail": "python-api running",
        "requestId": request_id
    }


# ------------------------------------------------------------------------------
# Predict Endpoint
# ------------------------------------------------------------------------------
@app.post("/predict")
def predict(request_payload: PredictRequest, request: Request):
    request_id = request.headers.get("x-request-id", "unknown")

    logger.info({
        "msg": "Handling /predict",
        "requestId": request_id,
        "version": request_payload.version
    })

    # Load correct model version
    if request_payload.version:
        model, metadata = registry.get_model(request_payload.version)
        version = request_payload.version
    else:
        model, metadata = registry.get_latest_model()
        version = metadata.get("version", "unknown")

    # Perform prediction
    prediction = model.predict([request_payload.text])[0]

    logger.info({
        "msg": "Prediction complete",
        "requestId": request_id,
        "prediction": prediction,
        "modelVersion": version
    })

    return {
        "version": version,
        "prediction": prediction,
        "metadata": {
            "best_cv_accuracy": metadata.get("best_cv_accuracy"),
            "test_accuracy": metadata.get("test_accuracy"),
            "saved_at": metadata.get("saved_at")
        },
        "requestId": request_id
    }


# ------------------------------------------------------------------------------
# NEW: List All Models Endpoint
# ------------------------------------------------------------------------------
@app.get("/models", response_model=List[ModelInfo])
def list_models(request: Request):
    """
    List all discovered model versions under the registry, with their metadata.

    Uses:
      - registry.list_versions()
      - registry.get_metadata(version)
    """
    request_id = request.headers.get("x-request-id", "unknown")

    logger.info({
        "msg": "Handling /models",
        "requestId": request_id
    })

    versions = registry.list_versions()
    models: List[ModelInfo] = []

    for v in versions:
        try:
            metadata = registry.get_metadata(v)
        except Exception as ex:
            logger.error({
                "msg": "Failed to read metadata for version",
                "version": v,
                "requestId": request_id,
                "error": str(ex)
            })
            # Skip broken entries
            continue

        models.append(ModelInfo(version=v, metadata=metadata))

    logger.info({
        "msg": "Completed /models",
        "requestId": request_id,
        "count": len(models)
    })

    return models


# ------------------------------------------------------------------------------
# NEW: Latest Model Info Endpoint
# ------------------------------------------------------------------------------
@app.get("/models/latest", response_model=LatestModelInfo)
def get_latest_model_info(request: Request):
    """
    Return the latest version + metadata.
    Uses:
      - registry.get_latest_version()
      - registry.get_metadata(version)
    """
    request_id = request.headers.get("x-request-id", "unknown")

    logger.info({
        "msg": "Handling /models/latest",
        "requestId": request_id
    })

    version = registry.get_latest_version()
    metadata = registry.get_metadata(version)

    logger.info({
        "msg": "Completed /models/latest",
        "requestId": request_id,
        "version": version
    })

    return LatestModelInfo(version=version, metadata=metadata)