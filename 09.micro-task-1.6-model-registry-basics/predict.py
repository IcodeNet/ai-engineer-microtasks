# predict.py - Predict Using Registry

import sys
import argparse
from registry import ModelRegistry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=str)
    parser.add_argument("--version", type=str, default=None)
    args = parser.parse_args()

    registry = ModelRegistry()

    if args.version:
        model, metadata = registry.get_model(args.version)
        print(f"[registry] Loaded model version {args.version}")
    else:
        model, metadata = registry.get_latest_model()
        print("[registry] Loaded latest model")

    prediction = model.predict([args.text])[0]
    print(f"Prediction: {prediction}")


if __name__ == "__main__":
    main()

