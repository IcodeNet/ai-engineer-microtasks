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
