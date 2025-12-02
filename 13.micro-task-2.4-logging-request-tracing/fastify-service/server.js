// server.js - Fastify gateway that calls the Python model API
// Now with basic request ID propagation and structured logging.

import Fastify from "fastify";
import cors from "fastify-cors";
import fetch from "node-fetch";
import { randomUUID } from "crypto";

const fastify = Fastify({
  logger: true
});

// Base URL for the Python model API, injected via environment variable in docker-compose
const PYTHON_API_BASE_URL =
  process.env.PYTHON_API_BASE_URL || "http://localhost:8000";

// Production-ready request ID generator using cryptographically secure UUID
// Uses crypto.randomUUID() (Node.js 14.17.0+) which is:
// - Cryptographically secure (not predictable, unlike Math.random())
// - Globally unique (extremely low collision probability: ~5.3×10^-36)
// - RFC 4122 compliant UUID v4 format (e.g., "550e8400-e29b-41d4-a716-446655440000")
// - More performant than Math.random() for high-throughput scenarios
// - Suitable for distributed systems and production environments
// - Works across multiple instances/servers without coordination
function generateRequestId() {
  // Use crypto.randomUUID() for production-grade uniqueness and security
  // Node.js 20 (used in Dockerfile) fully supports this
  return randomUUID();
}

// Register CORS for easier local testing (optional)
fastify.register(cors, {
  origin: true
});

// Hook: attach / generate a requestId for every incoming request
fastify.addHook("onRequest", async (request, reply) => {
  const incomingId = request.headers["x-request-id"];
  const requestId =
    typeof incomingId === "string" && incomingId.trim().length > 0
      ? incomingId.trim()
      : generateRequestId();

  // Attach to request object so handlers can use it
  request.requestId = requestId;

  // Also echo back to client
  reply.header("x-request-id", requestId);

  // Log basic request info
  fastify.log.info(
    {
      requestId,
      method: request.method,
      url: request.url
    },
    "Incoming request"
  );
});

// Simple health check for the Fastify service itself
fastify.get("/health", async (request, reply) => {
  const requestId = request.requestId;

  fastify.log.info(
    {
      requestId,
      route: "/health"
    },
    "Handling /health"
  );

  return {
    status: "ok",
    detail: "fastify-service running",
    pythonApiBaseUrl: PYTHON_API_BASE_URL,
    requestId
  };
});

// Proxy endpoint: accepts text and optional version, forwards to Python API
fastify.post("/predict", async (request, reply) => {
  const requestId = request.requestId;

  try {
    const { text, version } = request.body || {};

    if (!text || typeof text !== "string") {
      fastify.log.warn(
        {
          requestId,
          body: request.body
        },
        "Invalid /predict request: missing or non-string 'text'"
      );

      reply.code(400);
      return {
        error: "Invalid request: 'text' field is required and must be a string.",
        requestId
      };
    }

    const payload = { text };
    if (version) {
      payload.version = version;
    }

    fastify.log.info(
      {
        requestId,
        route: "/predict",
        pythonUrl: `${PYTHON_API_BASE_URL}/predict`,
        hasVersion: Boolean(version)
      },
      "Calling Python API /predict"
    );

    const pythonResponse = await fetch(`${PYTHON_API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Request-Id": requestId
      },
      body: JSON.stringify(payload)
    });

    if (!pythonResponse.ok) {
      const errorBody = await pythonResponse.text();

      fastify.log.error(
        {
          requestId,
          status: pythonResponse.status,
          body: errorBody
        },
        "Python API responded with non-OK status"
      );

      reply.code(502);
      return {
        error: "Python API error",
        status: pythonResponse.status,
        body: errorBody,
        requestId
      };
    }

    const result = await pythonResponse.json();

    fastify.log.info(
      {
        requestId,
        route: "/predict",
        pythonStatus: pythonResponse.status
      },
      "Python API call successful"
    );

    // You can transform/augment the response here if needed
    return {
      source: "fastify-service",
      pythonApiBaseUrl: PYTHON_API_BASE_URL,
      requestId,
      result
    };
  } catch (err) {
    fastify.log.error(
      {
        requestId,
        err
      },
      "Internal error in /predict handler"
    );

    reply.code(500);
    return {
      error: "Internal server error in fastify-service",
      requestId
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