
# LEARNING.md – Micro-Task 1.6 (Model Registry Basics)

*A beginner-friendly guide to understanding & building a model registry.*

---

# 1. What Is a Model Registry?

A **model registry** is a central place to store:

- model versions  
- metadata  
- performance metrics  
- training timestamps  
- production/staging aliases  

Instead of scattering models all over your repo, a registry creates **order and traceability**.

Real registries include:

- Azure Machine Learning Registry  
- MLflow Model Registry  
- AWS S3 + metadata  
- HuggingFace Hub  

In this micro-task, you build a **local registry abstraction**, which behaves like those but stores data in:

registry/

---

# 2. Why Do We Need a Registry?

## Without a registry:
You easily get:

- “Which model is this?”
- “Who trained this?”
- “What data was used?”
- “Can we roll back?”
- “Which version is in production?”
- “Where is the metadata?”

## With a registry:
You get:

- Version tracking  
- Reproducibility  
- Rollback safety  
- Clear promotion workflow (e.g., `latest`, `production`)  
- Centralised storage for all services  

This is the difference between **a script** and **an ML system**.

---

# 3. What We Build in This Micro-Task

We implement a local registry with the following layout:

    registry/
    versions/
    1.0.0/
    model.joblib
    metadata.json

    1.1.0/
    model.joblib
    metadata.json

    latest/
    model.joblib
    metadata.json

### Versioned models:
Stored under `registry/versions/<version>/`.

### “Latest” model:
Stored under `registry/latest/`.

Your prediction system will always load `latest` unless you specify a version manually.

---

# 4. Mapping Concepts to Code

---

## 4.1 Saving a model to the registry

```python
registry.save_model(MODEL_VERSION, best_model, metadata)
```

This automatically:
	•	creates the version directory
	•	writes model + metadata
	•	updates the “latest” alias

⸻

### 4.2 Loading the latest model in predict.py

model, metadata = registry.get_latest_model()

This keeps your API consistent even as the underlying version changes.

⸻

### 4.3 Loading a specific version

model, metadata = registry.get_model("1.0.0")

This allows:
	•	debugging
	•	regression testing
	•	A/B testing

⸻

### 5. Problem → Solution Section

⸻

### Problem:

“I might retrain a model many times. How do I track them?”

Solution:
The registry creates:

registry/versions/<version>/

Each version stays forever.

⸻

### Problem:

“How do APIs know which model to load?”

Solution:
Prediction systems load:

registry/latest/

The registry updates this automatically.

⸻

### Problem:

“What if I want to roll back?”

Solution:

registry.get_model("1.0.0")

Load any past version instantly.

⸻

### Problem:

“How do I keep metadata consistent?”

Solution:
Each model version has:

metadata.json

with:
	•	hyperparameters
	•	CV score
	•	test score
	•	timestamp
	•	version

⸻

## 6. Commands

Train and register a model:

python train.py

Predict with latest model:

python predict.py "this is great"

Predict using specific version:

python predict.py "this is great" --version 1.0.0


⸻

## 7. Summary

You now understand:
	•	what a model registry is
	•	why MLOps needs it
	•	how to version and store models
	•	how to track metadata
	•	how to maintain a stable interface for inference clients

This micro-task sets you up for:
	•	cloud registries
	•	CI/CD for ML
	•	production deployments
	•	staging → production promotion flows



You now have:

✔ Local model registry

✔ Versioned models

✔ Metadata tracking

✔ Latest alias

✔ Load specific version

✔ Prepare for cloud registries

This is now real ML engineering, not just running scripts.

# Next:
10.micro-task-2.1-model-api-python — turning your model into a real API.

 

