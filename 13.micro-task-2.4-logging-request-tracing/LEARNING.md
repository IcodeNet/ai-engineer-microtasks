# LEARNING.md – Micro-Task 2.4 (Logging and Request Tracing Across Services)

This document explains how and why to add logging and request tracing across the Fastify gateway and the Python model API.

------------------------------------------------------------
1. Why This Micro-Task Exists
------------------------------------------------------------

You now have:

- a Fastify gateway (fastify-service)
- a Python model API (python-api)
- docker-compose running both together

What is missing is GOOD OBSERVABILITY:

- When a request fails, where did it fail?
- How do you tie Fastify logs to Python logs for the same request?
- How do you debug latency and errors across services?

This micro-task adds:

- structured logging
- a request ID that flows from Fastify to Python
- consistent log messages that can be grepped or sent to a log system later.

------------------------------------------------------------
2. What We Will Implement
------------------------------------------------------------

You will:

1) Generate or propagate a Request ID in Fastify:
   - For every incoming HTTP request to Fastify, either:
     - use an existing X-Request-Id header, or
     - generate a new ID (e.g. UUID or simple incremental ID).

2) Log with the Request ID in Fastify:
   - Include requestId, method, url, statusCode in logs.
   - Log before and after calling the Python API.

3) Forward the Request ID to Python:
   - When Fastify calls the Python /predict endpoint:
     - send the request ID in the X-Request-Id header.

4) Read the Request ID in Python:
   - In FastAPI, implement middleware:
     - read X-Request-Id from request headers (or generate if missing).
     - log with this ID for every request.
     - optionally attach it to the response headers.

Result:
- Every real request has a unique ID.
- That ID appears in both Fastify and Python logs.
- You can follow a request end-to-end.

------------------------------------------------------------
3. What “Structured Logging” Means Here
------------------------------------------------------------

Instead of free-form string logs like:

"something went wrong in predict"

You aim for logs that are key/value-oriented, for example:

Fastify:

{
  "level": "info",
  "msg": "Calling Python API",
  "requestId": "abc123",
  "path": "/predict",
  "pythonUrl": "http://python-api:8000/predict"
}

Python:

{
  "level": "info",
  "msg": "Handling /predict",
  "requestId": "abc123",
  "path": "/predict"
}

This makes it much easier to filter and search logs later, even in plain text.

------------------------------------------------------------
4. Request ID Lifecycle
------------------------------------------------------------

1) Client → Fastify:
   - Optional: client sends X-Request-Id.
   - If missing, Fastify creates one.

2) Fastify → Python:
   - Fastify logs "incoming HTTP request" with requestId.
   - Fastify forwards X-Request-Id when calling Python API.

3) Inside Python:
   - Middleware reads X-Request-Id.
   - Logs "handling /predict" with that ID.
   - Model logic runs.
   - Logs "completed /predict" with that ID.

4) Python → Fastify:
   - Python returns response to Fastify.
   - Optionally also sets X-Request-Id header in its response.

5) Fastify → Client:
   - Fastify returns response.
   - Fastify logs "responded to client" with requestId.
   - Optionally passes X-Request-Id back to the client.

Now, for a single client request, all logs in both services can be tied together by that requestId.

------------------------------------------------------------
5. Where Changes Go (High Level)
------------------------------------------------------------

Fastify (server.js):

- Add a small preHandler or onRequest hook:
  - read X-Request-Id or generate one.
  - attach to request + reply (e.g. request.requestId).
- Use fastify.log with the requestId for key points:
  - when request enters Fastify (/predict).
  - before calling Python API.
  - after receiving response from Python.
- When calling Python:
  - include header: X-Request-Id: <id>.

Python (main.py):

- Add FastAPI middleware that:
  - reads X-Request-Id from headers (or generates it).
  - logs start/end of each request with that ID.
- Use print or logging module in a structured way:
  - include requestId in the log message.
- Optionally set response header: X-Request-Id.

------------------------------------------------------------
6. Problem → Solution Section
------------------------------------------------------------

Problem: “I see errors, but I cannot tell which logs belong to which request.”
Solution:
- Inject requestId into logs in both services.
- Propagate via X-Request-Id header.

Problem: “How do I debug latency?”
Solution:
- Log timestamps and requestId at:
  - Fastify entry
  - Python entry
  - Python exit
  - Fastify exit
- Compare times for the same requestId.

Problem: “What if clients already send X-Request-Id?”
Solution:
- Reuse it.
- If not provided, generate one.

------------------------------------------------------------
7. Summary
------------------------------------------------------------

In this micro-task, you will:

- Add a request ID per request at the edge (Fastify).
- Propagate that ID to the Python model API.
- Implement logging in both services that includes this ID.
- Gain basic distributed traceability across your small AI microservice stack.

This is a key step towards production-grade observability.