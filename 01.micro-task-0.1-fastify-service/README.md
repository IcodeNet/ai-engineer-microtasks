 
# 01 – Micro-Task 0.1: Fastify Service Skeleton

## Overview

This micro-task creates a minimal Fastify-based HTTP service that will act as the foundation for future AI-backed endpoints (e.g. `/predict`).  
It exposes basic operational endpoints and is structured so it can be dockerised and deployed to Azure later.

## Learning Objectives

By completing this micro-task, you will be able to:

- Spin up a Fastify service with a clean, modular structure.
- Expose basic health and metadata endpoints:
  - `GET /health` – service liveness check
  - `GET /info` – simple service metadata (name, version)
- Prepare the Node.js layer that will later call into Python-based ML/LLM inference.

## Tech Stack

- **Runtime:** Node.js (LTS)
- **Framework:** Fastify
- **Logging:** Fastify built-in logger

## Project Structure

```text
01.micro-task-0.1-fastify-service/
  src/
    server.js           # Fastify bootstrap and server startup
    routes/
      index.js          # Route registration (health + info)
      health.js         # GET /health
      info.js           # GET /info
  package.json
  README.md
````

## How to Run

From the `01.micro-task-0.1-fastify-service` folder:

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the service:

   ```bash
   node src/server.js
   ```

3. Verify endpoints:

   * Health check:
     `GET http://localhost:3000/health`
     Expected response:

     ```json
     { "status": "ok" }
     ```

   * Info:
     `GET http://localhost:3000/info`
     Expected response (example):

     ```json
     { "name": "ai-fastify-service", "version": "0.1.0" }
     ```

## Next Steps

The next micro-task will:

* Add JSON schemas to the routes for stronger contracts.
* Introduce a `/predict` endpoint with a stubbed “model” implementation.
* Prepare the API surface for integration with Python-based ML/LLM inference.


 
