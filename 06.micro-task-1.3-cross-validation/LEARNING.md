```
06.micro-task-1.3-cross-validation/LEARNING.md
```

---

# **LEARNING.md – Micro-Task 1.3 (Cross-Validation)**

*A Beginner-Friendly, Line-Mapped Guide to More Reliable Model Evaluation*

This micro-task introduces **cross-validation**, one of the most important ideas in machine learning.

By the end of this task, you will understand:

* What cross-validation is
* Why your simple train/test split is not enough
* How k-fold cross-validation works
* How scikit-learn performs it
* How it maps directly to your code
* How to interpret cross-validation scores
* How cross-validation avoids misleading results
* How to extend your code safely

This document is deliberately beginner-friendly while still mapping to the exact lines of Python code used in this micro-task.

---

# **1. Why Do We Need Cross-Validation? (Simple Explanation)**

Until now, you've used a **single** train/test split:

```
70% → train  
30% → test
```

But this can give **unstable** results when the dataset is small (like in your micro-task).

Example problems:

* The test set may accidentally contain too many positives
* Or too many negatives
* Or sentences that are unusually easy/hard
* A different random split may give very different accuracy

In simple terms:

> A single train/test split can mislead you.

Cross-validation fixes this problem.

---

# **2. What Is Cross-Validation? (Plain English)**

Cross-validation means:

> “Test the model several times on different slices of the data.”

Most common form: **k-fold cross-validation**.

Example: 5-fold cross-validation:

1. Split data into **5** equal parts
2. Train on 4 parts, test on the 5th
3. Repeat 5 times (each part becomes the test once)
4. Average the results

This gives you a **much more reliable** picture of model performance.

---

# **3. Why It’s Better Than One Train/Test Split**

Cross-validation:

* Uses **all data** for both training and testing (at different times)
* Reduces randomness
* Gives more stable accuracy
* Helps detect overfitting
* Works extremely well for small datasets

This is why almost all ML engineers use cross-validation when comparing models.

---

# **4. The Code You Added (Line-Mapped Explanation)**

Your new cross-validation code goes into `train.py`, usually **after building the model** but **before fitting** with `.fit(...)`.

Here is the exact block:

```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("Cross-validation scores:", cv_scores)
print("Mean accuracy:", cv_scores.mean())
```

Let’s break this down:

---

## **4.1 Importing the Function**

```python
from sklearn.model_selection import cross_val_score
```

This brings in scikit-learn's built-in cross-validation helper.

---

## **4.2 Calling cross_val_score()**

```python
cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
```

### What each parameter means:

* **model**
  The pipeline you created earlier (`TF-IDF + LogisticRegression`)

* **X**
  Your list of text sentences
  → This replaces the train/test split

* **y**
  Labels (“positive” or “negative”)

* **cv=5**
  Perform **5-fold cross-validation**

* **scoring="accuracy"**
  Evaluate accuracy each time

### What this function does internally:

It automatically:

1. Splits data into 5 folds
2. Trains the model 5 times
3. Tests on a different fold each time
4. Collects all 5 accuracy scores

---

## **4.3 Printing Results**

```python
print("Cross-validation scores:", cv_scores)
print("Mean accuracy:", cv_scores.mean())
```

Typical output might look like:

```
Cross-validation scores: [0.5 0.5 1.0 0.0 0.5]
Mean accuracy: 0.5
```

This gives you a much clearer idea of performance than a single split.

---

# **5. Where This Fits in Your Code**

### BEFORE (original workflow)

```
get_data() → train_test_split → model.fit → evaluate once → save model
```

### AFTER (cross-validation workflow)

```
get_data()  
→ cross_val_score (5 evaluations)  
→ train_test_split OR full training  
→ model.fit  
→ save model
```

Cross-validation is used **only for evaluation**, not for final training.

---

# **6. How to Run This Micro-Task**

From the root of the micro-task folder:

```bash
python train.py
```

This will print:

* 5 cross-validation accuracy scores
* the average accuracy
* your usual train/test results
* your saved model

---

# **7. Understanding Your Cross-Validation Output (Example)**

Imagine you see:

```
Cross-validation scores: [0.5 0.5 1.0 0.0 0.5]
Mean accuracy: 0.5
```

Interpretation:

* Model sometimes performs well (1.0)
* Sometimes fails (0.0)
* Usually around 0.5

This is **expected** with tiny datasets.
The important thing:
the model is **not stable**, confirming you need more data or more processing.

---

# **8. Problem → Solution Section (Your Likely Questions)**

### **Problem 1: “Why do scores vary so much?”**

**Solution:**
With tiny data, small differences in the test fold can change accuracy drastically.
Cross-validation shows you this instability — which is **good information**.

---

### **Problem 2: “Do we still need train_test_split?”**

**Solution:**
Yes.
Cross-validation is for *evaluation*.
Later, you still train once on the full training set (or full dataset).

---

### **Problem 3: “Why average the scores?”**

**Solution:**
Each fold tests different data.
The average is the most reliable performance estimate.

---

### **Problem 4: “Does cross-validation save the model?”**

**Solution:**
No.
It only evaluates.
You still call:

```python
model.fit(X_train, y_train)
```

to train the final version.

---

### **Problem 5: “Should I use cross-validation in real projects?”**

**Solution:**
Almost always yes — especially during model selection or tuning.

---

# **9. Commands Cheat Sheet**

### Run training with cross-validation:

```bash
python train.py
```

### Output will include:

```
Cross-validation scores: [...]
Mean accuracy: ...
```

### Then normal training continues and the model is saved:

```
models/text_classifier.joblib
```

---

# **10. End-to-End Flow Diagram for Cross-Validation**

```
raw text + labels
        ↓
cross_val_score()
        ↓  (5x: split → train → test → score)
  [scores array]
        ↓
mean accuracy
        ↓
train_test_split()
        ↓
final model.fit()
        ↓
save model
        ↓
predict.py
```

---

# **11. Summary**

In this micro-task you learned:

* Why a single train/test split is unreliable
* What cross-validation is
* How k-fold cross-validation works
* How to implement it in scikit-learn
* How to interpret varying accuracy scores
* How cross-validation fits into the training pipeline
* How to run and verify your results

This knowledge is essential for any ML engineer.
Cross-validation is one of the core tools used to select and validate models in real projects.


# Next Steps

After this micro-task, you are ready to:

* Tune the model with hyperparameter search (e.g. GridSearchCV)
* Start thinking about model versioning
* Prepare for deploying the model behind an API


---
 