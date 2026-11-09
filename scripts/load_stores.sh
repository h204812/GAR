#!/usr/bin/env bash
# Phase 0B: load Phase 0A SQL + Cypher seeds into running containers.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

POSTGRES_USER="${POSTGRES_USER:-acme}"
POSTGRES_DB="${POSTGRES_DB:-acme}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-acmecopilot}"

if ! docker compose ps --status running 2>/dev/null | grep -q acme-postgres; then
  echo "ERROR: acme-postgres is not running. Start with: bash scripts/up_stores.sh"
  exit 1
fi
if ! docker compose ps --status running 2>/dev/null | grep -q acme-neo4j; then
  echo "ERROR: acme-neo4j is not running."
  exit 1
fi

echo "==> Loading Postgres schema"
docker exec -i acme-postgres \
  psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  < data/sql/schema.sql

echo "==> Loading Postgres seed"
docker exec -i acme-postgres \
  psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  < data/sql/seed.sql

echo "==> Loading Neo4j Cypher seed"
docker exec -i acme-neo4j \
  cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
  < data/graph/seed.cypher

echo "==> Smoke checks"
echo -n "Postgres ticket count: "
docker exec -i acme-postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT COUNT(*) FROM tickets;"

echo -n "Postgres Payments Sev-1 Q3 2024: "
docker exec -i acme-postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc \
  "SELECT COUNT(*) FROM tickets WHERE team_id='payments' AND severity='Sev-1' AND created_at >= '2024-07-01' AND created_at < '2024-10-01';"

echo -n "Neo4j service count: "
docker exec -i acme-neo4j \
  cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain \
  "MATCH (s:Service) RETURN count(s) AS c;" | tail -n 1

echo -n "Neo4j checkout-api owner: "
docker exec -i acme-neo4j \
  cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" --format plain \
  "MATCH (s:Service {name:'checkout-api'})-[:OWNED_BY]->(t:Team) RETURN t.id;" | tail -n 1

echo -n "Qdrant ready: "
curl -sf http://localhost:"${QDRANT_HTTP_PORT:-6333}"/readyz
echo
echo "Qdrant collections (empty until Phase 1):"
curl -sf http://localhost:"${QDRANT_HTTP_PORT:-6333}"/collections
echo
echo
echo "Phase 0B load complete."
