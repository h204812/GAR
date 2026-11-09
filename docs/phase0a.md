# Phase 0A — Data on disk (no Docker)

## Goal

Create the synthetic Acme universe as files so Phase 1 (indexing) and later SQL/graph loads have a coherent source of truth.

## Deliverables

| Path | Contents |
|------|----------|
| `data/manifest.yaml` | Single source of truth (teams, services, incidents, policy facts) |
| `data/corpus/**/*.md` | Scripted markdown docs with YAML frontmatter |
| `data/sql/schema.sql` | Postgres schema |
| `data/sql/seed.sql` | Insert statements |
| `data/sql/snapshot.json` | JSON snapshot for inspection |
| `data/graph/seed.cypher` | Neo4j wipe + constraints + graph |
| `data/eval.jsonl` | 50 labeled golden questions |
| `data/seed_summary.json` | Counts from last seed run |

## How to run

```bash
uv sync
uv run python scripts/seed_universe.py
```

No API keys. No Docker. Offline.

## Explicitly deferred to Phase 0B

- `docker-compose.yml` (Qdrant, Postgres, Neo4j)
- Loading `seed.sql` / `seed.cypher` into live databases
- Embedding / Qdrant indexing (Phase 1)

## Definition of done

- [x] Manifest committed
- [x] Seed script regenerates all artifacts deterministically
- [x] ~45+ corpus docs
- [x] ~200 tickets + employees in SQL seed
- [x] Graph seed with OWNED_BY / DEPENDS_ON / AFFECTED
- [x] 50 eval questions with routes and gold doc ids
