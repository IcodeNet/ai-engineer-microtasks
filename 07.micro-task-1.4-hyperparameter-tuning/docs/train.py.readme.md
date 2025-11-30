
---

# **train.py – Text Classification with Hyperparameter Tuning (Beginner-Friendly Guide)**

This script extends the text classifier by adding **hyperparameter tuning** using GridSearchCV. It still classifies text as positive or negative, but now automatically finds the best model settings (hyperparameters) instead of using defaults.

---

# **1. What This Script Does (in plain English)**

The script:

1. Takes a small list of short sentences (some positive, some negative).
2. Cleans the text (lowercase, removes punctuation, normalizes spacing).
3. Converts cleaned sentences from text into numbers (TF-IDF).
4. **Tries different hyperparameter combinations** using GridSearchCV.
5. **Selects the best model** based on cross-validation performance.
6. Trains the best model on a train/test split.
7. Tests the model to see if it learned correctly.
8. Saves the tuned model to a file so it can be used later.

**Key difference from task 06:** Instead of using default hyperparameters, the script automatically finds the best settings by trying multiple combinations.

---

# **2. Important Concepts Explained**

### **A. Hyperparameters**

Hyperparameters are settings you choose **before** training, not learned from data.

**Examples for Logistic Regression:**
- **`C`:** Regularization strength (lower = stronger regularization, simpler model)
- **`max_iter`:** Maximum training iterations (more = more time to learn)

**Default values:**
- `C=1.0` (default)
- `max_iter=1000` (default)

**Why tune them?**
> Defaults work, but they're rarely optimal. Tuning finds settings that perform better on your specific data.

### **B. Grid Search**

Grid Search tries **all combinations** of hyperparameters you specify.

**Example grid:**
```python
param_grid = {
    "clf__C": [0.1, 1.0, 10.0],        # 3 values
    "clf__max_iter": [500, 1000, 2000]  # 3 values
}
```

**Total combinations:** 3 × 3 = 9 combinations

Grid Search will:
1. Train a model with C=0.1, max_iter=500
2. Train a model with C=0.1, max_iter=1000
3. Train a model with C=0.1, max_iter=2000
4. Train a model with C=1.0, max_iter=500
5. ... and so on for all 9 combinations

### **C. GridSearchCV**

`GridSearchCV` combines Grid Search with **Cross-Validation**:

- For each hyperparameter combination:
  - Runs k-fold cross-validation (e.g., 5-fold)
  - Calculates mean CV accuracy
- Selects the combination with **best mean CV accuracy**

**Why CV inside Grid Search?**
> Each combination is evaluated multiple times (via CV), so the "best" choice is more reliable.

### **D. The `clf__` Prefix**

In a pipeline, you access hyperparameters using:
```
<step_name>__<parameter_name>
```

**Example:**
- Pipeline step: `("clf", LogisticRegression(...))`
- To tune `C`: use `"clf__C"`
- To tune `max_iter`: use `"clf__max_iter"`

This tells GridSearchCV which step's parameters to tune.

### **E. Best Model Selection**

After GridSearchCV finishes:
- `grid.best_params_` → Best hyperparameter values
- `grid.best_score_` → Best mean CV accuracy
- `grid.best_estimator_` → The model with best hyperparameters

This model is then used for final training and evaluation.

### **F. Other Concepts**

All concepts from previous tasks still apply:
- **Text cleaning:** Normalizes input
- **TF-IDF:** Converts text to numbers
- **Logistic Regression:** Simple classifier
- **Pipeline:** Combines cleaning, vectorization, classification
- **Cross-validation:** Used internally by GridSearchCV
- **Train/Test Split:** 70% training, 30% testing
- **Accuracy:** How many predictions were correct
- **Saving the Model:** Persists to `models/text_classifier.joblib`

---

# **3. The Data Used**

Same tiny dataset as previous tasks:
- 10 sentences (5 positive, 5 negative)
- Hard-coded inside the script

**Note:** With only 10 examples, hyperparameter tuning may not show dramatic improvements. This is normal for tiny datasets. Real projects with larger datasets see bigger gains from tuning.

---

# **4. What Happens During Training**

Step-by-step:

1. **Load the texts and labels** (positive/negative)
2. **Define hyperparameter grid:**
   ```python
   param_grid = {
       "clf__C": [0.1, 1.0, 10.0],
       "clf__max_iter": [500, 1000, 2000],
   }
   ```
3. **Run GridSearchCV:**
   ```python
   grid = GridSearchCV(
       estimator=base_model,
       param_grid=param_grid,
       cv=5,              # 5-fold cross-validation
       scoring="accuracy"
   )
   grid.fit(X, y)  # Tries all 9 combinations, 5-fold CV each
   ```
   This:
   - Tries 9 combinations
   - Each uses 5-fold CV
   - Total: 9 × 5 = 45 model evaluations
4. **Get best model:**
   ```python
   best_model = grid.best_estimator_
   print("Best params:", grid.best_params_)
   print("Best CV accuracy:", grid.best_score_)
   ```
5. **Split into train/test** (70/30) for final evaluation
6. **Train best model** on training set
7. **Evaluate on test set:**
   ```python
   y_pred = best_model.predict(X_test)
   acc = accuracy_score(y_test, y_pred)
   ```
8. **Save the tuned model:**
   ```python
   joblib.dump(best_model, "models/text_classifier.joblib")
   ```

**Key difference:** Hyperparameter tuning happens **before** final training, finding optimal settings automatically.

---

# **5. Code Structure Explained**

### **Hyperparameter Grid**

```python
param_grid = {
    "clf__C": [0.1, 1.0, 10.0],
    "clf__max_iter": [500, 1000, 2000],
}
```

**What this means:**
- Try C values: 0.1 (strong regularization), 1.0 (default), 10.0 (weak regularization)
- Try max_iter values: 500, 1000, 2000 iterations
- Total: 3 × 3 = 9 combinations

### **GridSearchCV Setup**

```python
grid = GridSearchCV(
    estimator=base_model,    # Pipeline to tune
    param_grid=param_grid,   # Hyperparameters to try
    cv=5,                     # 5-fold cross-validation
    scoring="accuracy"        # Metric to optimize
)
```

**What happens:**
- For each combination, runs 5-fold CV
- Calculates mean CV accuracy
- Picks combination with highest mean

### **Fitting GridSearchCV**

```python
grid.fit(X, y)
```

**This is the slow part:**
- 9 combinations × 5 folds = 45 model trainings
- Takes longer than single training, but finds better settings

### **Using Best Model**

```python
best_model = grid.best_estimator_
best_model.fit(X_train, y_train)  # Final training on train/test split
```

The best model is then used for final evaluation and saving.

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
   - **Hyperparameter tuning output** (may take a few seconds)
   - **Best parameters** found by GridSearchCV
   - **Best CV accuracy** (mean across folds)
   - **Hold-out test evaluation** (classification report, accuracy)
   - **TF-IDF vocabulary sample**
   - Confirmation that tuned model was saved in `models/`

---

# **7. What Changed from Task 06**

| Task 06 | Task 07 |
|---------|--------|
| Manual cross-validation | GridSearchCV (CV built-in) |
| Default hyperparameters | Tuned hyperparameters |
| Single model | Best model from grid search |
| `cross_val_score` | `GridSearchCV` |
| Fixed `C` and `max_iter` | Tries multiple values |

**Benefits of hyperparameter tuning:**
- Automatically finds better settings
- More reliable (uses CV to evaluate each combination)
- Standard practice in ML workflows
- Can improve accuracy significantly on larger datasets

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
```

**Interpretation:**
- **Best params:** C=1.0 (default), max_iter=2000 (more iterations helped)
- **Best CV accuracy:** 60% (mean across 5 folds)
- **Test accuracy:** 66.7% (on hold-out test set)

**Note:** With only 10 examples, the best hyperparameters may be close to defaults. On larger datasets, tuning typically shows bigger improvements.

---

# **9. Hyperparameter Details**

### **C (Regularization Strength)**

- **Lower C (e.g., 0.1):** Stronger regularization → simpler model, less overfitting
- **Higher C (e.g., 10.0):** Weaker regularization → more complex model, risk of overfitting
- **Default:** 1.0

**When to use:**
- Low C: Small datasets, risk of overfitting
- High C: Large datasets, want to capture complex patterns

### **max_iter (Maximum Iterations)**

- **Lower (e.g., 500):** Faster training, may not converge
- **Higher (e.g., 2000):** Slower training, more time to learn
- **Default:** 100

**When to use:**
- If you see "convergence warning" → increase max_iter
- Complex patterns → may need more iterations

---

# **10. What You Can Improve Later**

Future micro-tasks will add:
- Model versioning to track different tuned models
- More hyperparameters to tune (TF-IDF settings, penalty type)
- Randomized search (faster than grid search for large grids)
- More advanced evaluation metrics
- Larger datasets (tuning will show bigger improvements)
- Deployment behind an API

---

