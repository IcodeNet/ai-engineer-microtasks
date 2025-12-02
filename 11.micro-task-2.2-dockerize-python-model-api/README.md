# 11.micro-task-2.2-dockerize-python-model-api

## Overview

This micro-task packages your FastAPI-based Python model inference service into a Docker container. This allows the service to run consistently across different machines and prepares it for use in docker-compose with your Fastify service in the next micro-task.

The Docker image will:

- Include your FastAPI application (main.py)
- Include the model registry client (registry.py)
- Install dependencies from requirements.txt
- Expose port 8000
- Start the API using uvicorn

After this micro-task, your Python model API becomes a portable, deployable unit.

---

## Requirements

Before starting, ensure this folder contains:

- main.py (from micro-task 10)
- registry.py (from micro-task 09)
- requirements.txt (FastAPI, uvicorn, scikit-learn, joblib, pydantic)
- Dockerfile (you will generate next)
- .dockerignore (you will generate next)

The registry folder can be mounted later; it does not need to be included inside the image for this micro-task.

---

## Running the Docker Image

### 1. Build the Docker image

```bash
docker build -t python-model-api .
```

**Explanation:** This command builds a Docker image from the Dockerfile in the current directory. Breaking it down:
- `docker build` - The command to build a Docker image
- `-t python-model-api` - Tags the image with the name "python-model-api" (the `-t` flag stands for "tag"). This name is what you'll use to reference the image when running containers
- `.` - The build context (the current directory). Docker looks for a Dockerfile here and uses files in this directory (respecting .dockerignore) to build the image

**What happens during the build:**
1. Docker reads the Dockerfile line by line
2. Starts with the base image (python:3.11-slim)
3. Copies your files (main.py, registry.py, text_utils.py, registry/)
4. Installs dependencies from requirements.txt
5. Sets up the working directory and exposes port 8000
6. Creates a final image tagged as "python-model-api"

**Note:** The first build takes longer as it downloads the base image and installs dependencies. Subsequent builds are faster due to Docker's layer caching.

### 2. Run the container

```bash
docker run -p 8000:8000 python-model-api
```

**Explanation:** This command starts a container from the "python-model-api" image. Breaking it down:
- `docker run` - The command to create and start a new container from an image
- `-p 8000:8000` - Port mapping flag (the `-p` stands for "publish"). The format is `host_port:container_port`:
  - First `8000` = port on your host machine (your computer)
  - Second `8000` = port inside the container (where the FastAPI app listens)
  - This creates a bridge so requests to `localhost:8000` on your machine are forwarded to port 8000 inside the container
- `python-model-api` - The name of the image to run (the one you built in step 1)

**What happens:**
1. Docker creates a new container from the image
2. Starts the container and runs the CMD from the Dockerfile (`uvicorn main:app --host 0.0.0.0 --port 8000`)
3. Maps your host's port 8000 to the container's port 8000
4. The FastAPI app starts listening inside the container
5. You can now access it at `http://localhost:8000` from your host machine

**Note:** The container runs in the foreground (you'll see logs). Press `Ctrl+C` to stop it. To run in the background, add `-d` flag: `docker run -d -p 8000:8000 python-model-api`

### 3. Test the API

Health:

curl http://localhost:8000/health

Predict using latest model:

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"this is great"}'

Predict using a specific version:

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"this is terrible", "version": "1.0.0"}'

---

## Project Structure

11.micro-task-2.2-dockerize-python-model-api/
  main.py
  registry.py
  Dockerfile
  .dockerignore
  requirements.txt
  README.md
  LEARNING.md

Registry contents (model.joblib, metadata.json) will be mounted later using docker-compose.

---

## Notes

- The Dockerfile will use python:3.11-slim as the base.
- The app will run using uvicorn main:app --host 0.0.0.0 --port 8000.
- Exposing 0.0.0.0 is required for container networking.
- This micro-task sets up the container; the next one will run it together with Fastify using docker-compose.

---

## Next Micro-Task

The next step after this is:

12.micro-task-2.3-docker-compose-fastify-python-api

This will let both services communicate using service names, e.g.:

http://python-model-api:8000/predict