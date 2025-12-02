# train.py - Text Classification with Cleaning, Tuning, and Model Versioning

import json
from datetime import datetime
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from text_utils import clean_text

# Manual semantic version for this model line
MODEL_VERSION = "1.0.0"


def get_data():
    """
    Tiny toy dataset for sentiment classification.
    Positive vs negative short sentences.
    """
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
    """
    Build a scikit-learn Pipeline that:
    - Cleans and vectorises text via TF-IDF
    - Trains a Logistic Regression classifier
    """
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,  # cleaning happens here
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    return pipeline


def main():
    # 1. Load full dataset
    X, y = get_data()

    # 2. Hyperparameter tuning with GridSearchCV (uses internal cross-validation)
    print("=== Hyperparameter Tuning with GridSearchCV (5-fold, accuracy) ===")

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
    print(f"Best CV accuracy: {best_cv_accuracy:.3f}\n")

    # Use the best model found by GridSearchCV
    best_model = grid.best_estimator_

    # 3. Train/test split for a concrete hold-out evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    # 4. Train the best model on the training set
    best_model.fit(X_train, y_train)

    # 5. Evaluate on the hold-out test set
    y_pred = best_model.predict(X_test)

    print("=== y_test (true labels) ===")
    print(y_test)

    print("\n=== y_pred (model predictions) ===")
    print(list(y_pred))

    print("\n=== Classification Report (hold-out test set) ===")
    print(classification_report(y_test, y_pred))

    test_accuracy = float(accuracy_score(y_test, y_pred))
    print(f"\nTest accuracy (single train/test split): {test_accuracy:.3f}")

    # 6. Optional: inspect TF-IDF vocabulary to confirm cleaning
    tfidf = best_model.named_steps["tfidf"]
    vocab = tfidf.vocabulary_
    print("\n=== TF-IDF Vocabulary Sample (first 20 entries) ===")
    print(dict(list(vocab.items())[:20]))

    # 7. Persist versioned model + metadata to disk
    models_root = Path("models")
    models_root.mkdir(exist_ok=True)

    # Version-specific directory: models/<MODEL_VERSION>/
    version_dir = models_root / MODEL_VERSION
    version_dir.mkdir(parents=True, exist_ok=True)

    versioned_model_path = version_dir / "text_classifier.joblib"
    joblib.dump(best_model, versioned_model_path)

    # Write metadata.json for this version
    metadata = {
        "version": MODEL_VERSION,
        "saved_at": datetime.utcnow().isoformat() + "Z",
        "best_params": best_params,
        "best_cv_accuracy": best_cv_accuracy,
        "test_accuracy": test_accuracy,
    }
    metadata_path = version_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    print(f"\nSaved versioned model to {versioned_model_path.resolve()}")
    print(f"Saved metadata to {metadata_path.resolve()}")

    # 8. Also update a 'latest' alias for predict.py
    latest_path = models_root / "text_classifier.joblib"
    joblib.dump(best_model, latest_path)
    print(f"Updated latest model alias at {latest_path.resolve()}")


if __name__ == "__main__":
    main()