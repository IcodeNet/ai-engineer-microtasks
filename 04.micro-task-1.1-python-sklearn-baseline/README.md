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

## 🚀 Quick Setup (First Time)

### Prerequisites

- **Python 3.10+** installed
- **direnv** (optional but recommended for auto-activation on Mac/Linux/WSL)
  - **Note**: On Windows 11, direnv works best through WSL. Native Windows PowerShell/CMD users can use manual activation.

### Step 1: Install direnv (Optional but Recommended)

**Mac:**
```bash
brew install direnv
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install direnv

# Fedora
sudo dnf install direnv
```

**Windows 11:**

direnv works best on Windows through **WSL (Windows Subsystem for Linux)**:

1. **Install WSL** (if not already installed):
   ```powershell
   wsl --install
   ```
   Restart your computer after installation.

2. **Inside WSL**, install direnv:
   ```bash
   sudo apt update
   sudo apt install direnv
   ```

3. **Configure direnv hook** in WSL (add to `~/.bashrc` or `~/.zshrc`):
   ```bash
   eval "$(direnv hook bash)"  # or "zsh" for zsh
   source ~/.bashrc
   ```

**Alternative for Windows (without WSL):**

If you're using PowerShell/CMD (not WSL), direnv auto-activation won't work. You can still use manual activation:
```powershell
# PowerShell
.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat
```

**Configure direnv hook** (Mac/Linux - add to `~/.zshrc` or `~/.bashrc`):
```bash
eval "$(direnv hook zsh)"  # or "bash" for bash
source ~/.zshrc
```

### Step 2: Create Virtual Environment

**Option A: Using `uv` (Recommended - Fastest)**

**Mac/Linux/WSL:**
```bash
uv venv
uv pip install -r requirements.txt
```

**Windows (PowerShell/CMD):**
```powershell
uv venv
uv pip install -r requirements.txt
```

**Option B: Using standard Python**

**Mac/Linux/WSL:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Note for Windows PowerShell:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Allow .envrc (One-Time Setup)

**Mac/Linux/WSL only:**

If you have direnv installed, allow the `.envrc` file:

```bash
direnv allow
```

This enables automatic environment activation when you `cd` into this directory.

**What this does:**
- ✅ Automatically activates `.venv` when you enter the directory
- ✅ Automatically deactivates when you leave
- ✅ No need to manually run `source .venv/bin/activate`

**Windows PowerShell/CMD:**

The `.envrc` file uses Unix shell syntax and won't work in native Windows PowerShell/CMD. Use manual activation instead (see Step 4 for verification). If you're using WSL, direnv will work normally.

### Step 4: Verify Setup

**Mac/Linux/WSL:**
```bash
# cd out and back in to test auto-activation
cd ..
cd 04.micro-task-1.1-python-sklearn-baseline

# Check Python is using venv
which python  # Should show: .../.venv/bin/python
python --version  # Should show Python 3.x
```

**Windows (PowerShell):**
```powershell
# cd out and back in to test auto-activation
cd ..
cd 04.micro-task-1.1-python-sklearn-baseline

# Check Python is using venv
where.exe python  # Should show: ...\.venv\Scripts\python.exe
python --version  # Should show Python 3.x
```

**Windows (CMD):**
```cmd
cd ..
cd 04.micro-task-1.1-python-sklearn-baseline

where python
python --version
```

## 🎯 How to Run

### Train the Model

```bash
python train.py
```

You should see output including test accuracy and a message indicating where the model was saved.

### Run a Prediction

```bash
python predict.py "this is great"
```

## 🔄 Auto-Activation with direnv

**If you have direnv set up (Mac/Linux/WSL):**

- **Auto-activate**: Just `cd` into the project directory
- **Auto-deactivate**: `cd` out of the directory
- **No manual activation needed**: The `.envrc` file handles it automatically

**If you don't have direnv (or using Windows PowerShell/CMD):**

You can still use manual activation:

**Mac/Linux/WSL:**
```bash
source .venv/bin/activate
deactivate  # When done
```

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
deactivate  # When done
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
deactivate  # When done
```

## 🛠️ Troubleshooting

### direnv not working?

1. **Check direnv is installed:**
   ```bash
   direnv --version
   ```

2. **Check direnv hook is configured:**
   ```bash
   grep "direnv hook" ~/.zshrc  # or ~/.bashrc
   ```

3. **Make sure .venv exists:**
   ```bash
   ls -la .venv
   ```

4. **Re-allow .envrc:**
   ```bash
   direnv allow
   ```

### Virtual environment not activating?

**Mac/Linux/WSL:**
- **Manual activation still works:**
  ```bash
  source .venv/bin/activate
  ```

- **Check .venv exists:**
  ```bash
  ls -la .venv/bin/python
  ```

- **Recreate if needed:**
  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

**Windows:**
- **Manual activation:**
  ```powershell
  # PowerShell
  .venv\Scripts\Activate.ps1
  
  # CMD
  .venv\Scripts\activate.bat
  ```

- **Check .venv exists:**
  ```powershell
  # PowerShell
  Test-Path .venv\Scripts\python.exe
  
  # CMD
  dir .venv\Scripts\python.exe
  ```

- **Recreate if needed:**
  ```powershell
  # PowerShell
  Remove-Item -Recurse -Force .venv
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

- **PowerShell execution policy error?**
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
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

 

 
 
 
 
