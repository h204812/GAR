#!/usr/bin/env bash
# Phase 0B steps 1–2: start Postgres, Neo4j, Qdrant.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env file"
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  echo "ERROR: Docker Compose not found."
  echo "Install with:  sudo apt install docker-compose-v2"
  echo "Then add yourself to the docker group:"
  echo "  sudo usermod -aG docker \"\$USER\" && newgrp docker"
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: cannot talk to Docker daemon (permission denied?)."
  echo "Fix with:"
  echo "  sudo usermod -aG docker \"\$USER\""
  echo "  newgrp docker   # or log out/in"
  echo "Or run once with: sudo \"\${COMPOSE[*]}\" up -d"
  exit 1
fi

echo "Starting stores: postgres, neo4j, qdrant ..."
"${COMPOSE[@]}" up -d
echo
"${COMPOSE[@]}" ps
echo
echo "Endpoints:"
echo "  Postgres  localhost:${POSTGRES_PORT:-5432}  (user/db from .env)"
echo "  Neo4j     http://localhost:${NEO4J_HTTP_PORT:-7474}  bolt://localhost:${NEO4J_BOLT_PORT:-7687}"
echo "  Qdrant    http://localhost:${QDRANT_HTTP_PORT:-6333}"
