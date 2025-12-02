# 17 – Micro-Task 3.1  
# Deploy Fastify + Python API to Azure Container Apps  
**LEARNING.md**

## 1. Purpose of This Micro-Task

Micro-Task 16 published two images to Azure Container Registry:

- `python-api:<version>`
- `fastify-service:<version>`

This micro-task deploys those images into **Azure Container Apps (ACA)**.

ACA becomes the platform runtime for your system:

- Pulls images from ACR
- Secures environment variables and secrets
- Provides HTTP ingress
- Handles scaling
- Provides basic logging and diagnostics

This micro-task covers **Platform / DevOps responsibilities**.

---

## 2. What You Will Implement

You will:

1. Create a Resource Group  
2. Create a Container Apps Environment  
3. Deploy the Python API container  
4. Retrieve its public URL  
5. Deploy the Fastify gateway container  
6. Inject a secret containing the API key  
7. Inject an environment variable pointing to the Python API URL  
8. Test the full end-to-end workflow

No code changes. Only deployment.

---

## 3. Architecture Before and After

### Before
Local-only system:

```
fastify-service  <->  python-api
(local docker-compose)
```

### After
Cloud-hosted microservices:

```
Client → Fastify Gateway (ACA) → Python API (ACA)
        pulls image from ACR   pulls image from ACR
```

Both run inside:

- One Resource Group  
- One ACA Environment  

---

## 4. New Azure Concepts Introduced

### Resource Group  
Logical grouping of Azure resources.

### Container Apps Environment  
Shared networking and configuration boundary for multiple container apps.

### Container App  
Managed container execution unit:

- Pulls image from ACR  
- Exposes HTTP ingress  
- Supports autoscaling  

### Secrets  
Secure values injected into containers as environment variables.

### Ingress  
The method by which an app becomes reachable:

- External = public URL  
- Internal = only reachable within environment  

For simplicity, both apps are external in this micro-task.

---

## 5. Problem → Solution Mapping

### Problem: “How do I run containers in Azure?”
Solution: Deploy each service as a Container App using images from ACR.

### Problem: “How does Fastify find the Python API in Azure?”
Solution: Retrieve the Python API’s Container App URL and inject it as `PYTHON_API_BASE_URL`.

### Problem: “How do I secure the API key?”
Solution: Store it as a Container App secret and expose it through an environment variable.

### Problem: “How do I scale?”
Solution: Set min and max replica counts in ACA definitions.

---

## 6. Deployment Flow You Will Implement

1. Create Resource Group  
2. Create Container Apps Environment  
3. Deploy Python API container  
4. Get its FQDN (URL)  
5. Deploy Fastify gateway container  
6. Inject API key secret  
7. Update Fastify environment variables  
8. Test `/health` and `/predict`  
9. Check logs

This produces a working cloud deployment.

---

## 7. Outputs of This Micro-Task

You will end up with:

- `python-api-app` running in Azure  
- `fastify-gateway-app` running in Azure  
- End-to-end prediction via public API  
- Log visibility using ACA commands  
- Basic scaling configuration  

These components become the starting point for:

- private networking  
- managed identities  
- VNET integration  
- logging to Log Analytics  
- CI/CD pipelines  
- blue/green deployment  

---

## 8. Next Steps

After this:

- Micro-Task 18 can harden security (private Python API + VNET)
- Micro-Task 19 can enable managed identities for ACR pulls
- Micro-Task 20 can add Log Analytics monitoring
- Micro-Task 21 can introduce CI/CD pipelines