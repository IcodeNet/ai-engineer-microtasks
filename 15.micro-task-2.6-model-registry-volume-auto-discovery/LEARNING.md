# LEARNING.md – Micro-Task 2.6 (Model Registry Volume and Auto-Discovery)

This document explains how to treat the model registry as real, durable storage and how to automatically discover model versions instead of hard-coding them.

------------------------------------------------------------
1. Why This Micro-Task Exists
------------------------------------------------------------

Right now you:

- Mount ./registry into the python-api container using docker-compose.
- Have a ModelRegistry that expects a fixed directory layout.
- Still treat the registry mostly as "a local folder we happen to mount".

In a real setup, the model registry is:

- durable (you don’t lose models when recreating containers),
- shared between environments (dev, staging, prod),
- discoverable (you can list versions, promote, roll back).

This micro-task moves you closer to that by:

- treating the registry as a proper volume (separation of code + data),
- adding model version auto-discovery to your ModelRegistry,
- exposing simple introspection (e.g. list available versions endpoint).

------------------------------------------------------------
2. Code vs Data: Why the Registry Must Be a Volume
------------------------------------------------------------

Key separation:

- Code:
  - main.py, registry.py, Fastify, Dockerfiles, etc.
  - Lives in images, versioned via Git and container tags.

- Data (Models):
  - model.joblib
  - metadata.json
  - Stored in registry volume, not baked into the image.

Benefits:

- Re-deploying Python container doesn’t wipe models.
- You can update models by updating the registry volume, not the image.
- Eventually, you can swap the volume for a remote storage (Azure Blob / S3) without changing clients.

docker-compose already mounts:

- ./registry → /app/registry

This micro-task clarifies that this directory is THE source of truth for model artefacts.

------------------------------------------------------------
3. What “Auto-Discovery” Means
------------------------------------------------------------

Up to now, you’ve implicitly known model versions like "1.0.0" and set them in code.

Auto-discovery means:

- the ModelRegistry can:
  - scan registry/versions/* directories,
  - parse version names (e.g. 1.0.0, 1.1.0, 2.0.0),
  - return a list of available versions,
  - determine a “latest” version if needed.

Typical operations you’ll support:

- list_versions()
  - returns all discovered versions as strings.

- get_latest_version()
  - decides which version is “latest” (e.g. highest semantic version).

- get_metadata(version)
  - read metadata.json without loading the model.

This is the beginning of behaving like a real model registry API.

------------------------------------------------------------
4. Improvements to ModelRegistry
------------------------------------------------------------

Your ModelRegistry currently supports:

- save_model(version, model, metadata)
- get_model(version)
- get_latest_model()

In this micro-task you add:

- list_versions()
  - scans registry/versions directory.
- get_latest_version()
  - semantic or simple lexical sort of discovered versions.
- get_metadata(version)
  - read metadata.json for a version.

This allows:

- Python API to implement an optional endpoint, e.g. /models or /models/latest.
- Future admin tools to query available versions without hard-coding.

------------------------------------------------------------
5. Example Directory Layout Revisited
------------------------------------------------------------

Registry volume (on host):

./registry/
  versions/
    1.0.0/
      model.joblib
      metadata.json
    1.1.0/
      model.joblib
      metadata.json
  latest/
    model.joblib
    metadata.json

The ModelRegistry inside the container sees this as:

/app/registry/
  versions/
    1.0.0/
    1.1.0/
  latest/

Auto-discovery:

- list directories under /app/registry/versions
- filter for valid version folders
- sort them and decide what “latest” means.

------------------------------------------------------------
6. API Exposure (Optional but Recommended)
------------------------------------------------------------

You can add auxiliary endpoints in Python, for example:

- GET /models
  → returns a list of available versions + some metadata.

- GET /models/latest
  → returns latest version + metadata.

These are very useful for:

- debugging,
- building dashboards,
- allowing ops or devs to see which model is live.

Fastify can optionally proxy those endpoints later if needed.

------------------------------------------------------------
7. Problem → Solution Section
------------------------------------------------------------

Problem: “How do I know which models are available without opening the filesystem manually?”
Solution:
- ModelRegistry.list_versions() reads the registry/versions directory and returns a list.

Problem: “How do I find which version is ‘latest’?”
Solution:
- Implement get_latest_version() that parses semantic versions and picks the highest.

Problem: “What happens when I deploy a new python-api image?”
Solution:
- As long as the registry volume is mounted back, all models are still there.
- The container can re-discover all versions at startup.

Problem: “How do I inspect model metadata without loading the model?”
Solution:
- Implement get_metadata(version) that just reads metadata.json.

------------------------------------------------------------
8. Summary
------------------------------------------------------------

In this micro-task you:

- Treat the registry as a proper, durable volume separate from code.
- Enhance your ModelRegistry with auto-discovery of versions.
- Optionally expose endpoints for viewing available models and the latest version.
- Move one step closer to a production-grade model registry / model store.

This lays the groundwork for:

- plugging in cloud storage instead of a local folder,
- promotion workflows (e.g. marking a version as “production”),
- separate tools that manage models without touching inference code.

------------------------------------------------------------
9. Fastify Admin Endpoints (How They Relate to This Micro-Task)
------------------------------------------------------------

In this micro-task, you made the model registry:
- durable (volume-based)
- discoverable (list_versions, get_latest_version, get_metadata)
- visible via Python endpoints: /models and /models/latest

To avoid exposing these Python management endpoints directly to external clients, you add
admin routes in the Fastify gateway:

- GET /admin/models
- GET /admin/models/latest

These routes:

- are protected by API key auth (same mechanism as /predict),
- forward the request to:
  - GET /models
  - GET /models/latest
  on the Python API,
- propagate the same X-Request-Id for joined logging,
- then return the response from the Python API to the caller.

Why this belongs conceptually to this micro-task:

- The whole point of this task is treating the registry as a first-class component:
  - volume-backed
  - auto-discoverable
  - introspectable.
- The Fastify admin endpoints are the "operational front door" to those
  capabilities for internal users (devs, ops, product).
- They complete the picture: the registry is not just discoverable internally,
  but also queryable through the same gateway that handles inference requests.
 