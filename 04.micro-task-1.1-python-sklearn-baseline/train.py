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

    # Split data into training (70%) and testing (30%) sets
    # See: file://./docs/train_test_split.md
    # Docs: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    # - test_size=0.3: 30% for testing, 70% for training
    # - random_state=42: ensures reproducible splits
    # - stratify=y: maintains class balance (50/50 positive/negative) in both sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Build the model pipeline (TfidfVectorizer + LogisticRegression)
    # See: file://./docs/build_train_predict.md
    # Docs: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
    # The pipeline combines text vectorization and classification into one model
    model = build_model()
    
    # Train the model on training data
    # See: file://./docs/build_train_predict.md
    # Docs: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline.fit
    # This learns: (1) vocabulary from texts, (2) patterns to classify positive/negative
    model.fit(X_train, y_train)

    # Evaluate the model on test data (unseen examples)
    # See: file://./docs/build_train_predict.md
    # Docs: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline.predict
    # Returns predictions for the 3 test examples
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