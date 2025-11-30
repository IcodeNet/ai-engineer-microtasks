```
07.micro-task-1.4-hyperparameter-tuning/LEARNING.md
```
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

**Explanation:**
Logistic Regression weights are numerical values that the model learns during training. Each weight corresponds to how important a particular feature (word or text pattern) is for making predictions. For example, if the word "excellent" has a high positive weight, the model learned that this word strongly indicates a positive sentiment. If "terrible" has a high negative weight, the model learned it indicates negative sentiment. These weights are automatically adjusted during training as the model sees examples and learns which features are most useful for classification. You don't set these manually — the algorithm calculates them by finding the best values that minimize prediction errors on your training data.

### **B) Hyperparameters**

These are settings **you choose**, not the model.

Examples:

* how many iterations to run (`max_iter`)
  **Explanation:** `max_iter` is the maximum number of iterations (training steps) the Logistic Regression algorithm will perform. Each iteration is one attempt to adjust the model's weights to better fit the data. Think of it like this: the algorithm starts with random weights, then on each iteration it looks at the training data, calculates how wrong its predictions are, and adjusts the weights slightly to improve. It repeats this process until either (1) the weights stop changing much (convergence), or (2) it reaches the `max_iter` limit. If `max_iter=500`, the algorithm stops after 500 attempts, even if it hasn't fully converged. Higher values (like 2000) give the model more chances to fine-tune its weights and learn complex patterns, but take longer to train. If you see a "convergence warning," it means the algorithm hit the `max_iter` limit before finding optimal weights — increasing `max_iter` usually fixes this.

* how strong regularisation is (`C`)
  **Explanation:** Regularisation prevents the model from overfitting (memorizing training data too closely). The `C` parameter controls this: **lower C** (like 0.1) means **stronger regularisation** (simpler model, less overfitting), while **higher C** (like 10.0) means **weaker regularisation** (more complex model, risk of overfitting). It's like a dial between "keep it simple" and "learn everything." Finding the right C is crucial for good performance.
  
  **Why is it called "C"?** The name comes from the mathematical formulation of Support Vector Machines (SVMs), where C was used as a constant in the optimization equation. Logistic Regression in scikit-learn uses the same naming convention for historical consistency. In the math, C represents the "cost" of misclassification — higher C means the model pays a higher cost for making mistakes, so it tries harder to fit the training data (weaker regularization). Think of C as the "cost constant" or "complexity constant."

* what penalty type to use (`l2`, `l1`)
  **Explanation:** These are different ways to apply regularisation. **L2 penalty** (also called "ridge") shrinks all weights proportionally — it's smooth and works well for most cases. **L1 penalty** (also called "lasso") can shrink some weights to exactly zero, effectively removing less important features. L1 is useful when you want feature selection (automatically ignoring irrelevant words), while L2 is gentler and usually preferred for text classification.

* how TF-IDF creates features (`min_df`, `max_df`, `ngram_range`)
  **Explanation:** TF-IDF (Term Frequency-Inverse Document Frequency) converts text into numerical features that your model can use. These hyperparameters control which words become features and how they're combined. **`min_df`** (minimum document frequency) ignores words that appear in fewer than X documents — useful for filtering out typos, rare words, or noise that won't help predictions. For example, `min_df=2` means a word must appear in at least 2 documents to be included. **`max_df`** (maximum document frequency) ignores words that appear in more than X% of documents — useful for filtering out common stop words like "the", "and", "is" that appear everywhere and don't help distinguish between classes. For example, `max_df=0.95` means words appearing in more than 95% of documents are ignored. **`ngram_range`** controls word combinations: `(1,1)` uses only single words (unigrams), `(1,2)` uses both single words and pairs of consecutive words (bigrams), like "very good" or "not bad". Bigrams can capture phrases and context that single words miss, potentially improving accuracy but creating more features (and slower training).

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

**What is the `clf__` prefix?** The `clf__` prefix tells Grid Search which step in your pipeline to tune. In your pipeline, the classifier step is named `"clf"` (short for "classifier"), so `clf__C` means "the C parameter of the clf step." The double underscore `__` is scikit-learn's syntax for accessing parameters inside a pipeline step. This allows you to tune hyperparameters of specific steps when you have a multi-step pipeline (like TF-IDF → Logistic Regression).

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


 # Next Steps

After this micro-task, you are ready to move from offline training to:
*	Model versioning (naming and tracking model artefacts over time)
*	Deploying the tuned model behind an API (FastAPI or Node/Fastify bridge)
*	Connecting to your Node.js service layer so your Fastify micro-tasks call this tuned Python model.
