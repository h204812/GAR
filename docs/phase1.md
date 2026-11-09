# Phase 1 — Indexing (baseline dense vectors)

## Goal

Index `data/corpus/**/*.md` into Qdrant:

1. Parse YAML frontmatter → **payload metadata**
2. Chunk markdown body
3. Embed with OpenAI `text-embedding-3-small`
4. Upsert vectors + payload into collection `acme_chunks`

Similarity search ranks by vectors only. Payload is for citations / later filters (Phase 5).

## Prerequisites

- Qdrant running (`docker compose up -d qdrant`)
- `OPENAI_API_KEY` in `.env`

## Run

```bash
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/index_corpus.py
```

Options:

```bash
python scripts/index_corpus.py --chunk-size 500 --chunk-overlap 80
python scripts/index_corpus.py --smoke-query "expense meal cap"
```

## Smoke check

Default query expects `pto-policy` in top-k for the PTO question.

## Not in this slice (later Phase 1)

- Parent-document retriever
- Multi-representation / summary index
- RAPTOR
- ColBERT
