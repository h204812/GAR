# Acme Knowledge Copilot

Hands-on lab for building a **production-style RAG pipeline** end to end. You implement each stage from the standard RAG diagram—indexing, query translation, routing, query construction, retrieval, and generation—on one fictional product: an internal copilot for **Acme**.

Three stores answer real questions together:

- **Qdrant** — policies, runbooks, wikis, postmortems  
- **Postgres** — employees, tickets, SLAs  
- **Neo4j** — services, dependencies, on-call ownership  

Data is **synthetic** (generated in-repo from a shared manifest), so SQL, graph, and document answers stay consistent and you always have gold labels.

## Documentation

| Document | Purpose |
|----------|---------|
| [docs/project_plan.md](docs/project_plan.md) | Full reference: phases, techniques, data plan |
| [docs/phase0a.md](docs/phase0a.md) | Phase 0A deliverables and how to regenerate data |
| [docs/corpus_format.md](docs/corpus_format.md) | Markdown + YAML frontmatter corpus standard |
| [docs/phase1.md](docs/phase1.md) | Dense indexing into Qdrant |

## Tech stack

LangGraph · LangChain · Qdrant · Postgres · Neo4j · FastAPI · Streamlit · RAGAS

## Project status

| Phase | Description | Status |
|-------|-------------|--------|
| **0A** | Manifest, scripted corpus, SQL/graph seeds, 50 eval questions | **Done** |
| **0B** | Docker stores + load SQL/Cypher | **Done** |
| **1** | Indexing — baseline dense chunks → Qdrant | **Done** (parent-doc / RAPTOR later) |
| 2 | Naive RAG baseline | Pending |
| 3–8 | Translation, routing, construction, CRAG, Self-RAG, full graph | Pending |

## Phase 0A quick start (data only)

```bash
cd /home/hrushik/proj

# Prefer a local venv if `uv` snap has permission issues
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Regenerate corpus, SQL, Cypher, eval from data/manifest.yaml
python scripts/seed_universe.py

pytest tests/test_phase0a_seed.py -q
```

Or with uv (when it works on your machine):

```bash
uv sync
uv run python scripts/seed_universe.py
```

### Generated artifacts

| Path | What |
|------|------|
| `data/corpus/` | 52 markdown docs with YAML frontmatter |
| `data/sql/` | `schema.sql`, `seed.sql`, `snapshot.json` |
| `data/graph/seed.cypher` | Neo4j graph seed |
| `data/eval.jsonl` | 50 golden questions |
| `data/seed_summary.json` | Counts from last run |

## Repository layout

```text
docs/                 Project plan and phase notes
data/                 Manifest + generated corpus/sql/graph/eval
scripts/              seed_universe.py
src/acme_copilot/     Package (seed modules now; RAG stages later)
tests/                Phase tests
pyproject.toml
```

## Phase 0B — start data stores

```bash
# One-time (if compose / docker group missing)
sudo apt install docker-compose-v2
sudo usermod -aG docker "$USER" && newgrp docker

cp -n .env.example .env
bash scripts/up_stores.sh
bash scripts/load_stores.sh   # schema + seed.sql + seed.cypher + smoke checks
```

See [docs/phase0b.md](docs/phase0b.md).

## Phase 1 — index corpus into Qdrant

```bash
# OPENAI_API_KEY must be set in .env
python scripts/index_corpus.py
```

Creates collection `acme_chunks` (vectors + frontmatter payload). See [docs/phase1.md](docs/phase1.md).

## Prerequisites

| Phase | Need |
|-------|------|
| **0A** | Python 3.11+ |
| **0B** | Docker + Docker Compose + docker group membership |
| **1+** | Embeddings/LLM (OpenAI or Ollama) |

## How to learn with this repo

1. Implement **one phase** at a time.  
2. Run the same **50** golden questions after each phase.  
3. Compare RAGAS metrics to the previous phase.  
4. Use Streamlit toggles (later) to see which technique helps on which question type.

## License

Not set yet. Add a license file before publishing.
