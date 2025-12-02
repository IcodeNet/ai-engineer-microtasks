# 17 – Micro-Task 3.1  
# Deploy Fastify + Python API to Azure Container Apps  
**README.md**

## Overview

This micro-task deploys:

- `python-api`  
- `fastify-service`  

from Azure Container Registry (ACR) into **Azure Container Apps (ACA)**.

You will create:

- A Resource Group  
- A Container Apps Environment  
- A Python API Container App  
- A Fastify Gateway Container App  

You will inject:

- `API_KEYS` secret  
- `PYTHON_API_BASE_URL` environment variable  

Finally, you will test end-to-end predictions through the gateway.

---

## 1. Environment Variables

Update these values to your environment.

```bash
export RG_NAME="bth-aiapps-rg"
export LOCATION="westeurope"

export ACR_NAME="mycompanyai"
export ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"

export ENV_NAME="bth-aiapps-env"

export PYTHON_API_IMAGE="${ACR_LOGIN_SERVER}/python-api:0.1.0"
export FASTIFY_IMAGE="${ACR_LOGIN_SERVER}/fastify-service:0.1.0"

export FASTIFY_API_KEY="test-key-1"
```

---

## 2. Create Resource Group

```bash
az group create \
  --name "$RG_NAME" \
  --location "$LOCATION"
```

---

## 3. Create Container Apps Environment

```bash
az containerapp env create \
  --name "$ENV_NAME" \
  --resource-group "$RG_NAME" \
  --location "$LOCATION"
```

---

## 4. Deploy Python API Container App

```bash
az containerapp create \
  --name python-api-app \
  --resource-group "$RG_NAME" \
  --environment "$ENV_NAME" \
  --image "$PYTHON_API_IMAGE" \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 2 \
  --registry-server "$ACR_LOGIN_SERVER" \
  --cpu 0.5 \
  --memory 1.0Gi
```

Get its public URL:

```bash
export PYTHON_API_BASE_URL="https://$(az containerapp show \
  --name python-api-app \
  --resource-group "$RG_NAME" \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv)"
```

---

## 5. Deploy Fastify Gateway Container App

Create the app:

```bash
az containerapp create \
  --name fastify-gateway-app \
  --resource-group "$RG_NAME" \
  --environment "$ENV_NAME" \
  --image "$FASTIFY_IMAGE" \
  --target-port 3000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --registry-server "$ACR_LOGIN_SERVER" \
  --cpu 0.5 \
  --memory 1.0Gi \
  --env-vars \
    PYTHON_API_BASE_URL="$PYTHON_API_BASE_URL" \
  --secrets \
    api-keys="$FASTIFY_API_KEY"
```

Bind secret to environment variable:

```bash
az containerapp update \
  --name fastify-gateway-app \
  --resource-group "$RG_NAME" \
  --set-env-vars API_KEYS=secretref:api-keys
```

---

## 6. Get Fastify Gateway URL

```bash
export FASTIFY_URL="https://$(az containerapp show \
  --name fastify-gateway-app \
  --resource-group "$RG_NAME" \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv)"
```

---

## 7. Test End-to-End

### Health

```bash
curl "$FASTIFY_URL/health"
```

### Predict (API-key protected)

```bash
curl -X POST "$FASTIFY_URL/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $FASTIFY_API_KEY" \
  -d '{"text":"this is great"}'
```

---

## 8. Logs

Fastify:

```bash
az containerapp logs show \
  --name fastify-gateway-app \
  --resource-group "$RG_NAME" \
  --follow
```

Python API:

```bash
az containerapp logs show \
  --name python-api-app \
  --resource-group "$RG_NAME" \
  --follow
```

---

## 9. Clean Up

```bash
az group delete \
  --name "$RG_NAME" \
  --yes \
  --no-wait
```

---

## Result

You now have:

- A fully running Fastify gateway in Azure  
- A fully running Python model API in Azure  
- Secure secret handling  
- End-to-end prediction flow  
- Scalable services ready for next steps  

This completes the Platform / DevOps deployment path for this stage.