
# 09 – Micro-Task 1.6: Model Registry Basics

## Overview

In this micro-task, we introduce a **local model registry** abstraction.

Instead of saving models directly to:

`models//
models/text_classifier.joblib`

…the training script now saves models using a **registry client**, and the prediction script loads models **through the registry client**.

This prepares you for moving to a real cloud registry later (Azure Blob Storage, AWS S3, MLflow).

---

## Goals

- Understand why ML models should be stored in a registry, not in random local folders.
- Create a reusable `ModelRegistry` class.
- Save:
  - versioned models
  - metadata
  - a “latest” alias
- Load:
  - the latest model
  - or a specific version
- Maintain backward compatibility with your existing flows.

---

## What You Build in This Micro-Task

### New file:

`registry.py`

Defines a simple local model registry:

- `save_model(version, model, metadata)`
- `get_latest_model()`
- `get_model(version)`
- maintains directory structure:

registry/
versions/
1.0.0/
model.joblib
metadata.json
latest/
model.joblib
metadata.json

### Updated files:

- `train.py` → stores models using the registry
- `predict.py` → loads models using the registry
- `README.md`
- `LEARNING.md`

---

## How to Use

### Train and register a model:

```bash
python train.py

Predict using the latest model:

python predict.py "this is great"

Predict using a specific model version:

python predict.py "this is great" --version 1.0.0


⸻

Next Steps

After this micro-task, the next evolution is:
	•	Connecting the registry to the cloud (Azure Blob / S3)
	•	Serving models via API
	•	Model promotion workflows: staging → production

