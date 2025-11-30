# train.py - Text Classification with Text Cleaning + Cross-Validation

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline

from text_utils import clean_text


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

    # 2. Cross-validation on the full dataset (evaluation only)
    print("=== Cross-validation (5-fold, accuracy) ===")
    cv_model = build_model()

    cv_scores = cross_val_score(
        cv_model,
        X,
        y,
        cv=5,
        scoring="accuracy",
    )

    print("CV scores:", cv_scores)
    print("CV mean accuracy:", cv_scores.mean())
    print("CV std:", cv_scores.std())
    print()

    # 3. Train/test split for a concrete hold-out evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    # 4. Build and train model on the training set
    model = build_model()
    model.fit(X_train, y_train)

    # 5. Evaluate on the hold-out test set
    y_pred = model.predict(X_test)

    print("=== y_test (true labels) ===")
    print(y_test)

    print("\n=== y_pred (model predictions) ===")
    print(list(y_pred))

    print("\n=== Classification Report (hold-out test set) ===")
    print(classification_report(y_test, y_pred))

    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy (single train/test split): {acc:.3f}")

    # 6. Optional: inspect TF-IDF vocabulary to confirm cleaning
    tfidf = model.named_steps["tfidf"]
    vocab = tfidf.vocabulary_
    print("\n=== TF-IDF Vocabulary Sample (first 20 entries) ===")
    print(dict(list(vocab.items())[:20]))

    # 7. Persist model to disk (for predict.py)
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "text_classifier.joblib"
    joblib.dump(model, model_path)

    print(f"\nSaved model to {model_path.resolve()}")


if __name__ == "__main__":
    main()