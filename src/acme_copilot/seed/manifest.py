from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]


def project_root() -> Path:
    return ROOT


def load_manifest(path: Path | None = None) -> dict[str, Any]:
    manifest_path = path or (ROOT / "data" / "manifest.yaml")
    with manifest_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid manifest at {manifest_path}")
    return data
