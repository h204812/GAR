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
| [docs/project_plan.md](docs/project_plan.md) | Full reference: phases, techniques, data plan, repo layout, definition of done |

## Tech stack

LangGraph · LangChain · Qdrant · Postgres · Neo4j · FastAPI · Streamlit · RAGAS

## Project status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffold, Docker, synthetic data, eval set | Not started |
| 1 | Indexing (chunking, parent-doc, RAPTOR) | Pending |
| 2 | Naive RAG baseline | Pending |
| 3–8 | Translation, routing, construction, CRAG, Self-RAG, full graph | Pending |

Details and checkpoints are in [docs/project_plan.md](docs/project_plan.md).

## Repository layout (planned)

```text
docs/                 Project plan and references
data/                 Manifest, corpus, SQL/graph seeds, eval.jsonl
scripts/              Seed and indexing scripts
src/acme_copilot/     Pipeline modules by stage
app/                  FastAPI + Streamlit lab
tests/                Per-technique tests
docker-compose.yml    Qdrant, Postgres, Neo4j
```

## Prerequisites (for Phase 0+)

- Python 3.11+ and [uv](https://docs.astral.sh/uv/) (recommended) or pip  
- Docker and Docker Compose  
- OpenAI API key **or** local Ollama for LLM/embeddings  

## Quick start

Phase 0 is not implemented yet. When it lands, the flow will be:

```bash
# Clone and enter the repo
cd acme-copilot

# Start data stores
docker compose up -d

# Install dependencies (after pyproject.toml exists)
uv sync

# Seed synthetic Acme data and build indexes
uv run python scripts/seed_universe.py
uv run python scripts/index_corpus.py

# Run the lab UI
uv run streamlit run app/lab.py
```

## How to learn with this repo

1. Implement **one phase** at a time.  
2. Run the same **50** golden questions after each phase.  
3. Compare RAGAS metrics to the previous phase.  
4. Use Streamlit toggles to see which technique helps on which question type.

## License

Not set yet. Add a license file before publishing.
