#!/usr/bin/env python3
"""Phase 0A: generate synthetic Acme corpus, SQL, graph, and eval from manifest.

No Docker, no LLM, no network required.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from acme_copilot.seed.corpus import generate_corpus  # noqa: E402
from acme_copilot.seed.employees import build_employees  # noqa: E402
from acme_copilot.seed.eval_set import generate_eval  # noqa: E402
from acme_copilot.seed.graph_seed import generate_graph  # noqa: E402
from acme_copilot.seed.manifest import load_manifest  # noqa: E402
from acme_copilot.seed.sql_seed import generate_sql  # noqa: E402
from acme_copilot.seed.tickets import build_tickets  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "data" / "manifest.yaml",
        help="Path to manifest.yaml",
    )
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    data_dir = ROOT / "data"

    employees = build_employees(manifest)
    tickets = build_tickets(manifest, employees)

    doc_ids = generate_corpus(manifest, data_dir / "corpus")
    generate_sql(manifest, employees, tickets, data_dir / "sql")
    generate_graph(manifest, employees, data_dir / "graph")
    n_eval = generate_eval(manifest, tickets, doc_ids, data_dir / "eval.jsonl")

    summary = {
        "seed": manifest["seed"],
        "employees": len(employees),
        "tickets": len(tickets),
        "teams": len(manifest["teams"]),
        "services": len(manifest["services"]),
        "incidents": len(manifest["incidents"]),
        "corpus_docs": len(doc_ids),
        "eval_questions": n_eval,
        "outputs": {
            "corpus": str(data_dir / "corpus"),
            "sql": str(data_dir / "sql"),
            "graph": str(data_dir / "graph" / "seed.cypher"),
            "eval": str(data_dir / "eval.jsonl"),
        },
    }
    (data_dir / "seed_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print("Phase 0A seed complete")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
