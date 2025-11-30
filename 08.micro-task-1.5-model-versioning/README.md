# 08 – Micro-Task 1.5: Model Versioning

## Overview

This micro-task adds **model versioning** on top of the tuned text classifier.

Instead of overwriting the same `text_classifier.joblib` file on every run, the training script now:

- saves each trained model under a **versioned directory**:  
  `models/<MODEL_VERSION>/text_classifier.joblib`
- writes a `metadata.json` file for each version with:
  - model version
  - timestamp
  - best hyperparameters
  - best cross-validation accuracy
  - hold-out test accuracy
- maintains a **"latest" alias** at:  
  `models/text_classifier.joblib`  
  so that `predict.py` keeps working without modification

This is the first step towards **production-style model lifecycle management**.

---

## Learning Objectives

By completing this micro-task, you will be able to:

- Understand why model versioning is important
- Save models with explicit versions instead of overwriting a single file
- Attach metadata (metrics + hyperparameters) to each version
- Maintain a stable "latest" model path for inference clients (e.g. `predict.py`, APIs)
- Reason about how to roll back or compare different model versions

---

## Tech Stack

- **Language:** Python 3.10+
- **Libraries:** scikit-learn, joblib, re, pathlib, json, datetime

---

## Project Structure

```text
08.micro-task-1.5-model-versioning/
  train.py                 # Training + tuning + versioned saving + metadata
  predict.py               # Loads the 'latest' model for single-text prediction
  requirements.txt         # Python dependencies
  models/
    text_classifier.joblib # Latest model alias (overwritten each run)
    1.0.0/
      text_classifier.joblib  # Versioned model
      metadata.json           # Metrics + params for this version
  README.md
  LEARNING.md              # (Optional) deeper explanation of versioning