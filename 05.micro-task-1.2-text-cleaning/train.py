# train.py - Text Classification Model Training with Text Cleaning

from text_utils import clean_text
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline




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
                    preprocessor=clean_text,  # <-- cleaning happens here
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ],
        memory=None
    )
    return pipeline


def main():
    # 1. Load data
    X, y = get_data()

    # 2. Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    # 3. Build and train model
    model = build_model()
    model.fit(X_train, y_train)

    # 4. Evaluate on test set
    y_pred = model.predict(X_test)

    print("=== y_test (true labels) ===")
    print(y_test)

    print("\n=== y_pred (model predictions) ===")
    print(list(y_pred))

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {acc:.3f}")

    # 5. Optional: inspect TF-IDF vocabulary to confirm cleaning
    tfidf = model.named_steps["tfidf"]
    vocab = tfidf.vocabulary_
    print("\n=== TF-IDF Vocabulary Sample (first 20 entries) ===")
    print(dict(list(vocab.items())[:20]))

    # 6. Persist model to disk
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "text_classifier.joblib"
    joblib.dump(model, model_path)

    print(f"\nSaved model to {model_path.resolve()}")


if __name__ == "__main__":
    main()
