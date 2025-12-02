# LEARNING.md – Micro-Task 2.1 (Python Model API with FastAPI)

This document explains the purpose, concepts, and code structure of your first machine learning inference API built with FastAPI.

------------------------------------------------------------
1. Why This Micro-Task Exists
------------------------------------------------------------

Up to this point, your workflow has been:

- train model with train.py
- version the model
- store it in the model registry
- make predictions with predict.py

Real systems do not run "predict.py". They expose models through an API so that:

- Node/Fastify services can call it
- front-end applications can access it through a backend-for-frontend
- batch jobs can query it
- external systems can integrate with it

This micro-task transforms your model into an online inference service.

------------------------------------------------------------
2. What FastAPI Provides
------------------------------------------------------------

FastAPI gives you:

- an HTTP server
- automatic request validation via Pydantic
- automatic OpenAPI/Swagger documentation
- async support for scaling
- easy integration with your model registry

You will build two endpoints:

GET /health
POST /predict

------------------------------------------------------------
3. How the API Loads the Model
------------------------------------------------------------

The API uses the ModelRegistry abstraction introduced in micro-task 09.

To load the latest model:

model, metadata = registry.get_latest_model()

To load a specific version:

model, metadata = registry.get_model("1.0.0")

This ensures:

- consistent loading
- version tracking
- flexibility to test old versions
- clean separation between model storage and inference

------------------------------------------------------------
4. Request and Response Structure
------------------------------------------------------------

POST /predict expects JSON:

{
  "text": "this is great",
  "version": "1.0.0"
}

Fields:
- text: required
- version: optional (default: latest)

The API returns:

{
  "version": "1.0.0",
  "prediction": "positive",
  "metadata": {
    "best_cv_accuracy": 0.6,
    "test_accuracy": 0.33,
    "saved_at": "2025-12-01T09:32:41Z"
  }
}

This response format ensures:
- you know which model served the request
- metadata is available for debugging and observability

------------------------------------------------------------
5. Mapping Code Concepts Clearly
------------------------------------------------------------

5.1 Pydantic Input Model

class PredictRequest(BaseModel):
    text: str
    version: Optional[str] = None

This enforces the contract for incoming requests.

5.2 FastAPI App

app = FastAPI(title="Text Classifier API", version="0.1.0")

Defines the basic app and metadata.

5.3 Health Endpoint

@app.get("/health")

Used for:
- Kubernetes readiness/liveness probes
- uptime checks
- debugging local server state

5.4 Predict Endpoint

@app.post("/predict")

Key logic:
1. Determine which model to load
2. Perform prediction: model.predict([request.text])
3. Return prediction + metadata

------------------------------------------------------------
6. Problem → Solution Section
------------------------------------------------------------

Problem: “How does Node/Fastify talk to Python?”
Solution: Through HTTP using fetch or axios.

Example (pseudo-code):

const response = await fetch("http://python-api:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "hello world" })
});

Problem: “How does the API know which version to use?”
Solution: The request can specify `version`, otherwise latest is loaded.

Problem: “How do I roll back a model?”
Solution: Call the API with a specific version.

Problem: “How do we ensure traceability?”
Solution: The API returns metadata describing the model.

------------------------------------------------------------
7. Commands to Test the API
------------------------------------------------------------

Start server:

uvicorn main:app --reload

Test health:

curl http://localhost:8000/health

Test prediction (latest):

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "this is good"}'

Test prediction (specific version):

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "this is terrible", "version": "1.0.0"}'

------------------------------------------------------------
8. Summary
------------------------------------------------------------

In this micro-task you:

- created a FastAPI-based ML inference service
- integrated it with your local model registry
- implemented version-aware model loading
- structured predictable request/response contracts
- prepared the system for integration with Node/Fastify
- built the foundation of a production ML microservice

Next steps after this micro-task could include:

- Dockerizing the API
- exposing it through Fastify
- adding authentication and API keys
- adding observability (logging, metrics)
- deploying to Azure Container Apps or Kubernetes

This micro-task marks the transition from offline ML scripts to online, callable AI systems.