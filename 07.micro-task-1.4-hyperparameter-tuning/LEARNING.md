```
07.micro-task-1.4-hyperparameter-tuning/LEARNING.md
```

It follows the exact tone, clarity, and structure of the previous micro-task documents.

---

# **LEARNING.md – Micro-Task 1.4 (Hyperparameter Tuning)**

*A Beginner-Friendly, Line-Mapped Guide to Improving Model Performance Using Grid Search*

This micro-task teaches you how to improve your model by tuning its **hyperparameters** — the adjustable settings that control how your model learns.

By the end of this task, you will understand:

* What hyperparameters are
* Why they matter
* What Grid Search does
* How scikit-learn tries different combinations
* How this fits into your current pipeline
* How to interpret tuning results
* How tuning connects to cross-validation
* Problems beginners face → and their clear solutions

This document is written to be **completely beginner-safe**, while still pointing to the **exact lines of code** used in this micro-task.

---

# **1. What Are Hyperparameters? (Plain English)**

When you train a model, there are two types of parameters:

### **A) Model parameters**

These are learned from data automatically.

Example:
The Logistic Regression weights inside your model.

### **B) Hyperparameters**

These are settings **you choose**, not the model.

Examples:

* how many iterations to run (`max_iter`)
* how strong regularisation is (`C`)
* what penalty type to use (`l2`, `l1`)
* how TF-IDF creates features (`min_df`, `max_df`, `ngram_range`)

Hyperparameters are like the **knobs** you turn to get better performance.

---

# **2. Why Hyperparameter Tuning Matters**

Your model currently uses **default** settings:

```python
LogisticRegression(max_iter=1000)
```

Defaults are OK for beginners, but almost never optimal.

Tuning helps your model:

* learn better patterns
* avoid overfitting
* avoid underfitting
* gain higher accuracy
* use the most informative text features

Hyperparameter tuning is one of the fastest ways to improve ML models.

---

# **3. What Is Grid Search? (Simple Explanation)**

Grid Search means:

> “Try all combinations of hyperparameters and find the best one.”

Example grid:

```python
{
    "clf__C": [0.1, 1.0, 10.0],
    "clf__penalty": ["l2"]
}
```

Grid Search will:

1. Train a model with C=0.1
2. Train a model with C=1.0
3. Train a model with C=10.0

and pick the best one.

This uses **cross-validation**, so each trial is reliable.

---

# **4. The Code You Added (Line-Mapped Explanation)**

Here is the tuning block added to `train.py`:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "clf__C": [0.1, 1.0, 10.0],
    "clf__max_iter": [500, 1000, 2000],
}

grid = GridSearchCV(
    model,
    param_grid,
    cv=5,
    scoring="accuracy"
)

grid.fit(X, y)

print("Best params:", grid.best_params_)
print("Best CV accuracy:", grid.best_score_)
```

Let’s walk through this carefully.

---

## **4.1 Importing GridSearchCV**

```python
from sklearn.model_selection import GridSearchCV
```

This brings in scikit-learn’s hyperparameter tuner.

---

## **4.2 Defining the Search Space**

```python
param_grid = {
    "clf__C": [0.1, 1.0, 10.0],
    "clf__max_iter": [500, 1000, 2000],
}
```

### 🔍 Why “clf__C”?

Your pipeline is named:

```
("clf", LogisticRegression(...))
```

To tune part of the pipeline, you use:

```
<stepname>__<parametername>
```

So:

* `clf__C` means “parameter C of the clf step”
* `clf__max_iter` means “parameter max_iter of the clf step”

This is a core scikit-learn concept.

---

## **4.3 Creating the Grid Search Object**

```python
grid = GridSearchCV(model, param_grid, cv=5, scoring="accuracy")
```

This:

* takes your pipeline
* explores all parameter combinations
* performs **5-fold cross-validation** for each combo
* evaluates accuracy

---

## **4.4 Running the Search**

```python
grid.fit(X, y)
```

This step might take a few seconds.

Grid Search will run:

* 3 values of C
* × 3 values of max_iter
* = 9 combinations
* × 5 folds each
* = 45 total model evaluations

Even for small datasets, this is fine.

---

## **4.5 Retrieving Best Results**

```python
grid.best_params_
grid.best_score_
```

Example output:

```
Best params: {'clf__C': 1.0, 'clf__max_iter': 2000}
Best CV accuracy: 0.6
```

Meaning:

* The best regularisation strength was C=1.0
* The best training iteration count was 2000
* The average cross-validation accuracy was 60%

This gives you a more stable estimate than the single split from earlier.

---

# **5. How Tuning Fits Into Your Workflow**

You do tuning **before** final training.

Full flow:

```
get_data()
↓
GridSearchCV (try hyperparameters)
↓
best_params (report)
↓
train_test_split (normal split)
↓
model.fit using either default or best settings
↓
classification_report
↓
save model
```

Hyperparameter tuning is **evaluation**, not **final training**.

---

# **6. How to Run This Micro-Task**

Simply:

```bash
python train.py
```

Your terminal will show:

* Best hyperparameters
* Best CV accuracy
* Normal train/test accuracy
* Saved model file

---

# **7. Understanding Your Tuning Output (Example)**

You may see something like:

```
Best params: {'clf__C': 10.0, 'clf__max_iter': 2000}
Best CV accuracy: 0.55
```

Interpretation:

* The model performed best with **stronger regularisation**
* And required more iterations to converge
* Overall cross-validation accuracy is around 55%

Given your dataset is tiny, these scores will fluctuate.
That’s normal.

---

# **8. Problem → Solution (Beginner Questions)**

### **Problem 1: “Why tune max_iter?”**

**Solution:**
If Logistic Regression doesn’t converge, it performs poorly.
Increasing `max_iter` allows it to learn more fully.

---

### **Problem 2: “Why tune C?”**

**Solution:**
C controls regularisation strength:

* Low C = stronger regularisation
* High C = weaker regularisation

It changes the model’s complexity.

---

### **Problem 3: “Does GridSearchCV replace cross-validation?”**

**Solution:**
No — GridSearchCV **uses** cross-validation.
Hyperparameter tuning depends on cross-validation.

---

### **Problem 4: “Should I always use tuning?”**

**Solution:**
When choosing or comparing models → YES.
For final production training → tuning is optional if time is limited.

---

# **9. Commands Cheat Sheet**

### Run hyperparameter tuning:

```bash
python train.py
```

### View best parameters:

Printed automatically via:

```python
print(grid.best_params_)
```

### View best accuracy:

```python
grid.best_score_
```

---

# **10. End-to-End Flow Diagram**

```
raw text → clean_text()
       ↓
TF-IDF
       ↓
initial model
       ↓
GridSearchCV (many small trainings)
       ↓
best hyperparameters
       ↓
train_test_split()
       ↓
final training
       ↓
model saved
       ↓
predict.py
```

---

# **11. Summary**

In this micro-task you learned:

* What hyperparameters are
* Why they matter in ML
* How GridSearchCV works
* How to tune Logistic Regression inside a pipeline
* How cross-validation powers tuning
* How to interpret best parameters and best score
* How tuning fits into your full training workflow

Hyperparameter tuning is one of the easiest ways to improve models quickly and systematically.

---
 