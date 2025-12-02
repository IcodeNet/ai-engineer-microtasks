// server.js - Fastify gateway that calls the Python model API
// Now with request ID propagation, structured logging, and API key authentication.

import Fastify from "fastify";
import cors from "@fastify/cors";
import fetch from "node-fetch";

const fastify = Fastify({
  logger: true
});

// Base URL for the Python model API, injected via environment variable in docker-compose
const PYTHON_API_BASE_URL =
  process.env.PYTHON_API_BASE_URL || "http://localhost:8000";

// -----------------------------------------------------------------------------
// API Key configuration
// -----------------------------------------------------------------------------
const rawApiKeys = process.env.API_KEYS || "";
const ALLOWED_API_KEYS = rawApiKeys
  .split(",")
  .map(k => k.trim())
  .filter(Boolean);

if (ALLOWED_API_KEYS.length === 0) {
  fastify.log.warn(
    "No API keys configured (API_KEYS env var is empty). All requests will currently be rejected."
  );
}

// -----------------------------------------------------------------------------
// Simple request ID generator (good enough for local/dev)
// -----------------------------------------------------------------------------
function generateRequestId() {
  const rand = Math.random().toString(16).slice(2, 8);
  return `req-${Date.now()}-${rand}`;
}

// Register CORS for easier local testing (optional)
fastify.register(cors, {
  origin: true
});

// -----------------------------------------------------------------------------
// Hook: attach / generate a requestId for every incoming request
// -----------------------------------------------------------------------------
fastify.addHook("onRequest", async (request, reply) => {
  const incomingId = request.headers["x-request-id"];
  const requestId =
    typeof incomingId === "string" && incomingId.trim().length > 0
      ? incomingId.trim()
      : generateRequestId();

  // Attach to request object so handlers and other hooks can use it
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

// -----------------------------------------------------------------------------
// Hook: API key authentication for protected routes
// -----------------------------------------------------------------------------
// We keep /health open, and protect /predict with API key auth.
fastify.addHook("preHandler", async (request, reply) => {
  const requestId = request.requestId;

  // routerPath is only available from this stage onward
  const routePath = request.routerPath || request.raw.url || "";

  // Leave /health (and potentially other public routes) open
  if (routePath === "/health") {
    return;
  }

  // Protect /predict
  if (routePath === "/predict") {
    // If no keys configured, reject everything
    if (ALLOWED_API_KEYS.length === 0) {
      fastify.log.warn(
        {
          requestId,
          routePath
        },
        "Request to protected route but no API keys are configured"
      );
      reply.code(500);
      return {
        error: "Server configuration error: no API keys configured",
        requestId
      };
    }

    const apiKeyHeader = request.headers["x-api-key"];

    const apiKey =
      typeof apiKeyHeader === "string" && apiKeyHeader.trim().length > 0
        ? apiKeyHeader.trim()
        : null;

    if (!apiKey || !ALLOWED_API_KEYS.includes(apiKey)) {
      fastify.log.warn(
        {
          requestId,
          routePath,
          provided: apiKey ? "present" : "missing"
        },
        "Invalid or missing API key"
      );

      reply.code(401);
      return {
        error: "Invalid or missing API key",
        requestId
      };
    }

    // Optionally attach key info for downstream logic
    request.apiKey = apiKey;

    fastify.log.info(
      {
        requestId,
        routePath
      },
      "API key validated successfully"
    );
  }
});

// -----------------------------------------------------------------------------
// Routes
// -----------------------------------------------------------------------------

// Simple health check for the Fastify service itself (public)
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
// Protected by API key via the preHandler hook
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

// -----------------------------------------------------------------------------
// Start the Fastify server
// -----------------------------------------------------------------------------
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