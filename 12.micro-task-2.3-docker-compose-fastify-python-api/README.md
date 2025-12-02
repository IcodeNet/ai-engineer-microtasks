# 12.micro-task-2.3-docker-compose-fastify-python-api

## Overview

This micro-task creates a multi-container environment using docker-compose.  
It runs:

1. A Python FastAPI model API (port 8000)
2. A Fastify gateway service (port 3000)

Both services run in their own containers and communicate through a shared Docker network.  
The model registry is mounted as a volume so the Python API can access model versions without rebuilding the image.

This micro-task recreates a real-world production environment where:
- Node services act as your gateway / BFF
- Python services perform ML inference
- docker-compose handles orchestration, networking, and volumes

---

## How to Run the System

### 1. Navigate into the micro-task folder:

cd "12.micro-task-2.3-docker-compose-fastify-python-api"

### 2. Start both services:

docker compose up --build

This will:
- build python-api
- build fastify-service
- create the shared network
- mount the registry volume
- start Fastify on port 3000
- start Python API on port 8000

---

## Testing the System

### Test Python API directly:

curl http://localhost:8000/health

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"this is excellent"}'

### Test Fastify → Python end-to-end:

curl http://localhost:3000/health

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"this is excellent"}'

Expected output includes:

- source: "fastify-service"
- result: { version, prediction, metadata }

---

## Folder Structure

12.micro-task-2.3-docker-compose-fastify-python-api/
  docker-compose.yml
  registry/
  python-api/
    main.py
    registry.py
    requirements.txt
    Dockerfile
    .dockerignore
  fastify-service/
    server.js
    package.json
    Dockerfile
    README.md
    LEARNING.md

---

## Key Concepts

- docker-compose starts both services with one command
- each service has its own Dockerfile and environment
- containers talk to each other using service names (not localhost)
- the registry folder is mounted into the Python container at /app/registry

This setup mirrors production environments with multiple microservices.

---
 