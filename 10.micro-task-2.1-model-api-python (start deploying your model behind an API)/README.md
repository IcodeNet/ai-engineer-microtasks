
# 10 – Micro-Task 2.1: Python Model API (FastAPI)

## Overview

This micro-task exposes your trained and versioned machine learning model through an HTTP API using FastAPI. The API loads the latest model from your model registry by default, but it can also load a specified version. It provides two endpoints:

- GET /health
- POST /predict

This API will later be consumed by your Node/Fastify backend or any other service.

## Endpoints

### GET /health

Returns a simple health status.

Example response:

{
  "status": "ok",
  "detail": "model API running"
}

### POST /predict

Accepts text input and returns the prediction with model version and metadata.

Request body:

{
  "text": "this is great",
  "version": "1.0.0"
}

The version field is optional. If omitted, the API loads the latest model.

Example response:

{
  "version": "1.0.0",
  "prediction": "positive",
  "metadata": {
    "best_cv_accuracy": 0.6,
    "test_accuracy": 0.33,
    "saved_at": "2025-12-01T09:32:41Z"
  }
}

## Project Structure

10.micro-task-2.1-model-api-python/
  main.py
  registry.py
  README.md
  LEARNING.md
  requirements.txt
  registry/
    versions/
      1.0.0/
        model.joblib
        metadata.json
    latest/
      model.joblib
      metadata.json

registry.py should be copied from micro-task 09.

## How to Run the API

1. (Optional) Create a virtual environment:

python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

2. Install dependencies:

pip install fastapi uvicorn scikit-learn joblib

3. Start the API server:

uvicorn main:app --reload

The API will be available at:

http://localhost:8000

4. Test the API

Health:

curl http://localhost:8000/health

Predict using latest:

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "this is great"}'

Predict using a specific version:

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "this is terrible", "version": "1.0.0"}'

## Next Steps

After this micro-task, you can:

- Add request logging
- Add authentication or API keys
- Package the service into a Docker image
- Deploy behind NGINX or Azure API Gateway
- Create a Fastify route that calls this Python API

This micro-task establishes your first Python-based inference service.