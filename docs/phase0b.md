# Phase 0B — Live data stores

## Goal

Run Postgres, Neo4j, and Qdrant in Docker, then load Phase 0A seed files.

## Steps 1–2 (this session)

1. `docker-compose.yml` + `.env` / `.env.example`
2. Start containers: `docker compose up -d`

### One-time host setup (if needed)

```bash
sudo apt update
sudo apt install docker-compose-v2
sudo usermod -aG docker "$USER"
newgrp docker   # or log out and back in

docker info
docker compose version
```

### Start stores

```bash
cd /home/hrushik/proj
cp -n .env.example .env
bash scripts/up_stores.sh
# or: docker compose up -d
```

### Ports

| Service | Ports |
|---------|--------|
| Postgres | `5432` |
| Neo4j | `7474` (HTTP), `7687` (Bolt) |
| Qdrant | `6333` (HTTP), `6334` (gRPC) |

Default passwords are in `.env.example` (lab only — not for production).

## Steps 3–5 (next)

- Load `data/sql/schema.sql` + `seed.sql` into Postgres  
- Load `data/graph/seed.cypher` into Neo4j  
- Confirm Qdrant health (collections in Phase 1)

## Steps 3–5 — load seeds

```bash
bash scripts/load_stores.sh
```

Loads `data/sql/schema.sql` + `seed.sql` into Postgres and `data/graph/seed.cypher` into Neo4j, then runs smoke queries. Qdrant stays empty until Phase 1.

## Status

| Step | Status |
|------|--------|
| 1 Compose file | Done |
| 2 `up -d` | Done (host) |
| 3 Load SQL | Done via `scripts/load_stores.sh` |
| 4 Load Cypher | Done |
| 5 Smoke checks | Done (Qdrant empty until Phase 1) |
