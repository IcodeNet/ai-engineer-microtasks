# train.py

import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression 
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sklearn.metrics import classification_report

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
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ],
        memory=None
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

    print("\n=== y_test (true labels) ===")
    print(y_test)

    print("\n=== y_pred (model predictions) ===")
    print(list(y_pred))

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

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