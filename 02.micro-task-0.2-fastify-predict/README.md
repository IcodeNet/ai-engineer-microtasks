# 02 – Micro-Task 0.2: Fastify `/predict` with Schema and Stub

## Overview

This micro-task extends the Fastify service by adding a `/predict` endpoint with JSON schema validation.  
The endpoint uses a stubbed "model" implementation that simulates an AI prediction.  
Later tasks will replace the stub with real Python-based ML/LLM inference.

## Learning Objectives

By completing this micro-task, you will be able to:

- Define a clear request/response contract for an AI prediction endpoint.
- Use Fastify's JSON schema support to validate incoming requests and outgoing responses.
- Implement a `/predict` route that is ready to be wired to a real model.

## Tech Stack

- **Runtime:** Node.js (LTS)
- **Framework:** Fastify
- **Validation:** Fastify JSON schema (AJV)

## Project Structure

```text
02.micro-task-0.2-fastify-predict-stub/
  src/
    server.js           # Fastify bootstrap and server startup
    routes/
      index.js          # Route registration (health, info, predict)
      health.js         # GET /health
      info.js           # GET /info
      predict.js        # POST /predict (schema + stub)
  package.json
  README.md


## 1. How Fastify schema validation actually works

In Fastify, every route can have an options object. Inside that you can add a `schema` key.

Basic pattern:

```js
app.post('/example', {
  schema: {
    body: { /* JSON Schema describing the request body */ },
    response: {
      200: { /* JSON Schema describing a 200 OK response */ }
    }
  }
}, async (request, reply) => {
  // request.body is already validated here
});
```

Fastify will:

* Validate `request.body` **before** your handler runs.
* Reject bad input with `400` + a JSON error.
* Validate your response (if `response` schemas are defined) and complain in dev if you return something invalid.

You’re effectively defining **contracts**, not just endpoints.

---

## 2. The `/predict` contract we’ll use

We’ll keep it simple and “ML-shaped”:

**Request body**

```json
{
  "text": "some user input"
}
```

**Response body**

```json
{
  "prediction": "positive",
  "confidence": 0.93
}
```

So the schemas become:

### `body` schema

```js
const predictBodySchema = {
  type: 'object',
  required: ['text'],
  properties: {
    text: { type: 'string', minLength: 1 }
  },
  additionalProperties: false
};
```

### `response` schema (for HTTP 200)

```js
const predictResponseSchema = {
  200: {
    type: 'object',
    required: ['prediction', 'confidence'],
    properties: {
      prediction: { type: 'string' },
      confidence: { type: 'number', minimum: 0, maximum: 1 }
    },
    additionalProperties: false
  }
};
```

Then you plug them into the route:

```js
app.post('/predict', {
  schema: {
    body: predictBodySchema,
    response: predictResponseSchema
  }
}, async (request, reply) => {
  // request.body is guaranteed to have a non-empty string 'text'
});
```
  

## API Contract

### POST `/predict`

**Request body**

```json
{
  "text": "some input text"
}
```

**Response body (200)**

```json
{
  "prediction": "positive",
  "confidence": 0.93
}
```

## How to Run

From the `02.micro-task-0.2-fastify-predict-stub` folder:

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the service:

   ```bash
   node src/server.js
   ```

3. Test endpoints:

   * Health check:
     `GET http://localhost:3000/health`

   * Info:
     `GET http://localhost:3000/info`

   * Predict:
     `POST http://localhost:3000/predict` with JSON body:

     ```json
     { "text": "hello world" }
     ```

     Expected example response:

     ```json
     {
       "prediction": "positive",
       "confidence": 0.9
     }
     ```

     
```
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a bad example"}'

  {"prediction":"negative","confidence":0.9}
```

```
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"This is good"}'

  {"prediction":"positive","confidence":0.9}
```
 


## Next Steps

The next micro-task will introduce:

* A separate "ML layer" module for prediction logic.
* The first Python-backed model that the Node.js service can call into.

```
 
