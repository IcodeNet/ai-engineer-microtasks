# LEARNING.md – Micro-Task 2.5 (API Keys and Authentication in Fastify)

This document explains how to add a simple API key authentication layer to the fastify-service so only authorised clients can call your gateway (and indirectly the Python model API).

------------------------------------------------------------
1. Why Add API Keys Now
------------------------------------------------------------

So far, your Fastify gateway:

- accepts any request from anyone
- proxies calls into the Python model API
- runs inside docker-compose, but nothing stops external callers

In a real environment, you must NOT expose the model API to arbitrary callers.

Basic requirements:

- Only authorised systems/clients can:
  - call /predict
  - access your AI behaviour in bulk
- You can:
  - rotate keys
  - issue different keys to different consumers
  - eventually enforce quotas or rate limits per key

This micro-task implements a simple, but realistic first step: API key auth in Fastify.

------------------------------------------------------------
2. What We Will Implement
------------------------------------------------------------

We will:

1) Store one or more API keys in environment variables or config (for now, docker-compose env variable is fine).

2) Require each client to send a header, for example:

   X-API-Key: <some-secret-key>

3) Add a Fastify preHandler / hook that:

   - extracts the X-API-Key from the request
   - compares it against the allowed key(s)
   - rejects the request with 401 or 403 if invalid
   - logs the failure with requestId

4) Allow the health endpoint (/health) to remain public (optional).

5) Optionally add very simple “role-like” behaviour:
   - different keys for "internal" vs "external"
   - for this micro-task, at least support multiple keys via a comma-separated env var.

------------------------------------------------------------
3. API Key Model Used in This Micro-Task
------------------------------------------------------------

We will use:

- An environment variable in Fastify:

  API_KEYS=key1,key2,key3

- For each incoming request to protected routes:
  - read header X-API-Key
  - split API_KEYS env var by comma
  - trim values
  - check if the provided key is in that set

You can improve this later by:

- storing keys in a database or secret store
- attaching metadata to each key (owner, roles, expiry)
- integrating with an identity provider

But for this micro-task, environment variables are enough.

------------------------------------------------------------
4. Which Routes Will Be Protected
------------------------------------------------------------

We will keep it simple:

- /health:
  - remains open (no API key required).
  - Useful for k8s probes, uptime checks.

- /predict:
  - requires API key.
  - No key or invalid key → 401/403.
  - Valid key → normal flow.

You can later expand protection to other routes if you add them.

------------------------------------------------------------
5. Where to Implement the Check in Fastify
------------------------------------------------------------

You’ll add a small hook, for example:

- fastify.addHook("preHandler", authCheck)

The authCheck function will:

1) For each request, decide if the route is protected:
   - If request.routerPath === "/predict" → check key
   - Else (e.g. /health) → allow.

2) If protected:
   - get X-API-Key from headers
   - if missing or invalid:
     - log a warning including:
       - requestId
       - client IP (optional)
       - path
     - reply.code(401 or 403).send({...})
     - do not call handler.

3) If valid:
   - attach a field like request.apiKey = <key> (optional).
   - call next() / move on to the route handler.

------------------------------------------------------------
6. How docker-compose Will Provide Keys
------------------------------------------------------------

In docker-compose.yml, under fastify-service:

environment:
  PYTHON_API_BASE_URL: http://python-api:8000
  API_KEYS: test-key-1,test-key-2

This allows you to:
- set keys per environment
- keep them out of the code base
- change keys without code changes

Locally, you can call Fastify with:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key-1" \
  -d '{"text":"this is great"}'

------------------------------------------------------------
7. Problem → Solution Section
------------------------------------------------------------

Problem: "How do I prevent random callers from hitting /predict?"
Solution:
- Enforce X-API-Key on /predict in Fastify.
- Reject missing or mismatched keys.

Problem: "What if I need multiple keys?"
Solution:
- Use comma-separated list in API_KEYS.
- Parse into an array and check membership.

Problem: "What about Python API security?"
Solution:
- Python is not directly exposed publicly, only reachable inside the Docker network.
- Fastify acts as the enforcement point for external clients.

Problem: "What if keys are leaked?"
Solution:
- Change API_KEYS in environment config.
- Restart Fastify.
- All old keys stop working.

------------------------------------------------------------
8. Summary
------------------------------------------------------------

In this micro-task, you will:

- Introduce API keys as a first authentication mechanism.
- Add an auth hook in Fastify that validates X-API-Key.
- Configure keys via environment variables (docker-compose).
- Protect the /predict route so only authorised clients can call your model.

This is the first step towards more advanced authentication and authorisation (JWT, OAuth2, mTLS, etc.).