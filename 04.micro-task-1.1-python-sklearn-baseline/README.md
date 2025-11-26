# 04.micro-task-1.1-python-sklearn-baseline

### Learning objectives

By the end of this micro-task you’ll be able to say:

* “I can train a basic text classifier end-to-end in Python.”
* “I know how to persist a model + vectoriser to disk so it can be served by another process.”
* “I can  can reload them and run a prediction from the command line.”


This is the first concrete tick against “pre-LLM methods” and classical ML.

---

### Components involved

You’ll create a *separate* micro-task folder:

`04.micro-task-1.1-python-sklearn-baseline/`

Inside it:

* A minimal **Python project** (no framework, just scripts)
* A script to:

  * define a tiny labelled dataset (hard-coded)
  * vectorise text (e.g. `TfidfVectorizer`)
  * train a simple model (e.g. logistic regression)
  * evaluate on a hold-out set
  * **save** the model + vectoriser to disk (e.g. with `joblib`)

Rough structure:

```text
04.micro-task-1.1-python-sklearn-baseline/
  train.py          # trains model and saves artefacts
  predict.py        # loads artefacts and does a single prediction from CLI
  requirements.txt
  README.md
  models/
    (created by train.py, e.g. classifier.joblib, vectorizer.joblib)
```

 Good. Then we go straight into building your **first real model**.

---

## 04.micro-task-1.1-python-sklearn-baseline

### 🎯 Learning objectives

By the end of this micro-task you will be able to say:

* You’ve **trained** a text classifier end-to-end in Python.
* You can **save** the model + vectoriser to disk as deployable artefacts.
* You can **reload** them and run a prediction from the command line.

This is your first concrete tick against “pre-LLM methods” and “training + deploying models”.

---

## 🧩 Components in this task

New folder at repo root:

`04.micro-task-1.1-python-sklearn-baseline/`

Inside:

```text
04.micro-task-1.1-python-sklearn-baseline/
  requirements.txt
  train.py
  predict.py
  models/            # created by train.py
  README.md
```

### Libraries

We’ll use:

* `scikit-learn` – vectoriser + classifier
* `joblib` – model persistence

---

## 1. `requirements.txt`

Create `04.micro-task-1.1-python-sklearn-baseline/requirements.txt`:

```txt
scikit-learn
joblib
```

(If you want, you can later add `numpy`/`pandas`, but not needed for this task.)

---

## 2. `train.py` — train and save model

Create `train.py` in that folder.

**Conceptual flow:**

1. Define a tiny labelled dataset (list of texts + labels).
2. Split into train / test.
3. Build a `Pipeline(TfidfVectorizer + LogisticRegression)`.
4. Train the model.
5. Evaluate on test set (print accuracy).
6. Save the trained pipeline to `models/text_classifier.joblib`.

Here is a solid, production-shaped starting point:

```python
# train.py
import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


def get_data():
    # Tiny toy dataset – sentiment-style
    texts = [
        "this is great",
        "I love this product",
        "absolutely fantastic experience",
        "really bad service",
        "this is terrible",
        "I hate this",
        "not good at all",
        "pretty nice overall",
        "quite enjoyable",
        "awful and disappointing",
    ]
    labels = [
        "positive",
        "positive",
        "positive",
        "negative",
        "negative",
        "negative",
        "negative",
        "positive",
        "positive",
        "negative",
    ]
    return texts, labels


def build_model():
    # Vectoriser + linear classifier
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    return pipeline


def main():
    X, y = get_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = build_model()
    model.fit(X_train, y_train)

    # simple evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {acc:.3f}")

    # persist model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "text_classifier.joblib"
    joblib.dump(model, model_path)

    print(f"Saved model to {model_path.resolve()}")


if __name__ == "__main__":
    main()
```

You can tweak dataset texts/labels if you like, but keep the structure.

---

## 3. `predict.py` — load and run one prediction

This script will:

* Load the saved pipeline.
* Take a text from the command line.
* Print the predicted label and (optional) probabilities.

```python
# predict.py
import sys
from pathlib import Path

import joblib


def load_model():
    model_path = Path("models/text_classifier.joblib")
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}. Run train.py first.")
    return joblib.load(model_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python predict.py \"some text to classify\"")
        sys.exit(1)

    text = sys.argv[1]
    model = load_model()

    pred = model.predict([text])[0]

    # Optional: probability per class (if supported)
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([text])[0]
        classes = model.classes_
        print(f"Prediction: {pred}")
        print("Class probabilities:")
        for cls, p in zip(classes, proba):
            print(f"  {cls}: {p:.3f}")
    else:
        print(f"Prediction: {pred}")


if __name__ == "__main__":
    main()
```

---
 
## Overview

This micro-task trains a simple text classifier using scikit-learn and saves it as a reusable model artefact.  
The goal is to establish a baseline "pre-LLM" model that can later be wired into the Node.js service layer.

## Learning Objectives

By completing this micro-task, you will be able to:

- Train a classical ML text classifier end-to-end in Python.
- Evaluate the model on a small hold-out test set.
- Persist the trained model to disk and load it again for inference.

## Tech Stack

- **Language:** Python 3.10+
- **Libraries:** scikit-learn, joblib

## Project Structure

```text
04.micro-task-1.1-python-sklearn-baseline/
  requirements.txt       # Python dependencies
  train.py               # Trains the classifier and saves artefacts
  predict.py             # Loads the classifier and predicts for one input text
  models/
    text_classifier.joblib   # Saved model pipeline (created by train.py)
  README.md
```

## How to Run

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux/macOS
   # .venv\Scripts\activate       # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Train the model:

   ```bash
   python train.py
   ```

   You should see output including test accuracy and a message indicating where the model was saved.

4. Run a prediction:

   ```bash
   python predict.py "this is great"
   ```

   Example output:

   ```text
   Prediction: positive
   Class probabilities:
     negative: 0.123
     positive: 0.877
   ```

## Next Steps

The next micro-task will:

* Wrap this Python model in a simple service or CLI bridge.
* Allow the Node.js Fastify layer to call the Python model for real predictions.
 

---

 

 
 
 
 
