# ACR_ONBOARDING.md – Onboarding Guide for Engineers

This document explains how a new engineer can quickly understand and use Azure Container Registry (ACR) for this project.

---

## 1. What You Need Installed

- Docker
- Azure CLI (`az`)

Check versions:

- `docker --version`
- `az version`

---

## 2. Know Your Registry

For this project:

- ACR name: `mycompanyai`
- Login server: `mycompanyai.azurecr.io`

If this changes, the values will be updated in:

- `.env.example`
- `commands.sh`

---

## 3. Basic Workflow Summary

1. Login to Azure.
2. Login to ACR.
3. Build images from Dockerfiles.
4. Tag them with the correct ACR names.
5. Push them.
6. Verify.

You can do this manually or use `commands.sh`.

---

## 4. Quick Start Using commands.sh

From the `16 – Micro-Task 3.0 – Azure ACR Publishing` folder:

1. Review `commands.sh` and update:
   - `ACR_NAME`
   - versions if needed

2. Make it executable:

   ```bash
   chmod +x commands.sh