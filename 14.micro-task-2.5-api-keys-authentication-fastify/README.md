# 14.micro-task-2.5-api-keys-authentication-fastify

## Overview

This micro-task adds a simple API key authentication layer to the fastify-service.  
The goal is to ensure that only clients with a valid X-API-Key header can call protected endpoints such as /predict.

Authentication is enforced in the Fastify gateway, which sits in front of the Python model API.

---

## Behaviour After This Micro-Task

- /health:
  - remains public.
  - no API key required.

- /predict:
  - requires a valid API key in header: X-API-Key.
  - if missing or invalid:
    - Fastify returns 401 or 403.
    - The request never reaches the Python API.
  - if valid:
    - normal flow: request is forwarded to the Python API.
    - logging and request tracing still apply.

---

## Configuration

API keys are configured via an environment variable in docker-compose:

In docker-compose.yml under fastify-service:

environment:
  PYTHON_API_BASE_URL: http://python-api:8000
  API_KEYS: test-key-1,test-key-2

You can specify one or more keys, separated by commas.

Example:

API_KEYS=client-a-key,client-b-key,internal-tool-key

In server.js, these are parsed into an in-memory list of valid keys.

---

## How Authentication Works

1. Client sends a request to Fastify:

POST /predict
Headers:
  Content-Type: application/json
  X-API-Key: test-key-1

2. Fastify’s auth hook:

- reads process.env.API_KEYS once at startup.
- splits into an array of keys.
- for each /predict request:
  - reads X-API-Key from headers.
  - checks if it matches one of the configured keys.

3. If X-API-Key is invalid or missing:

- Fastify logs a warning with requestId.
- returns 401 or 403 with JSON error.
- does not contact Python API.

4. If X-API-Key is valid:

- request proceeds as normal.
- Fastify calls the Python API with the same requestId.

---

## Example Requests

### Valid request:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key-1" \
  -d '{"text":"this is great"}'

### Invalid / missing key:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"this is great"}'

Expected: 401/403 with an error message indicating an invalid or missing API key.

---

## Implementation Points (Fastify)

You will add in server.js:

- A small function to load and parse API_KEYS from env.
- A Fastify hook (e.g. preHandler) that:
  - checks request.routerPath or request.raw.url.
  - skips auth for /health.
  - enforces auth for /predict.
- Logging of failures including requestId.

---

## Testing

1. Ensure docker-compose is updated to include API_KEYS for fastify-service.
2. Restart the stack:

cd "14.micro-task-2.5-api-keys-authentication-fastify"
docker compose up --build

3. Run the valid and invalid curl commands above.
4. Check logs:

- docker compose logs -f fastify-service

You should see log entries with:
- requestId
- route
- whether auth passed or failed.

---

## Next Steps

After this basic API key layer, future enhancements might include:

- per-key rate limiting
- roles or scopes per key
- rotating keys via a config or secret store
- replacing API keys with JWT/OAuth2 for user-auth flows.

This micro-task provides the minimal, production-relevant baseline:  
no key → no access to your model.