#!/usr/bin/env bash
#
# commands.sh - Helper script for Micro-Task 3.0 (Azure ACR Publishing)
#
# This script assumes:
# - Azure CLI is installed
# - Docker is installed
# - You have already created an Azure Container Registry (ACR)
#
# Usage (from this folder):
#   chmod +x commands.sh
#   ./commands.sh
#
# Or run individual sections by copying commands.

set -euo pipefail

echo "=== Micro-Task 3.0 – Azure ACR Publishing ==="

# --------------------------------------------------------------------
# 1. CONFIGURATION (EDIT THESE FOR YOUR ENVIRONMENT)
# --------------------------------------------------------------------

# ACR name (no domain, just the registry resource name)
export ACR_NAME="mycompanyai"

# Login server is usually: <ACR_NAME>.azurecr.io
export ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"

# Image versions (semantic versioning)
export PYTHON_API_VERSION="0.1.0"
export FASTIFY_SERVICE_VERSION="0.1.0"

echo "ACR_NAME          = $ACR_NAME"
echo "ACR_LOGIN_SERVER  = $ACR_LOGIN_SERVER"
echo "PYTHON_API_VERSION = $PYTHON_API_VERSION"
echo "FASTIFY_SERVICE_VERSION = $FASTIFY_SERVICE_VERSION"

# --------------------------------------------------------------------
# 2. LOGIN TO AZURE AND ACR
# --------------------------------------------------------------------

echo
echo ">>> Logging into Azure..."
az login

echo
echo ">>> Logging into ACR..."
az acr login --name "$ACR_NAME"

# --------------------------------------------------------------------
# 3. BUILD LOCAL IMAGES
# --------------------------------------------------------------------

echo
echo ">>> Building local images..."

# Build python-api image (expects ./python-api/Dockerfile)
docker build -t python-api-local ./python-api

# Build fastify-service image (expects ./fastify-service/Dockerfile)
docker build -t fastify-service-local ./fastify-service

# --------------------------------------------------------------------
# 4. TAG IMAGES FOR ACR
# --------------------------------------------------------------------

echo
echo ">>> Tagging images for ACR..."

docker tag python-api-local \
  "${ACR_LOGIN_SERVER}/python-api:${PYTHON_API_VERSION}"

docker tag fastify-service-local \
  "${ACR_LOGIN_SERVER}/fastify-service:${FASTIFY_SERVICE_VERSION}"

echo "Tagged images:"
echo "  ${ACR_LOGIN_SERVER}/python-api:${PYTHON_API_VERSION}"
echo "  ${ACR_LOGIN_SERVER}/fastify-service:${FASTIFY_SERVICE_VERSION}"

# --------------------------------------------------------------------
# 5. PUSH IMAGES TO ACR
# --------------------------------------------------------------------

echo
echo ">>> Pushing images to ACR..."

docker push "${ACR_LOGIN_SERVER}/python-api:${PYTHON_API_VERSION}"
docker push "${ACR_LOGIN_SERVER}/fastify-service:${FASTIFY_SERVICE_VERSION}"

# --------------------------------------------------------------------
# 6. VERIFY IN ACR
# --------------------------------------------------------------------

echo
echo ">>> Verifying repositories in ACR..."

az acr repository list --name "$ACR_NAME" -o table

echo
echo ">>> Tags for python-api:"
az acr repository show-tags --name "$ACR_NAME" --repository python-api -o table || true

echo
echo ">>> Tags for fastify-service:"
az acr repository show-tags --name "$ACR_NAME" --repository fastify-service -o table || true

echo
echo "=== Done. Images should now be available in ACR ==="
echo "python-api:       ${ACR_LOGIN_SERVER}/python-api:${PYTHON_API_VERSION}"
echo "fastify-service:  ${ACR_LOGIN_SERVER}/fastify-service:${FASTIFY_SERVICE_VERSION}"