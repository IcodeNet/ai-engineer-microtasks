
---

# **train.py – Text Classification with Cross-Validation (Beginner-Friendly Guide)**

This script extends the text classifier by adding **k-fold cross-validation** for more reliable model evaluation. It still classifies text as positive or negative, but now evaluates the model multiple times on different data splits to get a more honest performance estimate.

---

# **1. What This Script Does (in plain English)**

The script:

1. Takes a small list of short sentences (some positive, some negative).
2. Cleans the text (lowercase, removes punctuation, normalizes spacing).
3. Converts cleaned sentences from text into numbers (TF-IDF).
4. **Runs cross-validation** to evaluate the model on multiple splits.
5. Trains a model on a single train/test split.
6. Tests the model to see if it learned correctly.
7. Saves the trained model to a file so it can be used later.

**Key difference from task 05:** The model is evaluated using **cross-validation** before final training, giving a more reliable performance estimate.

---

# **2. Important Concepts Explained**

### **A. Cross-Validation (k-fold)**

A single train/test split can be misleading, especially with small datasets. Cross-validation evaluates the model multiple times on different splits.

**How it works:**
1. Split data into **k folds** (e.g., 5 folds)
2. For each fold:
   - Train on 4 folds
   - Test on the remaining 1 fold
3. Collect all 5 test scores
4. Calculate **mean** and **standard deviation**

**Example with 5-fold CV:**
- Fold 1: Train on folds 2-5, test on fold 1 → score: 0.6
- Fold 2: Train on folds 1,3-5, test on fold 2 → score: 0.7
- Fold 3: Train on folds 1-2,4-5, test on fold 3 → score: 0.5
- Fold 4: Train on folds 1-3,5, test on fold 4 → score: 0.65
- Fold 5: Train on folds 1-4, test on fold 5 → score: 0.7

**Mean accuracy:** 0.63  
**Standard deviation:** 0.08

**Why it's better:**
> Cross-validation gives you multiple performance estimates, so you see how stable your model is across different data splits.

### **B. Mean and Standard Deviation**

- **Mean:** Average of all CV scores (the typical performance)
- **Standard deviation:** How much scores vary (lower = more stable)

**Interpretation:**
- Mean = 0.63, std = 0.08 → Model performs around 63% with small variation
- Mean = 0.63, std = 0.25 → Model performs around 63% but very unstable

### **C. Two-Stage Evaluation**

This script does **two evaluations**:

1. **Cross-validation** (on full dataset):
   - More reliable estimate
   - Shows stability across splits
   - Uses `cross_val_score()`

2. **Single train/test split** (hold-out test):
   - Concrete final evaluation
   - Used for final model selection
   - Same as previous tasks

**Why both?**
- CV tells you how the model performs on average
- Hold-out test gives you a concrete final score

### **D. Other Concepts**

All concepts from previous tasks still apply:
- **Text cleaning:** Normalizes input
- **TF-IDF:** Converts text to numbers
- **Logistic Regression:** Simple classifier
- **Pipeline:** Combines cleaning, vectorization, classification
- **Train/Test Split:** 70% training, 30% testing
- **Accuracy:** How many predictions were correct
- **Saving the Model:** Persists to `models/text_classifier.joblib`

---

# **3. The Data Used**

Same tiny dataset as previous tasks:
- 10 sentences (5 positive, 5 negative)
- Hard-coded inside the script

**Note:** With only 10 examples, cross-validation scores will vary a lot. This is normal for tiny datasets. Real projects use thousands of examples.

---

# **4. What Happens During Training**

Step-by-step:

1. **Load the texts and labels** (positive/negative)
2. **Run cross-validation** (5-fold):
   ```python
   cv_scores = cross_val_score(cv_model, X, y, cv=5, scoring="accuracy")
   ```
   This:
   - Splits data into 5 folds
   - Trains and tests 5 times
   - Returns 5 accuracy scores
3. **Print CV results:**
   - Individual scores
   - Mean accuracy
   - Standard deviation
4. **Split into train/test** (70/30) for final evaluation
5. **Build and train model** on training set
6. **Evaluate on test set:**
   ```python
   y_pred = model.predict(X_test)
   acc = accuracy_score(y_test, y_pred)
   ```
7. **Save the model:**
   ```python
   joblib.dump(model, "models/text_classifier.joblib")
   ```

**Key difference:** Cross-validation happens **before** the final train/test split, giving you a more reliable performance estimate.

---

# **5. Code Structure Explained**

### **Cross-Validation Section**

```python
cv_model = build_model()

cv_scores = cross_val_score(
    cv_model,
    X,           # Full dataset (not split yet)
    y,           # Full labels
    cv=5,        # 5 folds
    scoring="accuracy"
)

print("CV scores:", cv_scores)
print("CV mean accuracy:", cv_scores.mean())
print("CV std:", cv_scores.std())
```

**What happens:**
- `cross_val_score` automatically splits data into 5 folds
- Trains 5 models (one per fold)
- Tests each on its held-out fold
- Returns array of 5 scores

### **Final Train/Test Split**

After CV, we still do a normal split for final evaluation:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
```

This gives us a concrete hold-out test set for final evaluation.

### **Model Training**

Same as before:
```python
model = build_model()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

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
   - **Cross-validation scores** (5 individual scores)
   - **CV mean accuracy** and **standard deviation**
   - **Hold-out test evaluation** (classification report, accuracy)
   - **TF-IDF vocabulary sample**
   - Confirmation that a file was saved in `models/`

---

# **7. What Changed from Task 05**

| Task 05 | Task 06 |
|---------|--------|
| Single train/test split | Cross-validation + train/test split |
| One evaluation | Two evaluations (CV + hold-out) |
| No stability measure | Mean + std deviation from CV |
| `train_test_split` only | `cross_val_score` + `train_test_split` |

**Benefits of cross-validation:**
- More reliable performance estimate
- Shows model stability across different splits
- Better for small datasets (uses all data for evaluation)
- Standard practice in ML evaluation

---

# **8. Understanding the Output**

**Example output:**

```
=== Cross-validation (5-fold, accuracy) ===
CV scores: [0.5 0.5 0.5 1.0 0.5]
CV mean accuracy: 0.6
CV std: 0.2

=== Classification Report (hold-out test set) ===
...
Test accuracy (single train/test split): 0.667
```

**Interpretation:**
- CV scores vary (0.5 to 1.0) because dataset is tiny
- Mean CV accuracy: 60%
- Standard deviation: 0.2 (20%) — high variation is normal for small datasets
- Hold-out test accuracy: 66.7% (one specific split)

**Note:** With only 10 examples, scores will fluctuate. This is expected and demonstrates why cross-validation is useful — it shows the range of possible performance.

---

# **9. What You Can Improve Later**

Future micro-tasks will add:
- Hyperparameter tuning (using CV internally)
- Model versioning to track different versions
- More advanced evaluation metrics
- Larger datasets (CV will be more stable)
- Deployment behind an API

---

