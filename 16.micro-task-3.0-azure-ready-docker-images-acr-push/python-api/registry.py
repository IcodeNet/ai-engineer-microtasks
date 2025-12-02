# registry.py - Local Model Registry Abstraction with Auto-Discovery

import json
from pathlib import Path
import joblib
from datetime import datetime


class ModelRegistry:
    """
    Simple filesystem-based model registry.

    Directory layout (root = "registry"):

      registry/
        versions/
          1.0.0/
            model.joblib
            metadata.json
          1.1.0/
            model.joblib
            metadata.json
        latest/
          model.joblib
          metadata.json
    """

    def __init__(self, root: str = "registry"):
        self.root = Path(root)
        self.versions_dir = self.root / "versions"
        self.latest_dir = self.root / "latest"
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.latest_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Save model + metadata
    # -------------------------------------------------------------------------
    def save_model(self, version: str, model, metadata: dict):
        """
        Save model + metadata under registry/versions/<version>/
        and update registry/latest/ with the same contents.
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

    # -------------------------------------------------------------------------
    # Load specific model
    # -------------------------------------------------------------------------
    def get_model(self, version: str):
        """
        Load model + metadata for a specific version from:
          registry/versions/<version>/
        """
        version_dir = self.versions_dir / version
        model_path = version_dir / "model.joblib"
        metadata_path = version_dir / "metadata.json"

        model = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text())
        return model, metadata

    # -------------------------------------------------------------------------
    # Load "latest" model (alias)
    # -------------------------------------------------------------------------
    def get_latest_model(self):
        """
        Load model + metadata for the 'latest' version.

        Implementation:
        - Uses get_latest_version() to determine the latest version by name.
        - Then delegates to get_model(version).

        If no versions exist, falls back to registry/latest/ as a raw alias.
        """
        versions = self.list_versions()
        if versions:
            latest_version = self.get_latest_version()
            return self.get_model(latest_version)

        # Fallback: use the latest alias directory directly
        model_path = self.latest_dir / "model.joblib"
        metadata_path = self.latest_dir / "metadata.json"

        model = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text())
        return model, metadata

    # -------------------------------------------------------------------------
    # NEW: list available versions
    # -------------------------------------------------------------------------
    def list_versions(self):
        """
        Return a sorted list of available model versions discovered under:

          registry/versions/

        Only directories are considered; file names are ignored.
        """
        if not self.versions_dir.exists():
            return []

        versions = []
        for child in self.versions_dir.iterdir():
            if child.is_dir():
                versions.append(child.name)

        # Sort lexically by default; you can swap this later for semantic sort.
        versions.sort()
        return versions

    # -------------------------------------------------------------------------
    # NEW: get latest version name
    # -------------------------------------------------------------------------
    def get_latest_version(self):
        """
        Determine the "latest" version name based on discovered versions.

        Strategy:
        - Try to parse versions as semantic version strings: MAJOR.MINOR.PATCH
          e.g. "1.0.0", "1.2.3"
        - If parsing fails for any version, fall back to simple lexical sort.

        Returns:
          - latest version string (e.g. "1.1.0"), or
          - raises ValueError if no versions exist.
        """
        versions = self.list_versions()
        if not versions:
            raise ValueError("No versions found in registry")

        def parse_semver(v: str):
            parts = v.split(".")
            if len(parts) != 3:
                raise ValueError("not semver")
            return tuple(int(p) for p in parts)

        # Try semantic version sort first
        try:
            versions_sorted = sorted(versions, key=parse_semver)
        except Exception:
            # Fallback to lexical sort
            versions_sorted = sorted(versions)

        return versions_sorted[-1]

    # -------------------------------------------------------------------------
    # NEW: get metadata for a specific version
    # -------------------------------------------------------------------------
    def get_metadata(self, version: str):
        """
        Read and return metadata.json for a specific version without
        loading the model.

        Path:
          registry/versions/<version>/metadata.json
        """
        version_dir = self.versions_dir / version
        metadata_path = version_dir / "metadata.json"
        return json.loads(metadata_path.read_text())