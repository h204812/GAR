# Phase 2 — Naive RAG (CLI)

## Scope

```text
question
  → embed (OpenAI text-embedding-3-small)
  → Qdrant cosine top-k on acme_chunks
  → LLM (gpt-4o-mini) with retrieved chunk text
  → answer + citations
```

| Topic | Phase 2 choice |
|-------|----------------|
| Similarity | Dense **cosine** over chunk embeddings |
| Stores queried | **Qdrant only** |
| Postgres / Neo4j | Not used |
| Query translation | **None** (Phase 3) |
| UI | CLI only |

## Run

```bash
source .venv/bin/activate
python scripts/ask.py "What is Acme PTO accrual for engineers?"
python scripts/ask.py -q "meal expense cap" --show-context
python scripts/ask.py -q "PTO carryover" --json
```

Requires `OPENAI_API_KEY` and indexed `acme_chunks` (`python scripts/index_corpus.py`).
