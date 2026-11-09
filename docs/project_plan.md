# Acme Knowledge Copilot — Project Plan

Reference document for the hands-on RAG pipeline lab. Implements every stage of the standard LangChain RAG pipeline diagram (indexing → query translation → routing → query construction → retrieval → generation).

**Status:** Phases **0A–2** complete (naive RAG CLI over Qdrant). Parent-doc / RAPTOR optional; Phase 3 = query translation.

---

## 1. Goals

| Goal | Detail |
|------|--------|
| Learn RAG end-to-end | Build each technique as code, not only read about it |
| One coherent product | Fictional company **Acme** with vector, SQL, and graph answers |
| Measurable progress | Same **50** golden questions after every phase; compare RAGAS metrics |
| Standard tooling | LangGraph, LangChain, Qdrant, Postgres, Neo4j |

---

## 2. Product summary

**Acme Knowledge Copilot** — single question box for internal knowledge: policies, runbooks, tickets, org structure, service dependencies.

| Store | Technology | Content |
|-------|------------|---------|
| Vector | Qdrant | Wiki, runbooks, policies, postmortems, architecture notes |
| Relational | Postgres | Employees, teams, tickets, SLAs, assets, incidents |
| Graph | Neo4j | Services, dependencies, ownership, incident impact |

---

## 3. Standard stack

| Layer | Choice |
|-------|--------|
| Orchestration | LangGraph |
| Retrievers | LangChain |
| Vectors | Qdrant |
| SQL | Postgres + SQLAlchemy |
| Graph | Neo4j Community |
| Embeddings | OpenAI `text-embedding-3-small` (local swap later) |
| LLM | `gpt-4o-mini` or Ollama |
| API | FastAPI (`/ask`) |
| Lab UI | Streamlit (per-technique toggles) |
| Evaluation | RAGAS + pytest |

---

## 4. Where data comes from

All **Acme** data is **synthetic and generated in-repo**. No scraping, no production exports.

| Asset | Source |
|-------|--------|
| Unstructured docs | `data/manifest.yaml` + scripted templates (`scripts/seed_universe.py`); LLM expansion deferred |
| Postgres rows | Same manifest → `scripts/seed_universe.py` |
| Neo4j graph | Same manifest → Cypher or seed script |
| Golden eval (`data/eval.jsonl`) | Hand-written + templated from known IDs/counts in seed |

**Optional later:** public HF/BEIR corpora as a *second* index for retrieval benchmarks only (not wired to SQL/graph).

**Production analogy (out of scope for now):** Confluence, Jira, warehouse replicas, service catalog — add as a separate ingestion phase after the pipeline is understood.

### Data scale (targets)

- 45–60 markdown docs with YAML frontmatter (self-query metadata)
- ~200 tickets, ~80 employees, ~12 teams in Postgres
- ~40 services, dependency/ownership edges in Neo4j
- 50 labeled eval questions

### Coherence rule

Same entity names everywhere: e.g. `checkout-api`, `payments-ledger`, `INC-2024-0912`, Payments team.

---

## 5. Pipeline coverage (diagram → phases)

| Diagram block | Techniques | Phase |
|---------------|------------|-------|
| **Indexing** | Semantic splitter, parent document, multi-representation summaries, RAPTOR, ColBERT* | 1 |
| **Query translation** | Multi-query, RAG-Fusion, decomposition, step-back, HyDE | 3 |
| **Routing** | Logical (LLM), semantic (embedding) | 4 |
| **Query construction** | Text-to-SQL, Text-to-Cypher, self-query retriever | 5 |
| **Retrieval** | Re-rank, RankGPT, CRAG (+ web fallback) | 6 |
| **Generation** | Self-RAG, rewrite-retrieve-read (RRR) | 7 |

\* ColBERT in-scope as drop-in; full embedding fine-tune is optional.

---

## 6. Build phases

| Phase | Deliverable |
|-------|-------------|
| **0A** | Manifest, scripted corpus, SQL/Cypher seed files, 50-question `eval.jsonl` (no Docker, no LLM) — **done** |
| **0B** | docker-compose (Qdrant, Postgres, Neo4j) + load seed files into live stores |
| **1** | Indexing: chunk experiments, parent-doc, summaries, RAPTOR |
| **2** | Naive RAG baseline + first RAGAS scoreboard |
| **3** | Query translation modules + Streamlit toggles |
| **4** | Logical + semantic routing |
| **5** | Text-to-SQL, Text-to-Cypher, self-query filters |
| **6** | Re-ranking, CRAG |
| **7** | Self-RAG / RRR |
| **8** | Full LangGraph, ablation study, lab UI polish |

### How we work each session

1. Implement one phase in code.
2. Run the 50 golden questions.
3. Compare faithfulness, context recall, relevancy, latency, cost vs previous phase.
4. Do not wire the full graph until Phase 2 baseline exists.

### Definition of done (per phase)

1. Typed Python module with tests (not a notebook-only spike).
2. Streamlit can enable/disable the technique on one question.
3. Eval runner appends a metrics row.
4. You can state when the technique helps vs hurts.

---

## 7. Golden question types

| Type | Example | Must use |
|------|---------|----------|
| Factual policy | PTO accrual for engineers | Vector + citation |
| Filtered docs | Payments runbook updated after 2024 | Self-query metadata |
| Structured count | Sev-1 tickets for Payments last quarter | Text-to-SQL |
| Multi-hop graph | If checkout-api is down, which teams? | Text-to-Cypher |
| Hybrid | Latest checkout outage + owner | SQL + graph + vector |
| Poor retrieval | USD to INR for expenses | CRAG web |
| Ambiguous | Why are payments slow? | Decomposition + Self-RAG |

---

## 8. Repository layout (target)

```text
acme-copilot/                    # project root
  docs/
    project_plan.md              # this file
  data/
    manifest.yaml
    corpus/
    sql/
    graph/
    eval.jsonl
  scripts/
    seed_universe.py
    generate_corpus.py
    index_corpus.py
  src/acme_copilot/
    indexing/
    translation/
    routing/
    construction/
    retrieval/
    generation/
    graph/
    eval/
  app/                           # FastAPI + Streamlit
  tests/
  docker-compose.yml
  pyproject.toml
```

---

## 9. Out of scope (until copilot works)

- Auth, multi-tenant
- Production observability
- GPU embedding fine-tuning
- Live Confluence/Jira connectors
- Agent tool-calling beyond CRAG web search

---

## 10. References

- In-IDE plan canvas: `RAG-pipeline-project.canvas.tsx` (Cursor canvases folder for this workspace)
- LangChain RAG from scratch / LangGraph documentation
- RAGAS evaluation metrics

---

## Changelog

| Date | Change |
|------|--------|
| 2026-11-09 | Initial `docs/project_plan.md`; git repo initialized |
| 2026-11-09 | Phase 0A: manifest, 52 corpus docs, SQL/graph seeds, 50 eval questions |
| 2026-11-09 | Phase 0B: added `docker-compose.yml` (Postgres, Neo4j, Qdrant) |
| 2026-11-09 | Phase 0B: loaded SQL + Cypher seeds; smoke checks passed |
| 2026-11-09 | Phase 1 baseline: chunk + OpenAI embed + Qdrant `acme_chunks` |
| 2026-11-09 | Phase 2: naive RAG CLI (`scripts/ask.py`) |
