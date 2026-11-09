#!/usr/bin/env python3
"""Phase 2 naive RAG CLI: question → Qdrant cosine top-k → OpenAI answer.

Only retrieves from Qdrant. No query translation. No SQL/graph.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from acme_copilot.generation.naive_rag import ask  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to ask (or pass via --question)",
    )
    parser.add_argument("--question", "-q", dest="question_flag", help="Question text")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--collection", default="acme_chunks")
    parser.add_argument("--model", default=None, help="Chat model (default gpt-4o-mini)")
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print retrieved chunks before the answer",
    )
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    question = args.question_flag or args.question
    if not question:
        parser.error("Provide a question as a positional arg or with -q/--question")

    result = ask(
        question,
        top_k=args.top_k,
        collection=args.collection,
        model=args.model,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "question": result.question,
                    "answer": result.answer,
                    "citations": result.citations,
                    "model": result.model,
                    "top_k": result.top_k,
                    "collection": result.collection,
                    "contexts": [
                        {
                            "doc_id": c.get("doc_id"),
                            "chunk_id": c.get("chunk_id"),
                            "score": c.get("score"),
                            "text": c.get("text"),
                        }
                        for c in result.contexts
                    ],
                },
                indent=2,
            )
        )
        return 0

    print(f"Q: {result.question}")
    print(f"collection={result.collection}  top_k={result.top_k}  model={result.model}")
    print(f"similarity=cosine (dense)  stores=qdrant-only  query_translation=none")
    print()

    if args.show_context:
        print("Retrieved contexts:")
        for i, hit in enumerate(result.contexts, start=1):
            text = (hit.get("text") or "").replace("\n", " ")
            preview = text[:140] + ("…" if len(text) > 140 else "")
            print(
                f"  {i}. score={hit.get('score'):.4f} "
                f"doc_id={hit.get('doc_id')} chunk_id={hit.get('chunk_id')}"
            )
            print(f"     {preview}")
        print()

    print("A:", result.answer)
    print()
    print("Citations:", ", ".join(result.citations) or "(none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
