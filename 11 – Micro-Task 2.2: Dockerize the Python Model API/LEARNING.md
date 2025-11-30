# LEARNING.md – Micro-Task 2.2 (Dockerize the Python Model API)

This document explains why and how you containerise your Python FastAPI model service.

------------------------------------------------------------
1. Why Dockerize the Python API
------------------------------------------------------------

Until now, your Python model API runs directly on your local machine using:

- a local Python interpreter
- a manually created virtualenv
- pip-installed dependencies

Problems with this approach:

- It works only on machines that are set up correctly.
- "Works on my machine" issues become very common.
- Deploying to servers, Azure, or Kubernetes is painful.
- Node/Fastify and Python may require conflicting environments.

Docker solves this by:

- Bundling your code + dependencies into an image.
- Providing a consistent runtime across all machines.
- Giving you a standard unit of deployment for your model service.

Your goal in this micro-task:

- Create a Docker image that runs your FastAPI model API.
- Expose port 8000.
- Use uvicorn as the ASGI server.
  **Explanation:** uvicorn is a fast ASGI (Asynchronous Server Gateway Interface) server for Python web applications. ASGI is the modern standard for async Python web frameworks like FastAPI. uvicorn handles incoming HTTP requests, manages connections, and runs your FastAPI application. It's the production-ready server that actually serves your API endpoints — when you run `uvicorn main:app`, it starts a web server that listens for requests and routes them to your FastAPI app. Think of it as the "engine" that powers your FastAPI service, similar to how Node.js runs JavaScript web servers.
- Prepare this container to be orchestrated alongside Fastify later.

------------------------------------------------------------
2. What the Container Needs to Do
------------------------------------------------------------

The Docker container must:

1. Use a Python base image (e.g. python:3.11-slim).
2. Copy your API code:
   - main.py
   - registry.py
   - requirements.txt
3. Install all required Python packages.
4. Start the FastAPI app using uvicorn.
5. Listen on port 8000 inside the container.

You will then map container port 8000 to host port 8000.

------------------------------------------------------------
3. Important Concepts in the Dockerfile
------------------------------------------------------------

Key Dockerfile concepts you will use:

- FROM:
  Base image (for example: python:3.11-slim).
- WORKDIR:
  Directory inside the container where your app will live.
- COPY:
  Copy files from your repo into the image.
- RUN:
  Execute commands at build time (e.g. pip install).
- EXPOSE:
  Document the port the app listens on (8000).
- CMD:
  Define the command that starts the app (uvicorn main:app ...).

Example of a final run command inside Docker:

uvicorn main:app --host 0.0.0.0 --port 8000

The host 0.0.0.0 is critical. It tells uvicorn to listen on all network interfaces inside the container so that the host machine can reach it.

------------------------------------------------------------
4. Why We Add .dockerignore
------------------------------------------------------------

The .dockerignore file prevents Docker from copying unnecessary files into the build context. This:

- Makes builds faster.
- Keeps the image smaller.
- Avoids accidentally packaging secrets or temp files.

Typical entries:

- .venv/
- __pycache__/
- *.pyc
- .git/

This is similar to .gitignore but for Docker builds.

------------------------------------------------------------
5. Relationship with the Model Registry
------------------------------------------------------------

In earlier micro-tasks, you created a ModelRegistry that stores:

- model.joblib
- metadata.json

under:

registry/
  versions/<version>/
  latest/

For Docker, there are two options:

1. Bake the registry into the image (copy it in).
2. Mount it as a volume at runtime.

For this micro-task, you assume:

- The container is built with code only.
- The registry folder can be mounted or populated later.

The FastAPI code still uses:

from registry import ModelRegistry

and expects the registry directory layout to be usable inside the container.

------------------------------------------------------------
6. Build and Run Workflow
------------------------------------------------------------

After creating the Dockerfile, your workflow will be:

1) Build the image:

docker build -t python-model-api .

2) Run the container:

docker run -p 8000:8000 python-model-api

This maps host port 8000 to container port 8000.

3) Test health:

curl http://localhost:8000/health

If you see the expected JSON response, the containerized API is working.

------------------------------------------------------------
7. Problem → Solution Section
------------------------------------------------------------

Problem: “Why not just run uvicorn directly on the host?”
Solution:
- Docker gives you a reproducible environment.
- Easier deployment to servers and cloud.
- Better isolation between services.

Problem: “How does Fastify call this container?”
Solution:
- Fastify makes HTTP calls to the container’s host/port.
- In docker-compose, this will be done by service name (e.g. http://python-model-api:8000).

Problem: “What about Python version differences?”
Solution:
- Docker fixes the Python version via the base image (python:3.11-slim).
- Every environment using this image will run the same Python version.

Problem: “What if the image doesn’t see my registry?”
Solution:
- Either bake a snapshot of the registry into the image or
- Mount the registry directory as a volume in docker run or docker-compose.
- For now, you just ensure the code runs; in later micro-tasks, you will handle volumes.

------------------------------------------------------------
8. Summary
------------------------------------------------------------

In this micro-task, you:

- Learned why Docker is essential for a production-like ML service.
- Understood how to wrap your FastAPI model API into a container.
- Prepared the service to be run anywhere Docker is available.
- Built the foundation for multi-service orchestration with docker-compose.

The next step is to:

- Use docker-compose to run both:
  - your Node/Fastify service
  - your Python model API container

and wire Fastify to call Python over HTTP using service names.

This is the bridge from local scripts to a fully containerised microservice architecture for your AI components.