# Micro-Task 3.0 – Azure Container Registry (ACR) Image Publishing  
**LEARNING.md**

## 1. Purpose of This Micro-Task

Up to now, your Fastify gateway and Python model API have only run locally using docker-compose.  
Azure cannot access these containers directly from your laptop.  
All cloud deployment flows require images to live in a **container registry**.

This micro-task teaches you how to:

- Build production Docker images for both services  
- Tag them using semantic versions  
- Authenticate with Azure Container Registry (ACR)  
- Push the images into ACR  
- Verify the registry contains the correct versions  

This is the first real **cloud-readiness** step.

---

## 2. What This Micro-Task Adds

This micro-task adds:

- A reproducible way to build container images  
- Correct image tagging (“registry/repository:version”)  
- ACR authentication  
- ACR publishing workflow  
- Versioned artifacts ready for deployment  

It does NOT deploy anything yet — that is Micro-Task 17.

---

## 3. Architecture Context

### Before (local only)
```
docker-compose builds locally  
docker-compose runs locally  
Azure cannot see anything
```

### After (cloud-ready)
```
Local Docker build  
→ docker tag  
→ docker push  
→ Azure Container Registry  
→ Azure Container Apps / AKS (next micro-task)
```

### ASCII Flow
```
[Local Docker] → [Tagged Image] → [Push] → [ACR Registry] → (Future) Azure Compute
```

---

## 4. Key Terms You Must Understand

**Azure Container Registry (ACR)**  
Private registry where Azure pulls all images.

**Login Server**  
Hostname of your registry, e.g.  
`mycompanyai.azurecr.io`

**Repository**  
Folder inside registry (python-api, fastify-service)

**Image**  
Built container snapshot (your code + OS + dependencies)

**Tag**  
A semantic version label (0.1.0, 0.2.0, etc.)

---

## 5. Problem → Solution Breakdown

**Problem:** Azure cannot use local images.  
**Solution:** Push images to ACR and reference them by tag.

**Problem:** Hard to track versions when deploying multiple services.  
**Solution:** Use semantic versioning for image tags.

**Problem:** CI/CD needs predictable artifacts.  
**Solution:** ACR becomes the single source of truth.

---

## 6. What You Will Produce

After this micro-task, your ACR will contain:

```
mycompanyai.azurecr.io/python-api:0.1.0
mycompanyai.azurecr.io/fastify-service:0.1.0
```

These become real deployable units.

---

## 7. Step-by-Step Learning Details

### Step 1 — Authenticate

```
az login
az acr login --name <ACR_NAME>
```

### Step 2 — Build the images locally

```
docker build -t python-api-local ./python-api
docker build -t fastify-service-local ./fastify-service
```

### Step 3 — Tag the images for ACR

```
docker tag python-api-local \
  <ACR_LOGIN_SERVER>/python-api:0.1.0

docker tag fastify-service-local \
  <ACR_LOGIN_SERVER>/fastify-service:0.1.0
```

### Step 4 — Push to ACR

```
docker push <ACR_LOGIN_SERVER>/python-api:0.1.0
docker push <ACR_LOGIN_SERVER>/fastify-service:0.1.0
```

### Step 5 — Verify

```
az acr repository list --name <ACR_NAME> -o table
```

---

## 8. Risks and Real-World Issues

- Wrong registry name → image goes nowhere  
- Using “latest” → unpredictable deployments  
- Forgetting to log into ACR → push denied  
- Tag mismatch → production pulls the wrong image  

This micro-task teaches the correct patterns.

---

## 9. What This Enables Next

Micro-Task 17 will deploy these images into:

- Azure Container Apps  
- with environment variables  
- secrets  
- scaling  
- health checks  
- logging  

Your system becomes a true cloud microservice architecture.

---

## 10. Summary

This micro-task delivers:

- Cloud-ready docker images  
- Stored in Azure Container Registry  
- Versioned and validated  
- Ready for deployment in the next micro-task  

You now have production-grade artifacts Azure can pull.