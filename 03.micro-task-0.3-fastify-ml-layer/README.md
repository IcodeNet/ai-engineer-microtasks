# 03 – Micro-Task 0.3: Fastify ML Layer Abstraction

## Overview

This micro-task refactors the `/predict` endpoint to delegate all prediction logic to a separate "ML layer" module.  
The goal is to separate HTTP concerns (routing, validation) from model concerns (inference), so that the stub can later be replaced with a real Python-backed model without changing the API contract.

🎯 Learning objectives

By completing this micro-task, you will be able to:

- Isolate model logic in a dedicated module (`src/ml/predictor.js`).
- Keep Fastify route handlers thin and focused on I/O and validation.
- Prepare the Node.js service to call out to a Python ML/LLM service in later tasks.


By the end of this micro-task you’ll be able to say:

“My API does not contain business/model logic; it delegates to an ML layer.”

“I can swap the model implementation (stub → Python service) without touching the route contract.”

That’s the bridge to Python models and later to BERT/LLMs.

🧩 Components in this task

ML Layer Module (Node side for now)
New folder:

src/ml/
  predictor.js


This will export a single function, e.g.:

export function predictText(text) {
  // return { prediction, confidence }
}


Later this function becomes a call to Python.

Predict Route → ML Layer
src/routes/predict.js stops doing “clever” work.
It should:

Validate input via schema (already done)

Pull text from request.body

Call predictText(text)

Return the result

Clean API Layer
Your route handlers should now be “thin” and composable. That’s what you’ll show in interviews and code samples.

## Tech Stack

- **Runtime:** Node.js (LTS)
- **Framework:** Fastify
- **Architecture:** Separated API and ML layers

## Project Structure

```text
03.micro-task-0.3-fastify-ml-layer/
  src/
    server.js           # Fastify bootstrap and server startup
    routes/
      index.js          # Route registration (health, info, predict)
      health.js         # GET /health
      info.js           # GET /info
      predict.js        # POST /predict (delegates to ml/predictor.js)
    ml/
      predictor.js      # ML layer: stub prediction function
  package.json
  README.md
