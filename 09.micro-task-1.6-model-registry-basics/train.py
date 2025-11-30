# train.py - Model Training with Registry Storage

import json
from datetime import datetime
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from registry import ModelRegistry
from text_utils import clean_text

MODEL_VERSION = "1.0.0"


def get_data():
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
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(preprocessor=clean_text)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    return pipeline


def main():
    registry = ModelRegistry()

    X, y = get_data()

    print("=== Hyperparameter Tuning ===")
    base_model = build_model()

    param_grid = {
        "clf__C": [0.1, 1.0, 10.0],
        "clf__max_iter": [500, 1000, 2000],
    }

    grid = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
    )

    grid.fit(X, y)

    best_params = grid.best_params_
    best_cv_accuracy = float(grid.best_score_)

    print("Best params:", best_params)
    print("Best CV accuracy:", best_cv_accuracy)

    best_model = grid.best_estimator_

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    best_model.fit(X_train, y_train)

    y_pred = best_model.predict(X_test)

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    test_accuracy = float(accuracy_score(y_test, y_pred))

    metadata = {
        "version": MODEL_VERSION,
        "saved_at": datetime.utcnow().isoformat()
        + "Z",
        "best_params": best_params,
        "best_cv_accuracy": best_cv_accuracy,
        "test_accuracy": test_accuracy,
    }

    registry.save_model(MODEL_VERSION, best_model, metadata)


if __name__ == "__main__":
    main()
