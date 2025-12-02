// server.js - Fastify gateway that calls the Python model API

import Fastify from "fastify";
import cors from "fastify-cors";
import fetch from "node-fetch";

const fastify = Fastify({
  logger: true
});

// Base URL for the Python model API, injected via environment variable in docker-compose
const PYTHON_API_BASE_URL =
  process.env.PYTHON_API_BASE_URL || "http://localhost:8000";

// Register CORS for easier local testing (optional)
fastify.register(cors, {
  origin: true
});

// Simple health check for the Fastify service itself
fastify.get("/health", async (request, reply) => {
  return {
    status: "ok",
    detail: "fastify-service running",
    pythonApiBaseUrl: PYTHON_API_BASE_URL
  };
});

// Proxy endpoint: accepts text and optional version, forwards to Python API
fastify.post("/predict", async (request, reply) => {
  try {
    const { text, version } = request.body || {};

    if (!text || typeof text !== "string") {
      reply.code(400);
      return {
        error: "Invalid request: 'text' field is required and must be a string."
      };
    }

    const payload = { text };
    if (version) {
      payload.version = version;
    }

    const pythonResponse = await fetch(`${PYTHON_API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!pythonResponse.ok) {
      const errorBody = await pythonResponse.text();
      reply.code(502);
      return {
        error: "Python API error",
        status: pythonResponse.status,
        body: errorBody
      };
    }

    const result = await pythonResponse.json();

    // You can transform/augment the response here if needed
    return {
      source: "fastify-service",
      pythonApiBaseUrl: PYTHON_API_BASE_URL,
      result
    };
  } catch (err) {
    fastify.log.error(err);
    reply.code(500);
    return {
      error: "Internal server error in fastify-service"
    };
  }
});

// Start the Fastify server
const start = async () => {
  try {
    const port = process.env.PORT || 3000;
    await fastify.listen(port, "0.0.0.0");
    fastify.log.info(`fastify-service listening on port ${port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();