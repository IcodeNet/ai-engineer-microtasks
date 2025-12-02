# main.py - FastAPI Model Inference API

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from registry import ModelRegistry


class PredictRequest(BaseModel):
    text: str
    version: Optional[str] = None


app = FastAPI(title="Text Classifier API", version="0.1.0")

# Initialise the registry client
registry = ModelRegistry()


@app.get("/health")
def health():
    """
    Simple health check endpoint.
    """
    return {
        "status": "ok",
        "detail": "model API running"
    }


@app.post("/predict")
def predict(request: PredictRequest):
    """
    Predict the sentiment for the given text.
    - If request.version is provided: load that model version.
    - Otherwise: load the latest model from the registry.
    """

    if request.version:
        model, metadata = registry.get_model(request.version)
        version = request.version
    else:
        model, metadata = registry.get_latest_model()
        version = metadata.get("version", "unknown")

    # Perform prediction
    prediction = model.predict([request.text])[0]

    # Build response payload
    return {
        "version": version,
        "prediction": prediction,
        "metadata": {
            "best_cv_accuracy": metadata.get("best_cv_accuracy"),
            "test_accuracy": metadata.get("test_accuracy"),
            "saved_at": metadata.get("saved_at")
        }
    }