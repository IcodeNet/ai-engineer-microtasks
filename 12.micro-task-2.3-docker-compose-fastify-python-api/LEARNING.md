# LEARNING.md – Micro-Task 2.3 (docker-compose for Fastify + Python Model API)

This document explains why docker-compose is required, what it solves, and how the Fastify gateway and Python model API communicate inside a shared container network.

------------------------------------------------------------
1. Why This Micro-Task Exists
------------------------------------------------------------

In Micro-Task 11, you dockerised the Python API individually.

In this micro-task, you bring two independent services together:

1. The Python model API (FastAPI, port 8000)
2. The Fastify gateway (Node.js, port 3000)

Both services must run:
- together
- in separate containers
- on a shared internal network
- with stable service-to-service names (instead of localhost)

docker-compose is the tool that runs multi-container systems locally.

This micro-task simulates real multi-service deployments in Azure or Kubernetes.

------------------------------------------------------------
2. What docker-compose Solves
------------------------------------------------------------

Without docker-compose:
- You run `docker run` manually for each service.
- You assign ports manually.
- You must pass environment variables yourself.
- You must manage container networking manually.

docker-compose provides:
- one command (`docker compose up`)
- automatic service networking
- stable DNS service names (e.g. `http://python-api:8000`)
- shared volumes (for model registry)
- automatic dependency ordering (`depends_on`)
- a reproducible local environment

------------------------------------------------------------
3. How the Services Communicate
------------------------------------------------------------

In docker-compose:

- Each service is placed on the same custom network (`app-network`).
- Docker automatically assigns DNS names based on service names.

So in Fastify:

PYTHON_API_BASE_URL = "http://python-api:8000"

works because:
- `python-api` is the container name AND the DNS hostname.

No localhost.  
No manual IPs.  
No port guessing.

------------------------------------------------------------
4. What the Registry Volume Does
------------------------------------------------------------

Your model registry is stored locally in:

./registry/

docker-compose mounts it into the Python container:

- host: ./registry
- container: /app/registry

This allows the container to load:

- models/<version>/model.joblib
- models/<version>/metadata.json
- latest/model.joblib

This keeps model data outside the container so it can be updated without rebuilding the image.

------------------------------------------------------------
5. docker-compose.yml Breakdown
------------------------------------------------------------

Service: python-api
- built from python-api/Dockerfile
- exposes port 8000
- mounts registry volume
- sits on app-network

Service: fastify-service
- built from fastify-service/Dockerfile
- exposes port 3000
- depends_on python-api (ensures python loads first)
- environment variable points to python-api URL
- sits on app-network

Network: app-network
- shared bridge network so services can see each other

------------------------------------------------------------
6. Typical Developer Workflow
------------------------------------------------------------

Start everything:

docker compose up --build

Stop:

docker compose down

Rebuild only Fastify:

docker compose build fastify-service

View logs:

docker compose logs -f python-api
docker compose logs -f fastify-service

------------------------------------------------------------
7. Problem → Solution Section
------------------------------------------------------------

Problem: “Why can’t Fastify call localhost:8000?”
Solution: localhost inside a container is the container itself. The Python API runs in a different container. docker-compose provides service names for cross-container requests.

Problem: “Why mount the registry instead of baking it into the Python image?”
Solution: Models change frequently. Rebuilding the whole image for every model version is slow and unnecessary.

Problem: “How do I update a model while containers are running?”
Solution: Replace files inside ./registry — no rebuild required.

Problem: “What happens if Python API starts after Fastify?”
Solution: docker-compose `depends_on` ensures Python starts first.

------------------------------------------------------------
8. Summary
------------------------------------------------------------

In this micro-task, you:

- built a multi-container microservice environment
- connected Fastify → Python API using docker networking
- mounted a registry volume to allow runtime model access
- learned how to orchestrate multiple AI services together

This forms the foundation for:
- local MLOps pipelines
- real-world multi-service deployments
- scaling models and gateways independently

Next micro-task options:
- Add logging + request tracing
- Add API keys and auth
- Move registry to a proper Azure storage volume
- Deploy both services to Azure Container Apps