# registry.py - Local Model Registry Abstraction

import json
from pathlib import Path
import joblib
from datetime import datetime

# Import clean_text so joblib can unpickle models that reference it
from text_utils import clean_text


class ModelRegistry:
    def __init__(self, root: str = "registry"):
        self.root = Path(root)
        self.versions_dir = self.root / "versions"
        self.latest_dir = self.root / "latest"
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.latest_dir.mkdir(parents=True, exist_ok=True)

    def save_model(self, version: str, model, metadata: dict):
        """
        Save model + metadata under registry/versions/<version>/
        Also update registry/latest/ with the same contents.
        """

        # --- Save versioned directory ---
        version_dir = self.versions_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)

        model_path = version_dir / "model.joblib"
        metadata_path = version_dir / "metadata.json"

        joblib.dump(model, model_path)
        metadata_path.write_text(json.dumps(metadata, indent=2))

        # --- Save latest alias ---
        latest_model_path = self.latest_dir / "model.joblib"
        latest_metadata_path = self.latest_dir / "metadata.json"

        joblib.dump(model, latest_model_path)
        latest_metadata_path.write_text(json.dumps(metadata, indent=2))

        print(f"[registry] Saved version {version}")
        print(f"[registry] Updated latest model alias")

    def get_latest_model(self):
        model_path = self.latest_dir / "model.joblib"
        metadata_path = self.latest_dir / "metadata.json"
        model = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text())
        return model, metadata

    def get_model(self, version: str):
        version_dir = self.versions_dir / version
        model_path = version_dir / "model.joblib"
        metadata_path = version_dir / "metadata.json"
        model = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text())
        return model, metadata
