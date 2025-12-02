# IMAGE_NAMING.md – Image, Repository and Registry Naming Conventions

This document defines naming rules for your containers in Azure Container Registry (ACR).

---

## 1. Registry Name

Registry name should be:

- short
- lowercase
- alphanumeric

Example:

- `mycompanyai`
- `flagstoneai`
- `bth-ai-lab`

Azure will expose this registry as:

- `<ACR_NAME>.azurecr.io`

Example:

- `mycompanyai.azurecr.io`

---

## 2. Repository Names

Repository names represent **logical services**, not environments.

Good examples:

- `python-api`
- `fastify-service`
- `ingestion-worker`
- `backoffice-admin-api`

Avoid:

- environment in repo name (`python-api-dev`, `python-api-prod`)
- overly generic names (`service`, `api`)

Environments should be separated using **tags** and/or **separate resource groups**, not by repository name.

---

## 3. Image Name Format

General format:

`<ACR_LOGIN_SERVER>/<repository>:<tag>`

Example:

- `mycompanyai.azurecr.io/python-api:0.1.0`
- `mycompanyai.azurecr.io/fastify-service:0.1.0`

---

## 4. Tag Conventions

Tags should be:

- semantic versions for stable releases:
  - `0.1.0`
  - `0.2.0`
  - `1.0.0`

Optional additional tag strategies:

- build-id tags:
  - `0.1.0-build.123`
- date-based tags:
  - `0.1.0-2025-12-02`

But for this micro-task, keep it simple:

- `0.1.0`, `0.2.0`, etc.

---

## 5. Examples for This Project

Assuming:

- ACR name: `mycompanyai`
- Login server: `mycompanyai.azurecr.io`

Then:

- Python API:
  - `mycompanyai.azurecr.io/python-api:0.1.0`
- Fastify service:
  - `mycompanyai.azurecr.io/fastify-service:0.1.0`

These are the exact strings you will pass to:

- Azure Container Apps
- AKS manifests
- App Service
- CI/CD pipelines

---

## 6. Environment Separation

Do not encode environment into repository names.

Prefer:

- Separate resource groups or Container Apps environments
- Same image tag deployed into:
  - `bth-ai-dev`
  - `bth-ai-staging`
  - `bth-ai-prod`

That keeps artifacts reusable and deployment-specific concerns outside the image itself.