# 13.micro-task-2.4-logging-request-tracing

## Overview

This micro-task adds structured logging and request tracing across:

- fastify-service (Node/Fastify gateway)
- python-api (FastAPI model service)

The goal is to be able to follow a single request through both services using a shared Request ID (X-Request-Id), and to have more useful, structured logs for debugging and observability.

---

## Objectives

By the end of this micro-task, you will:

- Assign a Request ID for each incoming client request in Fastify.
- Log key events in Fastify with the Request ID.
- Forward the Request ID to the Python API via X-Request-Id header.
- Read and log the same Request ID in the Python API.
- Optionally include X-Request-Id in the HTTP responses for client visibility.

---

## Changes You Will Make

### In fastify-service (server.js):

- Add a hook (e.g. onRequest or preHandler) to:
  - read X-Request-Id from incoming headers (if present), or
  - generate a new ID if not present.

- Store this ID on the request object.

- Log with this ID:
  - when /health or /predict is called
  - before calling Python API /predict
  - after receiving the response from Python

- When calling the Python API:
  - include the header: X-Request-Id: <id>

### In python-api (main.py):

- Add FastAPI middleware to:
  - read X-Request-Id from the request headers (or create one if missing)
  - log incoming request with that ID
  - log completion with that ID

- Optionally set X-Request-Id in the response headers.

---

## Example Behaviour

1. Client calls Fastify:

POST http://localhost:3000/predict
Body: { "text": "this is great" }

2. Fastify:

- Assigns requestId = e.g. "req-1234".
- Logs:
  - "Incoming request /predict" with requestId.
- Calls Python:

POST http://python-api:8000/predict
Headers: X-Request-Id: req-1234

3. Python:

- Reads X-Request-Id = req-1234.
- Logs:
  - "Handling /predict" with requestId=req-1234.
  - "Completed /predict" with requestId=req-1234.

4. Fastify:

- Receives result from Python.
- Logs:
  - "Python API call successful" with requestId=req-1234.
- Returns response to client, optionally with:

X-Request-Id: req-1234

5. Client:

- Sees X-Request-Id in the response.
- Can report this ID when filing bugs, allowing engineers to find the exact logs.

---

## How to Test

1) Run your docker-compose stack:

cd "13.micro-task-2.4-logging-request-tracing"
docker compose up --build

2) Send a prediction request:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"this is excellent"}' -i

3) Check:

- That the response may include X-Request-Id.
- That logs from both fastify-service and python-api include a matching requestId value.

You can view logs with:

docker compose logs -f fastify-service
docker compose logs -f python-api

---

## Folder Structure (Suggested)

13.micro-task-2.4-logging-request-tracing/
  README.md
  LEARNING.md
  notes.txt              (optional, for your own experiments)
  fastify-patches/       (optional)
  python-api-patches/    (optional)

In practice, the actual code changes live in the existing micro-task 12 services:
- fastify-service/server.js
- python-api/main.py

This micro-task focuses on the behaviour, not duplicating service repos.

---

## Next Steps

After implementing logging and request tracing, next typical tasks are:

- Hook logs into a centralised log solution (ELK, Loki, Azure Monitor)
- Add correlation IDs to other services (databases, queues, etc.)
- Implement structured logging formats (JSON logs)
- Add metrics and basic tracing (e.g. OpenTelemetry)

This micro-task is the foundation of real observability in your AI microservice stack.