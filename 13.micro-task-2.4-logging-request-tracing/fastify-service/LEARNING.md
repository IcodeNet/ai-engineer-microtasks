# LEARNING.md – fastify-service (Gateway for Python Model API)

This document explains the role of the fastify-service in the architecture and how it interacts with the Python model API.

------------------------------------------------------------
1. Purpose of fastify-service
------------------------------------------------------------

The fastify-service acts as a gateway / backend-for-frontend (BFF) in front of the Python model API.

Responsibilities:
- Expose a stable HTTP interface for clients (e.g. React app, other services).
- Call the Python model API over the internal Docker network.
- Handle basic validation and error handling.
- Optionally enrich or transform responses before sending them to clients.

In this micro-task, the fastify-service offers:
- GET /health
- POST /predict

------------------------------------------------------------
2. How it Connects to Python API
------------------------------------------------------------

The Fastify service does NOT talk to localhost:8000.

Instead, it uses an environment variable:

PYTHON_API_BASE_URL

In docker-compose.yml, this is set to:

http://python-api:8000

The host "python-api" matches the service name defined in docker-compose. Docker's internal DNS resolves "python-api" to the correct container.

In server.js:

const PYTHON_API_BASE_URL =
  process.env.PYTHON_API_BASE_URL || "http://localhost:8000";

During local non-docker testing, localhost:8000 can be used.  
Inside docker-compose, the environment variable overrides it to the container hostname.

------------------------------------------------------------
3. Endpoints Exposed by fastify-service
------------------------------------------------------------

1) GET /health

- Returns status of the fastify-service itself.
- Also returns the configured PYTHON_API_BASE_URL for debugging.

2) POST /predict

- Expects JSON body:
  {
    "text": "some text",
    "version": "optional model version"
  }

- Validates that "text" is present and is a string.
- Builds a payload for the Python API.
- Calls: POST {PYTHON_API_BASE_URL}/predict
- Returns a combined payload including:
  - information that the request passed through fastify-service
  - the raw result from the Python API (prediction, metadata)

------------------------------------------------------------
4. Why Use Node/Fastify in Front of Python
------------------------------------------------------------

Reasons this pattern is common in real systems:

- Node/Fastify can:
  - handle authentication and authorisation
  - centralise logging, metrics and tracing
  - integrate with existing Node-based backend stack
  - provide a single API surface to front-end clients

- Python focuses on:
  - model inference
  - numerical and ML logic
  - staying close to the data science code

This separation allows each part to:
- use the best language and stack for its job
- be deployed and scaled independently

------------------------------------------------------------
5. Running fastify-service in Docker
------------------------------------------------------------

Inside its own Dockerfile:

- Base image: node:20-alpine
- Working directory: /app
- Copies package.json and runs npm install
- Copies server.js
- Exposes port 3000
- Starts server with: npm start

docker-compose sets:

- ports:
  - "3000:3000" (host → container)
- depends_on:
  - python-api (ensures Python API is started first)
- environment:
  - PYTHON_API_BASE_URL=http://python-api:8000

------------------------------------------------------------
6. dev vs production
------------------------------------------------------------

In development:
- You can run fastify-service directly with:
  - npm install
  - npm run dev
- and point it at a local Python API running on localhost:8000.

In docker-compose:
- docker builds and runs the container.
- Node connects to the Python container using the service name "python-api".
- Both services share the same Docker network.

------------------------------------------------------------
7. Problem → Solution Section
------------------------------------------------------------

Problem: "Why is PYTHON_API_BASE_URL not localhost?"
Solution: Inside Docker, localhost points to the Fastify container itself. The Python API runs in a different container, so you must use its service name.

Problem: "Why put validation in Fastify and not Python?"
Solution: Fastify is the gateway and first line of defence. It can quickly reject bad requests and prevent invalid traffic from reaching Python.

Problem: "What if Python API goes down?"
Solution:
- fastify-service /predict will return a 502-like error (configured in server.js).
- Frontend can see error and display fallback UI.
- You can later integrate retries, circuit breakers, etc.

------------------------------------------------------------
8. Summary
------------------------------------------------------------

The fastify-service is:
- the gateway / BFF in front of the Python model API
- responsible for validating requests and proxying calls
- configured via PYTHON_API_BASE_URL to talk to Python
- running in its own container and communicating over a Docker network

This is a standard pattern in modern AI microservice architectures.