# 06 – Micro-Task 1.3: Cross-Validation for Text Classifier

## Overview

This micro-task extends the cleaned text classifier by adding **k-fold cross-validation**.  
Instead of relying on a single random train/test split, the model is evaluated several times on different splits of the data, giving a more reliable view of its performance.

The model itself is unchanged:

- Text is cleaned with `clean_text()`
- Text is vectorised with TF-IDF
- A Logistic Regression classifier is used

What changes here is **how** you evaluate it.

---

## Learning Objectives

By completing this micro-task, you will be able to:

- Understand why a single train/test split can be misleading
- Use scikit-learn’s `cross_val_score` to run k-fold cross-validation
- Interpret a set of cross-validation scores (mean and standard deviation)
- Keep a separate hold-out test evaluation and saved model

---

## Tech Stack

- **Language:** Python 3.10+
- **Libraries:** scikit-learn, joblib, re, pathlib

---

## Project Structure

```text
06.micro-task-1.3-cross-validation/
  train.py           # Text cleaning + cross-validation + train/test split + save
  predict.py         # Loads model and predicts sentiment for a single input text
  requirements.txt   # Python dependencies
  models/
    text_classifier.joblib   # Saved model (created by train.py)
  README.md
  LEARNING.md        # Conceptual + line-mapped explanation of this micro-task