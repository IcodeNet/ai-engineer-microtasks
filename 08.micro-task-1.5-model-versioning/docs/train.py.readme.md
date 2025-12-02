
---

# **train.py – Text Classification with Model Versioning (Beginner-Friendly Guide)**

This script extends the text classifier by adding **model versioning**. It still classifies text as positive or negative with hyperparameter tuning, but now saves models with version numbers and metadata, making it easy to track, compare, and rollback to different model versions.

---

# **1. What This Script Does (in plain English)**

The script:

1. Takes a small list of short sentences (some positive, some negative).
2. Cleans the text (lowercase, removes punctuation, normalizes spacing).
3. Converts cleaned sentences from text into numbers (TF-IDF).
4. Tries different hyperparameter combinations using GridSearchCV.
5. Selects the best model based on cross-validation performance.
6. Trains the best model on a train/test split.
7. Tests the model to see if it learned correctly.
8. **Saves the model with a version number** (e.g., `models/1.0.0/`).
9. **Saves metadata** (version, timestamp, performance metrics, hyperparameters).
10. **Creates a "latest" alias** for easy access.

**Key difference from task 07:** Models are saved with version numbers and metadata, enabling proper model management and tracking.

---

# **2. Important Concepts Explained**

### **A. Model Versioning**

Every time you retrain a model, it should be saved with a version number. This allows you to:
- **Track changes:** Know which model version is deployed
- **Compare performance:** See how different versions perform
- **Rollback:** Go back to a previous version if needed
- **Reproduce:** Know exactly which model was used when

**Version format:** Semantic versioning (e.g., `1.0.0`, `1.1.0`, `2.0.0`)
- **Major (1.0.0):** Breaking changes, major improvements
- **Minor (1.1.0):** New features, improvements
- **Patch (1.0.1):** Bug fixes, small tweaks

### **B. Versioned Directory Structure**

Models are saved in version-specific directories:

```
models/
  1.0.0/
    text_classifier.joblib
    metadata.json
  text_classifier.joblib  (latest alias)
```

**Benefits:**
- Each version has its own folder
- Easy to find specific versions
- Can keep multiple versions simultaneously

### **C. Metadata**

Metadata is information about the model saved alongside it:

**Example metadata:**
```json
{
  "version": "1.0.0",
  "saved_at": "2025-11-30T13:45:00Z",
  "best_params": {"clf__C": 1.0, "clf__max_iter": 2000},
  "best_cv_accuracy": 0.600,
  "test_accuracy": 0.667
}
```

**Why it matters:**
> Metadata lets you compare models without loading them. You can see which version performed best, when it was trained, and what hyperparameters were used.

### **D. Latest Alias**

A "latest" model file is also saved at:
```
models/text_classifier.joblib
```

**Purpose:**
- Easy access for `predict.py` (always uses latest)
- Convenient for development
- Can be updated to point to any version

**Note:** In production, you'd typically load a specific version, not "latest".

### **E. Other Concepts**

All concepts from previous tasks still apply:
- **Text cleaning:** Normalizes input
- **TF-IDF:** Converts text to numbers
- **Logistic Regression:** Simple classifier
- **Pipeline:** Combines cleaning, vectorization, classification
- **Hyperparameter tuning:** GridSearchCV finds best settings
- **Cross-validation:** Used internally by GridSearchCV
- **Train/Test Split:** 70% training, 30% testing
- **Accuracy:** How many predictions were correct

---

# **3. The Data Used**

Same tiny dataset as previous tasks:
- 10 sentences (5 positive, 5 negative)
- Hard-coded inside the script

---

# **4. What Happens During Training**

Step-by-step:

1. **Load the texts and labels** (positive/negative)
2. **Run GridSearchCV** to find best hyperparameters (same as task 07)
3. **Get best model** from grid search
4. **Split into train/test** (70/30) for final evaluation
5. **Train best model** on training set
6. **Evaluate on test set:**
   ```python
   y_pred = best_model.predict(X_test)
   test_accuracy = accuracy_score(y_test, y_pred)
   ```
7. **Create versioned directory:**
   ```python
   version_dir = models_root / MODEL_VERSION  # e.g., models/1.0.0/
   version_dir.mkdir(parents=True, exist_ok=True)
   ```
8. **Save versioned model:**
   ```python
   versioned_model_path = version_dir / "text_classifier.joblib"
   joblib.dump(best_model, versioned_model_path)
   ```
9. **Save metadata:**
   ```python
   metadata = {
       "version": MODEL_VERSION,
       "saved_at": datetime.utcnow().isoformat() + "Z",
       "best_params": best_params,
       "best_cv_accuracy": best_cv_accuracy,
       "test_accuracy": test_accuracy,
   }
   metadata_path = version_dir / "metadata.json"
   metadata_path.write_text(json.dumps(metadata, indent=2))
   ```
10. **Create latest alias:**
    ```python
    latest_path = models_root / "text_classifier.joblib"
    joblib.dump(best_model, latest_path)
    ```

**Key difference:** Models are saved with version numbers and metadata, enabling proper tracking and management.

---

# **5. Code Structure Explained**

### **Model Version Constant**

```python
MODEL_VERSION = "1.0.0"
```

**What this does:**
- Defines the version for this training run
- Should be updated when you make significant changes
- Follows semantic versioning (major.minor.patch)

**When to update:**
- **Major (2.0.0):** Changed model architecture, new features
- **Minor (1.1.0):** Improved hyperparameters, better performance
- **Patch (1.0.1):** Bug fixes, small tweaks

### **Versioned Directory Creation**

```python
models_root = Path("models")
models_root.mkdir(exist_ok=True)

version_dir = models_root / MODEL_VERSION  # e.g., models/1.0.0/
version_dir.mkdir(parents=True, exist_ok=True)
```

**What this does:**
- Creates `models/` directory if it doesn't exist
- Creates version-specific directory (e.g., `models/1.0.0/`)
- `parents=True` creates parent directories if needed
- `exist_ok=True` doesn't error if directory already exists

### **Saving Versioned Model**

```python
versioned_model_path = version_dir / "text_classifier.joblib"
joblib.dump(best_model, versioned_model_path)
```

**Result:**
- Model saved at `models/1.0.0/text_classifier.joblib`
- Each version has its own model file

### **Saving Metadata**

```python
metadata = {
    "version": MODEL_VERSION,
    "saved_at": datetime.utcnow().isoformat() + "Z",
    "best_params": best_params,
    "best_cv_accuracy": best_cv_accuracy,
    "test_accuracy": test_accuracy,
}
metadata_path = version_dir / "metadata.json"
metadata_path.write_text(json.dumps(metadata, indent=2))
```

**What this does:**
- Creates a JSON file with model information
- Includes version, timestamp, hyperparameters, performance
- Saved at `models/1.0.0/metadata.json`

**Why JSON?**
- Human-readable
- Easy to parse programmatically
- Standard format for metadata

### **Latest Alias**

```python
latest_path = models_root / "text_classifier.joblib"
joblib.dump(best_model, latest_path)
```

**What this does:**
- Saves model at `models/text_classifier.joblib`
- Always points to the most recent version
- Convenient for `predict.py` to load without specifying version

---

# **6. How to Run It**

1. Open a terminal in this folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Train the model:
   ```
   python train.py
   ```
4. You should see:
   - **Hyperparameter tuning output**
   - **Best parameters** and **CV accuracy**
   - **Hold-out test evaluation**
   - **Saved versioned model** path (e.g., `models/1.0.0/text_classifier.joblib`)
   - **Saved metadata** path (e.g., `models/1.0.0/metadata.json`)
   - **Updated latest model alias**

---

# **7. What Changed from Task 07**

| Task 07 | Task 08 |
|---------|---------|
| Single model file | Versioned directory structure |
| No metadata | Metadata JSON file |
| No version tracking | Semantic versioning |
| `models/text_classifier.joblib` | `models/1.0.0/text_classifier.joblib` + latest alias |
| No timestamp | Timestamp in metadata |

**Benefits of versioning:**
- Track model history
- Compare different versions
- Rollback to previous versions
- Reproduce results
- Production-ready model management

---

# **8. Understanding the Output**

**Example output:**

```
=== Hyperparameter Tuning with GridSearchCV (5-fold, accuracy) ===
Best params: {'clf__C': 1.0, 'clf__max_iter': 2000}
Best CV accuracy: 0.600

=== Classification Report (hold-out test set) ===
...
Test accuracy (single train/test split): 0.667

Saved versioned model to /path/to/models/1.0.0/text_classifier.joblib
Saved metadata to /path/to/models/1.0.0/metadata.json
Updated latest model alias at /path/to/models/text_classifier.joblib
```

**File structure created:**
```
models/
  1.0.0/
    text_classifier.joblib
    metadata.json
  text_classifier.joblib  (latest)
```

**Metadata example:**
```json
{
  "version": "1.0.0",
  "saved_at": "2025-11-30T13:45:00Z",
  "best_params": {
    "clf__C": 1.0,
    "clf__max_iter": 2000
  },
  "best_cv_accuracy": 0.600,
  "test_accuracy": 0.667
}
```

---

# **9. Model Versioning Best Practices**

### **When to Update Version**

- **Major (2.0.0):** Changed model type, new features, breaking changes
- **Minor (1.1.0):** Better hyperparameters, improved performance, new preprocessing
- **Patch (1.0.1):** Bug fixes, small tweaks, code improvements

### **Versioning Workflow**

1. Train model with current version (e.g., `1.0.0`)
2. Evaluate performance
3. If better, update version (e.g., `1.1.0`) and retrain
4. Compare versions using metadata
5. Deploy best version

### **Using Versions in Production**

**Load specific version:**
```python
model_path = Path(f"models/{version}/text_classifier.joblib")
model = joblib.load(model_path)
```

**Load latest:**
```python
model_path = Path("models/text_classifier.joblib")
model = joblib.load(model_path)
```

**Compare versions:**
```python
# Load metadata from different versions
with open("models/1.0.0/metadata.json") as f:
    v1_metadata = json.load(f)
with open("models/1.1.0/metadata.json") as f:
    v2_metadata = json.load(f)

# Compare test accuracies
print(f"v1.0.0: {v1_metadata['test_accuracy']}")
print(f"v1.1.0: {v2_metadata['test_accuracy']}")
```

---

# **10. What You Can Improve Later**

Future improvements:
- Automatic version bumping based on performance
- Model registry (database of all versions)
- A/B testing between versions
- Model monitoring and drift detection
- Automated rollback on performance degradation
- Integration with MLflow or similar tools
- Deployment pipelines that use versioned models
- API endpoints that can load specific versions

---

