# main.py – FastAPI Model Inference API
# Now with request ID middleware + structured logging.

from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import time
import uuid
import logging
import json

from registry import ModelRegistry


# ------------------------------------------------------------------------------
# Logging Setup (structured logging with JSON formatting)
# ------------------------------------------------------------------------------
logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)

logger = logging.getLogger("python-api")


# ------------------------------------------------------------------------------
# Helper: Format structured log messages as JSON strings
# ------------------------------------------------------------------------------
def log_structured(level: str, data: dict):
    """
    Log structured data as JSON string for better parsing and filtering.
    Production logging systems (e.g., ELK, Splunk, CloudWatch) can parse JSON logs.
    """
    message = json.dumps(data, ensure_ascii=False)
    getattr(logger, level.lower())(message)


# ------------------------------------------------------------------------------
# Request Models
# ------------------------------------------------------------------------------
class PredictRequest(BaseModel):
    text: str
    version: Optional[str] = None


# ------------------------------------------------------------------------------
# FastAPI App + Registry
# ------------------------------------------------------------------------------
app = FastAPI(title="Text Classifier API", version="0.1.0")
registry = ModelRegistry()


# ------------------------------------------------------------------------------
# Production-ready request ID generator using cryptographically secure UUID
# ------------------------------------------------------------------------------
def generate_request_id():
    """
    Generate a production-ready request ID using UUID v4.
    
    Uses uuid.uuid4() which is:
    - Cryptographically secure (not predictable, unlike truncated hex)
    - Globally unique (extremely low collision probability: ~5.3×10^-36)
    - RFC 4122 compliant UUID v4 format (e.g., "550e8400-e29b-41d4-a716-446655440000")
    - Suitable for distributed systems and production environments
    - Works across multiple instances/servers without coordination
    
    Returns full UUID string (not truncated) for maximum uniqueness and compatibility
    with distributed tracing systems (e.g., OpenTelemetry, Jaeger).
    """
    return str(uuid.uuid4())


# ------------------------------------------------------------------------------
# Middleware: attach requestId to every request + log start/end
# ------------------------------------------------------------------------------
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    # Read incoming ID from Fastify or generate a new one
    # Validate incoming ID: must be a non-empty string (matches Node.js behavior)
    incoming = request.headers.get("x-request-id")
    request_id = (
        incoming.strip() 
        if incoming and isinstance(incoming, str) and incoming.strip()
        else generate_request_id()
    )

    # Store on request state so handlers can access it (similar to Fastify's request.requestId)
    request.state.request_id = request_id

    start = time.time()

    # Log request start
    log_structured("info", {
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
    log_structured("info", {
        "msg": "Completed request",
        "path": request.url.path,
        "method": request.method,
        "durationMs": duration_ms,
        "requestId": request_id,
        "statusCode": response.status_code
    })

    return response


# ------------------------------------------------------------------------------
# Health Endpoint
# ------------------------------------------------------------------------------
@app.get("/health")
def health(request: Request):
    # Get request ID from state (set by middleware) or fallback to header
    request_id = getattr(request.state, "request_id", request.headers.get("x-request-id", "unknown"))

    log_structured("info", {
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
    # Get request ID from state (set by middleware) or fallback to header
    request_id = getattr(request.state, "request_id", request.headers.get("x-request-id", "unknown"))

    log_structured("info", {
        "msg": "Handling /predict",
        "requestId": request_id,
        "version": request_payload.version
    })

    try:
        # Load correct model version
        if request_payload.version:
            try:
                model, metadata = registry.get_model(request_payload.version)
                version = request_payload.version
            except FileNotFoundError:
                log_structured("error", {
                    "msg": "Model version not found",
                    "requestId": request_id,
                    "version": request_payload.version
                })
                raise HTTPException(
                    status_code=404,
                    detail=f"Model version '{request_payload.version}' not found"
                )
        else:
            try:
                model, metadata = registry.get_latest_model()
                version = metadata.get("version", "unknown")
            except FileNotFoundError:
                log_structured("error", {
                    "msg": "Latest model not found",
                    "requestId": request_id
                })
                raise HTTPException(
                    status_code=500,
                    detail="Latest model not available"
                )

        # Perform prediction
        try:
            prediction = model.predict([request_payload.text])[0]
        except Exception as e:
            log_structured("error", {
                "msg": "Prediction failed",
                "requestId": request_id,
                "modelVersion": version,
                "error": str(e)
            })
            raise HTTPException(
                status_code=500,
                detail="Prediction failed"
            )

        log_structured("info", {
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
    except HTTPException:
        # Re-raise HTTP exceptions (already logged)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        log_structured("error", {
            "msg": "Unexpected error in /predict",
            "requestId": request_id,
            "error": str(e),
            "errorType": type(e).__name__
        })
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )