# AI Engineer Micro-Tasks Index

A quick index of all micro-tasks in this repository. Each task is a self-contained lab with its own README, LEARNING guide, code, and docker-compose environment.

---

## **01 – 03: Fastify Service Foundations**

### 01. `01.micro-task-0.1-fastify-service`
- Minimal Fastify HTTP service
- Health and info endpoints

### 02. `02.micro-task-0.2-fastify-predict`
- Fastify service with `/predict` endpoint
- JSON schema validation

### 03. `03.micro-task-0.3-fastify-ml-layer`
- Refactored ML layer module
- Separation of concerns

---

## **04 – 09: Classical ML Foundations & Model Management**

### 04. `04.micro-task-1.1-python-sklearn-baseline`
- TF-IDF + Logistic Regression  
- Introduces basic ML pipeline
- train/test split, accuracy metrics

### 05. `05.micro-task-1.2-text-cleaning`
- Text cleaning preprocessor
- Lowercasing, punctuation removal, stopwords

### 06. `06.micro-task-1.3-cross-validation`
- k-fold cross-validation
- Model evaluation improvements

### 07. `07.micro-task-1.4-hyperparameter-tuning`
- GridSearchCV for hyperparameter optimization
- best_params, best_cv_accuracy

### 08. `08.micro-task-1.5-model-versioning`
- Semantic version folders (1.0.0, 1.1.0…)  
- Saved metadata.json
- Model versioning system

### 09. `09.micro-task-1.6-model-registry-basics`
- Structured registry folder for model artifacts
- ModelRegistry abstraction

---

## **10 – 12: API + Dockerisation**

### 10. `10.micro-task-2.1-model-api-python (start deploying your model behind an API)`
- Python Model API (FastAPI)
- `/predict` and `/health` endpoints
- Model registry integration

### 11. `11.micro-task-2.2-dockerize-python-model-api`
- Dockerfile + containerised inference
- Dockerized FastAPI service

### 12. `12.micro-task-2.3-docker-compose-fastify-python-api`
- Full stack running via docker-compose
- Fastify gateway + Python API

---

## **13 – 15: Production Behaviours**

### 13. `13.micro-task-2.4-logging-request-tracing`
- requestId propagation Fastify → Python
- Structured logging across services

### 14. `14.micro-task-2.5-api-keys-authentication-fastify`
- `X-API-Key` enforcement for protected endpoints
- API key authentication layer

### 15. `15.micro-task-2.6-model-registry-volume-auto-discovery`
- Docker volume for models  
- Python auto-discovers versions  
- Fastify exposes `/admin/models` & `/admin/models/latest`

---

## How to Use This Repository

Each micro-task can be run independently:

```bash
cd "<micro-task-folder>"
docker compose up --build