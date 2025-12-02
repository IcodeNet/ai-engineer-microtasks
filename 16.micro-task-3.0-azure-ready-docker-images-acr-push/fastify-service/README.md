# fastify-service – Gateway for Python Model API

## Overview

This service is a small Fastify-based Node.js application that acts as a gateway in front of the Python model API.

It exposes:

- GET /health
- POST /predict (protected by API key)
- GET /admin/models (protected by API key)
- GET /admin/models/latest (protected by API key)

and forwards prediction requests to the Python API defined by the environment variable:

PYTHON_API_BASE_URL

In docker-compose, this is set to:

http://python-api:8000

---

## How It Fits into Micro-Task 15

This service runs as one container in the compose stack:

- python-api: Python FastAPI model service (port 8000)
- fastify-service: Node Fastify gateway (port 3000)

docker-compose handles:

- building both images
- creating a shared network
- setting PYTHON_API_BASE_URL so Fastify can reach Python

In this micro-task, the fastify-service also exposes admin endpoints:

- GET /admin/models (protected by API key)
- GET /admin/models/latest (protected by API key)

These endpoints proxy to the Python API's `/models` and `/models/latest` endpoints, allowing internal users to query available model versions without directly accessing the Python API.

---

## Installation (Local, without Docker)

From the fastify-service folder:

npm install

Start in dev mode with auto-reload:

npm run dev

Start in normal mode:

npm start

By default, the service uses:

PYTHON_API_BASE_URL = http://localhost:8000

So you should run the Python API locally on port 8000 in another terminal.

---

## Endpoints

### GET /health

Example:

curl http://localhost:3000/health

Response includes:

- status: "ok"
- detail: "fastify-service running"
- pythonApiBaseUrl: the configured Python API URL

### POST /predict

**Note:** This endpoint requires an API key in the `X-API-Key` header.

Example:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{"text":"this is great"}'

Response structure:

- source: "fastify-service"
- pythonApiBaseUrl: URL used to call Python
- result: raw JSON returned from the Python /predict endpoint

You can also send a version field:

{
  "text": "this is terrible",
  "version": "1.0.0"
}

Fastify will include this version when forwarding to Python.

### GET /admin/models

**Note:** This endpoint requires an API key in the `X-API-Key` header.

Example:

curl http://localhost:3000/admin/models \
  -H "X-API-Key: your-api-key-here"

Returns a list of all available model versions with their metadata.

### GET /admin/models/latest

**Note:** This endpoint requires an API key in the `X-API-Key` header.

Example:

curl http://localhost:3000/admin/models/latest \
  -H "X-API-Key: your-api-key-here"

Returns the latest model version and its metadata.

---

## Running in docker-compose

From the root of the micro-task:

cd "15.micro-task-2.6-model-registry-volume-auto-discovery"

docker compose up --build

- Fastify is available at: http://localhost:3000
- Python API is available at: http://localhost:8000
- Fastify calls Python using: http://python-api:8000

---

## Files

- server.js – Fastify application, includes /health and /predict routes.
- package.json – Node dependencies and scripts.
- Dockerfile – Builds a containerised version of this service.
- LEARNING.md – Explanation of the role and behaviour of this service.

---

## API Key Configuration

The service requires API keys to be configured via the `API_KEYS` environment variable in `docker-compose.yml`:

```yaml
environment:
  API_KEYS: "key1,key2,key3"
```

Multiple keys can be provided as a comma-separated list. All protected endpoints (`/predict`, `/admin/models`, `/admin/models/latest`) require a valid API key in the `X-API-Key` header.

## Next Steps

Future improvements could include:

- role-based access control (different keys for different endpoints)
- rate limiting per API key
- API key rotation and management
- request/response schema validation
- integrating with your real product APIs and front-end