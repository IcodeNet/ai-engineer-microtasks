# 07 – Micro-Task 1.4: Hyperparameter Tuning with GridSearchCV

## Overview

This micro-task extends the cleaned text classifier by adding **hyperparameter tuning** using scikit-learn’s `GridSearchCV`.

Instead of relying on the default settings of `LogisticRegression`, this task:

- defines a small search space for key hyperparameters (`C`, `max_iter`)
- runs **k-fold cross-validation** internally for each combination
- selects the **best-performing model** based on mean cross-validation accuracy
- evaluates that best model on a separate train/test split
- saves the tuned model for use by `predict.py`

The model architecture remains the same:

- Text cleaning via `clean_text()`
- TF-IDF vectorisation
- Logistic Regression classifier

Only the configuration (hyperparameters) is being optimised.

---

## Learning Objectives

By completing this micro-task, you will be able to:

- Understand what hyperparameters are and why they matter
- Use `GridSearchCV` to tune model hyperparameters
- Interpret the best parameters and best cross-validation score
- Use the tuned model for a final train/test evaluation
- Save the tuned model as a deployable artefact

---

## Tech Stack

- **Language:** Python 3.10+
- **Libraries:** scikit-learn, joblib, re, pathlib

---

## Project Structure

```text
07.micro-task-1.4-hyperparameter-tuning/
  train.py           # Text cleaning + hyperparameter tuning + train/test + save
  predict.py         # Loads model and predicts sentiment for a single input text
  requirements.txt   # Python dependencies
  models/
    text_classifier.joblib   # Tuned model (created by train.py)
  README.md
  LEARNING.md        # Conceptual + line-mapped explanation of hyperparameter tuning