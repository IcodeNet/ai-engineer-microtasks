# fastify-service – Gateway for Python Model API

## Overview

This service is a small Fastify-based Node.js application that acts as a gateway in front of the Python model API.

It exposes:

- GET /health
- POST /predict

and forwards prediction requests to the Python API defined by the environment variable:

PYTHON_API_BASE_URL

In docker-compose, this is set to:

http://python-api:8000

---

## How It Fits into Micro-Task 12

This service runs as one container in the compose stack:

- python-api: Python FastAPI model service (port 8000)
- fastify-service: Node Fastify gateway (port 3000)

docker-compose handles:

- building both images
- creating a shared network
- setting PYTHON_API_BASE_URL so Fastify can reach Python

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

Example:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
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

---

## Running in docker-compose

From the root of the micro-task:

cd "13.micro-task-2.4-logging-request-tracing"

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

## Next Steps

Future improvements could include:

- adding authentication (API keys, JWT)
- logging and tracing across Fastify and Python
- better error handling and observability
- request/response schema validation
- integrating with your real product APIs and front-end.