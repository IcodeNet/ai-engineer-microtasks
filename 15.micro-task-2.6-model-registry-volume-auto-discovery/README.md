# 15.micro-task-2.6-model-registry-volume-auto-discovery

## Overview

This micro-task improves how you manage and use the model registry by:

1. Treating `./registry` as a proper, durable volume for model artefacts.
2. Adding simple auto-discovery of model versions to `ModelRegistry`.
3. Optionally exposing endpoints in the Python API for listing models.

The goal is to stop hard-coding model versions in code and start discovering them from the registry volume.

---

## Objectives

By the end of this micro-task you should be able to:

- List all model versions present in `./registry/versions`.
- Ask the registry which version is “latest”.
- Read metadata for a given version without loading the model.
- (Optional) call Python API endpoints like `/models` and `/models/latest` to see what’s available.

---

## Expected Changes

### In `registry.py`:

Add methods such as:

- `list_versions()`:
  - scans the `versions` directory under the registry root.
  - returns a list of version strings, e.g. `["1.0.0", "1.1.0"]`.

- `get_latest_version()`:
  - uses `list_versions()` and returns the highest version.
  - can start with simple lexical sort, or parse semantic versions.

- `get_metadata(version: str)`:
  - reads `metadata.json` under `versions/<version>/`.
  - returns the JSON as a dict.

You keep existing methods:

- `save_model(version, model, metadata)`
- `get_model(version)`
- `get_latest_model()`  
  (which can internally use `get_latest_version()`)

### In `main.py` (Python API):

Optionally add endpoints:

- `GET /models`
  - uses `registry.list_versions()` and `registry.get_metadata()` for each version.
  - returns an array of `{ version, metadata }`.

- `GET /models/latest`
  - uses `registry.get_latest_version()` and `get_metadata()`.

These are management/debug APIs, not for end-users.

---

## Registry Volume Reminder

In `docker-compose.yml`, the python-api service already mounts the registry:

services:
  python-api:
    ...
    volumes:
      - ./registry:/app/registry

This means:

- On host:
  - models live under `./registry`.
- In container:
  - models are visible under `/app/registry`.

Your `ModelRegistry` class should be pointed at `/app/registry` (as it already is).

After this micro-task, you rely on the filesystem structure to discover what’s there, rather than hard-coding version values.

---

## How to Test

1. Ensure you have at least 1–2 versions in your registry:
   - e.g. `./registry/versions/1.0.0`, `./registry/versions/1.1.0`.

2. Rebuild and run docker-compose:

cd "15.micro-task-2.6-model-registry-volume-auto-discovery"
docker compose up --build

3. Inside the running `python-api` container (optional deeper test):

docker exec -it python-api sh

Then in the container shell:

python
>>> from registry import ModelRegistry
>>> r = ModelRegistry()
>>> r.list_versions()
>>> r.get_latest_version()
>>> r.get_metadata("1.0.0")

4. If you add `/models` and `/models/latest` endpoints, test via curl:

curl http://localhost:8000/models
curl http://localhost:8000/models/latest

---

## Folder Structure for This Micro-Task

15.micro-task-2.6-model-registry-volume-auto-discovery/
  README.md
  LEARNING.md
  notes.txt              (optional)
  registry-patches/      (optional, for diff snippets)

Actual code changes live in your existing python-api (registry.py, main.py).

---

## Next Steps

After implementing this, you are ready to:

- point the registry at a remote storage backend (Azure Blob, S3).
- implement promotion flags in metadata (e.g. "stage": "prod", "canary": true).
- build internal tooling for model management and audit.

This micro-task is your bridging step from “filesystem as an implementation detail” to a more explicit “model store” concept.