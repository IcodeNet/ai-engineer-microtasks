# 16 – Micro-Task 3.0  
# Azure Container Registry (ACR) Image Publishing

## Overview

This micro-task converts your Fastify gateway and Python model API into **Azure-deployable container images**.  
You will build image artifacts locally and push them to Azure Container Registry (ACR).

These images are the foundation for the next micro-task: **deploying the entire stack to Azure Container Apps**.

---

## Prerequisites

- Azure CLI installed  
- Docker installed  
- Azure subscription  
- An Azure Container Registry (ACR) already created  

Example values:
- ACR name: `mycompanyai`
- Login server: `mycompanyai.azurecr.io`

---

## 1. Set Environment Variables

```
export ACR_NAME="mycompanyai"
export ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"

export PYTHON_API_VERSION="0.1.0"
export FASTIFY_SERVICE_VERSION="0.1.0"
```

---

## 2. Login to Azure + ACR

```
az login
az acr login --name "$ACR_NAME"
```

---

## 3. Build Local Images

```
docker build -t python-api-local ./python-api
docker build -t fastify-service-local ./fastify-service
```

---

## 4. Tag for Azure Registry

```
docker tag python-api-local \
  "$ACR_LOGIN_SERVER/python-api:${PYTHON_API_VERSION}"

docker tag fastify-service-local \
  "$ACR_LOGIN_SERVER/fastify-service:${FASTIFY_SERVICE_VERSION}"
```

---

## 5. Push Images to ACR

```
docker push "$ACR_LOGIN_SERVER/python-api:${PYTHON_API_VERSION}"
docker push "$ACR_LOGIN_SERVER/fastify-service:${FASTIFY_SERVICE_VERSION}"
```

---

## 6. Verify Images in ACR

List repositories:

```
az acr repository list --name "$ACR_NAME" -o table
```

List tags:

```
az acr repository show-tags --name "$ACR_NAME" --repository python-api -o table
az acr repository show-tags --name "$ACR_NAME" --repository fastify-service -o table
```

---

## Output of This Micro-Task

Your Azure Container Registry will now contain:

```
mycompanyai.azurecr.io/python-api:0.1.0
mycompanyai.azurecr.io/fastify-service:0.1.0
```

These are production-ready artifacts Azure can pull during deployment.

---

## Next Micro-Task

Proceed to:

**17 – Deploy Fastify + Python API to Azure Container Apps**

You will use the images created in this micro-task to deploy the entire stack into Azure’s serverless container environment.