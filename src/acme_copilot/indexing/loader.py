from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class CorpusDocument:
    """One markdown file: body text + YAML frontmatter metadata."""

    path: Path
    body: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def doc_id(self) -> str:
        return str(self.metadata.get("doc_id") or self.path.stem)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta_raw = parts[1]
    body = parts[2].lstrip("\n")
    meta = yaml.safe_load(meta_raw) or {}
    if not isinstance(meta, dict):
        raise ValueError("Frontmatter must be a YAML mapping")
    return meta, body


def load_corpus(corpus_dir: Path) -> list[CorpusDocument]:
    """Load all *.md files under corpus_dir (recursive)."""
    docs: list[CorpusDocument] = []
    for path in sorted(corpus_dir.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        metadata, body = _parse_frontmatter(raw)
        if not body.strip():
            continue
        docs.append(CorpusDocument(path=path, body=body, metadata=metadata))
    return docs
