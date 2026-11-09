#!/usr/bin/env python3
"""Phase 1: index Acme markdown corpus into Qdrant (dense vectors + metadata payload)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from acme_copilot.indexing.pipeline import index_corpus, search_corpus  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=ROOT / "data" / "corpus",
        help="Corpus directory",
    )
    parser.add_argument("--collection", default="acme_chunks")
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--chunk-overlap", type=int, default=120)
    parser.add_argument(
        "--no-recreate",
        action="store_true",
        help="Do not wipe collection before upsert",
    )
    parser.add_argument(
        "--smoke-query",
        default="What is Acme PTO accrual for engineers?",
        help="Run a similarity search after indexing (empty string to skip)",
    )
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    summary = index_corpus(
        args.corpus,
        collection=args.collection,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        recreate=not args.no_recreate,
    )
    print("Indexing complete")
    print(json.dumps(summary, indent=2))

    if args.smoke_query:
        print(f"\nSmoke search: {args.smoke_query!r}")
        hits = search_corpus(
            args.smoke_query, collection=args.collection, limit=args.top_k
        )
        for i, hit in enumerate(hits, start=1):
            text = (hit.get("text") or "").replace("\n", " ")
            preview = text[:160] + ("…" if len(text) > 160 else "")
            print(
                f"{i}. score={hit['score']:.4f} doc_id={hit.get('doc_id')} "
                f"chunk_id={hit.get('chunk_id')}"
            )
            print(f"   {preview}")

        top_docs = [h.get("doc_id") for h in hits]
        if "pto-policy" not in top_docs:
            print(
                "\nWARNING: expected doc_id 'pto-policy' in top-k for PTO smoke query",
                file=sys.stderr,
            )
            return 1
        print("\nSmoke check OK (pto-policy in top-k)")

    (ROOT / "data" / "index_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
