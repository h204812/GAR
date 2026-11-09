from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_loads():
    data = yaml.safe_load((ROOT / "data" / "manifest.yaml").read_text(encoding="utf-8"))
    assert data["seed"] == 42
    assert len(data["teams"]) == 12
    assert data["ticket_counts"]["payments_sev1_q3_2024"] == 4


def test_seed_artifacts_exist_after_generation():
    summary_path = ROOT / "data" / "seed_summary.json"
    assert summary_path.exists(), "Run: uv run python scripts/seed_universe.py"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["corpus_docs"] >= 45
    assert summary["tickets"] == 200
    assert summary["eval_questions"] == 50
    assert (ROOT / "data" / "eval.jsonl").exists()
    assert (ROOT / "data" / "sql" / "seed.sql").exists()
    assert (ROOT / "data" / "graph" / "seed.cypher").exists()


def test_eval_jsonl_has_fifty_lines():
    path = ROOT / "data" / "eval.jsonl"
    assert path.exists()
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 50
    first = json.loads(lines[0])
    assert first["id"] == "eval-001"
    assert "question" in first
