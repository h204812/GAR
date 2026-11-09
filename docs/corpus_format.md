# Corpus format (Phase 0A)

Standard format for Acme unstructured documents.

## Layout

```text
data/corpus/
  policies/*.md
  wiki/*.md
  runbooks/*.md
  postmortems/*.md
  architecture/*.md
  security/*.md
```

## File format

- Encoding: UTF-8
- Extension: `.md`
- Metadata: YAML frontmatter
- Body: Markdown

### Required frontmatter fields

| Field | Description |
|-------|-------------|
| `doc_id` | Unique id (used in eval gold citations) |
| `doc_type` | `policy` \| `wiki` \| `runbook` \| `postmortem` \| `architecture` |
| `last_updated` | ISO date `YYYY-MM-DD` |
| `source` | Always `synthetic` for Phase 0A |
| `title` | Human title |

### Optional fields (for self-query later)

`department`, `team`, `service`, `incident_id`, `severity`, `classification`

## Generation

```bash
uv sync
uv run python scripts/seed_universe.py
```

Corpus is **scripted from** `data/manifest.yaml` (no LLM). Regenerate anytime; seed is fixed (`seed: 42`).
