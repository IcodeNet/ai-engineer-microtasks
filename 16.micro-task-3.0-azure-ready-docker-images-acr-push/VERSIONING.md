# VERSIONING.md – Docker Image Versioning Strategy

## Goal

Define a **simple, consistent, production-friendly** versioning scheme for:

- `python-api` Docker image
- `fastify-service` Docker image

This is about **service versions**, not ML model versions.

---

## 1. Semantic Versioning

We use **semantic versioning**:

`MAJOR.MINOR.PATCH`

Examples:

- `0.1.0`
- `0.2.0`
- `1.0.0`
- `1.1.3`

### Rules

- **MAJOR**: Breaking changes to the API or behaviour.
- **MINOR**: New features, non-breaking changes.
- **PATCH**: Bug fixes, small tweaks, internal changes.

---

## 2. When to Bump Which Part

Examples:

- `0.1.0` → `0.1.1`
  - Logging change
  - Minor refactor
  - No change to API or responses

- `0.1.0` → `0.2.0`
  - New endpoint added
  - Backwards compatible change

- `0.1.0` → `1.0.0`
  - Breaking change in API contract
  - Response shape changes
  - Path changes (`/predict` → `/v2/predict` etc.)

---

## 3. Aligning With Registry Models

Your ML model version (e.g. `1.0.0`, `1.1.0`) is **separate** from the **service version**.

You can:

- Let ML model version live in **metadata** and registry
- Let Docker image version live in **semantic tags** for the service

Example:

- `python-api` Docker image: `0.3.0`
- Inside that image, default model version: `1.2.0`

The Docker tag tells you **what service you are running**, not the model weights.

---

## 4. Tag Examples in ACR

Assuming:

- ACR login server: `mycompanyai.azurecr.io`

Examples:

- `mycompanyai.azurecr.io/python-api:0.1.0`
- `mycompanyai.azurecr.io/python-api:0.2.0`
- `mycompanyai.azurecr.io/fastify-service:0.1.0`
- `mycompanyai.azurecr.io/fastify-service:1.0.0`

---

## 5. Avoid Overusing `latest`

You can have `latest` pointing at the current recommended version, but:

- Never rely on `latest` in production manifests.
- Always pin an explicit version (`0.1.0`, `0.2.0`, etc.).
- Use `latest` only for:
  - local experiments
  - dev environments

---

## 6. Practical Flow

1. Implement change.
2. Decide MINOR or PATCH bump.
3. Update environment variables:
   - `PYTHON_API_VERSION`
   - `FASTIFY_SERVICE_VERSION`
4. Build, tag, push.
5. Update Azure deployment to use the new tag.

This keeps deployment history traceable and auditable.