
---

# **LEARNING.md – Micro-Task 1.1 (Python Sklearn Baseline)**

### *A complete beginner-friendly explanation of everything happening in `train.py` and `predict.py`*

This document explains both the **theory** and the **code** involved in training a very simple machine-learning model to classify text as *positive* or *negative*.

It assumes **no prior ML experience**.

By the end, you will understand:

* **what each line of code does**
* **why we do it**
* **where every metric comes from**
* **how the model learns**
* **how the results you saw were generated**
* **your earlier questions answered in context**

---

# ⭐ 1. What This Micro-Task Is About

This micro-task teaches you how to:

1. Build a tiny labelled dataset
2. Convert raw text into numbers using **TF-IDF**
3. Train a simple classifier (**Logistic Regression**)
4. Test the model on unseen data
5. Understand accuracy, precision, recall, F1
6. Save a trained model
7. Reload it to make predictions

This workflow (train → evaluate → save → load → predict) is the foundation for **all ML** you’ll do later (BERT, LLMs, Whisper, etc.).

---

# ⭐ 2. Understanding the Theory (Beginner-Friendly)

Let’s make the core ML concepts simple and visual.

---

## 🧠 2.1 What is a “Model”?

A model is a small mathematical program that tries to answer a question.

Here, the question is:

> “Is this sentence positive or negative?”

The model learns this by seeing examples.

---

## 🎓 2.2 What is “Training”?

Training means:

1. You show the model examples
2. It learns patterns
3. It guesses better over time

Example:

* “I love this” → positive
* “awful experience” → negative

The model slowly learns **which words** tend to belong to which class.

---

## 🔢 2.3 Why convert text to numbers?

Models cannot understand text.

We must convert:

```
"This is great"
```

into a **numeric representation**.

We use **TF-IDF** to turn each sentence into a **vector of numbers**.

Plain English:

* Words that appear often get higher values
* Very common words (“the”, “is”) get less weight
* Words unique to a sentiment (“great”, “terrible”) become important

This lets a classifier understand text mathematically.

---

## 🎯 2.4 What is Logistic Regression?

Despite the name, it’s a **classification** model.

It tries to draw a boundary:

```
[positive texts]   vs   [negative texts]
```

It’s:

* simple
* fast
* reliable

Perfect for learning.

---

## 🧪 2.5 What is train/test split?

We must test the model on examples it has **never** seen.

So we split the data:

* **Training set** → used to learn
* **Test set** → used to evaluate

In your code:

* 70% training
* 30% testing

This avoids lying to yourself about how well the model works.

---

## 📊 2.6 What are accuracy, precision, recall, F1?

### ✔️ Accuracy

Overall correctness.

```
correct predictions / total predictions
```

### ✔️ Precision

When the model says *positive*,
how often is it right?

### ✔️ Recall

Of all real *positives*,
how many did the model find?

### ✔️ F1

A balance between precision and recall.

We will decode your actual outputs later.

---

# ⭐ 3. Full Code Mapping (Line-by-Line Explanation)

This section shows each ML concept mapped **exactly** to the code that implements it.

---

## 📦 3.1 Building the Dataset

**Code:**

```python
def get_data():
    texts = [...]
    labels = [...]
    return texts, labels
```

**Meaning:**
These hard-coded examples are your “training material”.

The model will learn from these.

---

## 🧱 3.2 Building the Model Pipeline

**Code:**

```python
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000)),
])
```

This defines two steps:

1. `"tfidf"` → convert text to numbers
2. `"clf"` → classify those numbers into positive/negative

---

## 🔀 3.3 Train/Test Split

**Code:**

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
```

This is where your **test labels** come from:

```
['negative', 'negative', 'positive']
```

Those are the true labels used during evaluation.

---

## 🚀 3.4 Training the Model

**Code:**

```python
model.fit(X_train, y_train)
```

This is where the model *learns*.

---

## 🔮 3.5 Model Predictions

**Code:**

```python
y_pred = model.predict(X_test)
```

This produced your model’s guesses:

```
['positive', 'positive', 'positive']
```

Every metric is calculated from comparing:

```
y_test  vs  y_pred
```

---

## 🧾 3.6 Generating the Metrics

**Code:**

```python
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))
```

Running:

```bash
python train.py
```

printed your classification report.

We decode it in Section 4.

---

## 💾 3.7 Saving the Model

**Code:**

```python
joblib.dump(model, "models/text_classifier.joblib")
```

This produces a file you can load later.

---

# ⭐ 4. Understanding Your Actual Output (Full Breakdown)

You saw:

```
=== y_test ===
['negative', 'negative', 'positive']

=== y_pred ===
['positive', 'positive', 'positive']
```

Let’s decode this.

---

## 🧮 4.1 Real counts (from y_test)

```
Real negatives: 2
Real positives: 1
```

## 🧮 4.2 Model predictions (from y_pred)

```
Predicted negatives: 0
Predicted positives: 3
```

## 🧮 4.3 Correct predictions

Only one match:

```
positive → positive  (correct)
```

Accuracy = 1/3 = **0.33**

---

## 📋 4.4 Classification Report (Your Real Output)

```
negative   precision=0.00 recall=0.00 f1=0.00 support=2
positive   precision=0.33 recall=1.00 f1=0.50 support=1
accuracy = 0.33
```

### Why?

* Model predicted “positive” for *every* test sample
* Therefore:

  * Negative precision = 0
  * Negative recall = 0
  * Positive recall = 1 (it caught the only positive)
  * Positive precision = 1/3

All consistent with the arrays.

---

# ⭐ 5. Problem → Solution (Your Questions Mapped to Code)

---

## ❓ Problem 1

**“Where do numbers like ‘model predicted 5 positives’ come from?”**

### ✔️ Solution

They come directly from:

```python
y_pred = model.predict(X_test)
```

To count predicted positives:

```python
y_pred.count("positive")
```

---

## ❓ Problem 2

**“Where do we see real positives/negatives?”**

### ✔️ Solution

They come directly from:

```python
y_test
```

Count them:

```python
y_test.count("positive")
```

---

## ❓ Problem 3

**“Why is precision undefined sometimes?”**

### ✔️ Solution

If the model never predicts a class (e.g. negative), then:

```
precision = true_positives / predicted_positives
```

becomes:

```
0 / 0 = undefined
```

scikit-learn sets it to 0.0 and warns you.

---

## ❓ Problem 4

**“How do you interpret the classification report?”**

### ✔️ Solution

Each line corresponds to:

* precision: correct predictions / predicted
* recall: correct predictions / real
* f1: harmonic mean
* support: number of true examples

---

# ⭐ 6. Commands Cheat Sheet

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Train the model:

```bash
python train.py
```

### Predict with saved model:

```bash
python predict.py "this is great"
```

### Check saved model:

```
models/text_classifier.joblib
```

---

# ⭐ 7. What To Improve Next (Future Micro-Tasks)

* Add text cleaning
* Better metrics (precision/recall/F1 visualisation)
* Cross-validation
* Hyperparameter tuning
* Model versioning
* Deployment behind an API
* Connecting this model to Node.js Fastify

All of these build on this micro-task.

---

# ⭐ 8. Final Summary

This document combined:

* **Beginner-safe theory**
* **Exact code mapping**
* **Your questions + answers**
* **Actual outputs + how they were produced**
* **Step-by-step training logic**

You now understand *precisely* how and why your first ML model works.

---

 