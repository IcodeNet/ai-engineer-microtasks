---

# **LEARNING.md – Micro-Task 1.5 (Model Versioning)**

*A Beginner-Friendly, Line-Mapped Guide to Saving ML Models Properly*

---

# **1. Why This Micro-Task Exists**

Up to now, every training run overwrote:

```
models/text_classifier.joblib
```

That's fine early on, but in real AI engineering this is unacceptable because you lose:

- the old model
- the metrics
- the hyperparameters
- when it was created
- how it was trained
- what clients are using
- ability to roll back when something breaks

**Model versioning fixes all of this.**

---

# **2. What We Introduce in This Micro-Task**

This micro-task adds:

### ✅ A version folder per model

```
models/1.0.0/text_classifier.joblib
```

### ✅ Metadata file with all training info

```
models/1.0.0/metadata.json
```

### ✅ A stable "latest" alias

(used by predict.py and future APIs)

```
models/text_classifier.joblib
```

This lets training evolve without breaking inference clients.

---

# **3. What Model Versioning Means (Plain English)**

A model version tells you:

- what the model is
- how it was trained
- how well it performed
- which hyperparameters it used
- when it was saved

This is similar to:

- versioning code (Git tags)
- versioning APIs (v1, v2, v3)
- versioning mobile apps (1.2.0, 1.3.1…)

You now do the same for ML models.

---

# **4. Mapping Concepts to Code (Line-Mapped Explanation)**

## **4.1 Version Constant**

```python
MODEL_VERSION = "1.0.0"
```

Versioning rule-of-thumb:

- **Patch:** 1.0.0 → 1.0.1 (small fix)
- **Minor:** 1.0.0 → 1.1.0 (new hyperparams)
- **Major:** 1.0.0 → 2.0.0 (new dataset or architecture)

---

## **4.2 Version Directory Creation**

```python
version_dir = models_root / MODEL_VERSION
version_dir.mkdir(parents=True, exist_ok=True)
```

Creates:

```
models/1.0.0/
```

---

## **4.3 Saving the Versioned Model**

```python
versioned_model_path = version_dir / "text_classifier.joblib"
joblib.dump(best_model, versioned_model_path)
```

This ensures:

- the previous model is preserved
- reproducibility is possible

---

## **4.4 Metadata File**

```python
metadata = {
    "version": MODEL_VERSION,
    "saved_at": datetime.utcnow().isoformat() + "Z",
    "best_params": best_params,
    "best_cv_accuracy": best_cv_accuracy,
    "test_accuracy": test_accuracy
}
metadata_path.write_text(json.dumps(metadata, indent=2))
```

Metadata captures:

- version number
- timestamp
- hyperparameters
- cross-validation accuracy
- test set accuracy

Everything you need to audit or reproduce the model.

---

## **4.5 Maintain "latest" Alias**

```python
latest_path = models_root / "text_classifier.joblib"
joblib.dump(best_model, latest_path)
```

All inference systems load:

```
models/text_classifier.joblib
```

This file always points to the newest version — but old versions remain in their own folders.

---

# **5. Directory Structure After Running the Task**

After:

```bash
python train.py
```

You get:

```
models/
  text_classifier.joblib        # always latest
  1.0.0/
    text_classifier.joblib      # versioned model
    metadata.json               # training metadata
```

---

# **6. End-to-End Flow Diagram**

```
data
  ↓
hyperparameter tuning (GridSearchCV)
  ↓
best model selected
  ↓
train/test evaluation
  ↓
save model → models/<version>/text_classifier.joblib
  ↓
save metadata → models/<version>/metadata.json
  ↓
copy model → models/text_classifier.joblib (latest)
  ↓
predict.py loads latest
```

---

# **7. Problem → Solution (Your Questions Answered)**

### **Problem 1: Why not overwrite the old model?**

Because you lose:

- auditability
- reproducibility
- rollback safety
- comparison between models

---

### **Problem 2: Why store metadata?**

Without metadata you cannot answer:

- "Which hyperparameters created this model?"
- "How accurate was it?"
- "When was it trained?"

---

### **Problem 3: Why keep a "latest" alias?**

So that:

- `predict.py`
- your future API
- your Fastify microservices

do not need to know the version.

They always load the latest stable model.

---

### **Problem 4: When do I bump the version?**

Use semantic versioning:

- **Patch** = tiny data or code fix
- **Minor** = hyperparameter change
- **Major** = new dataset, architecture, or task

---

# **8. Commands for This Micro-Task**

### **Train + version model:**

```bash
python train.py
```

### **Inspect versioned models:**

```
models/
  1.0.0/
    model + metadata
```

### **Predict using latest:**

```bash
python predict.py "this is great"
```

---

# **9. Summary**

This micro-task teaches you:

- how to version ML models
- how to save model metadata
- how to preserve older models
- how to create a stable inference entry point
- how to think like a production ML engineer

This skill is essential for:

- deploying ML models
- CI/CD for ML
- model registries (S3, Azure Blob, MLflow)
- auditing and reproducibility

You are now ready for:

👉 **09.micro-task-1.6-model-registry-basics**

---
