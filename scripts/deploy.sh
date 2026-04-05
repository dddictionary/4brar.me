#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/root/portfolio"
cd "$REPO_DIR"

# ── Save current commit for rollback ─────────────────────────────────
PREV_SHA=$(git rev-parse HEAD)
echo "Previous commit: ${PREV_SHA}"

# ── Create shared networks (idempotent) ──────────────────────────────
docker network create portfolio_net 2>/dev/null || true
docker network create monitoring_net 2>/dev/null || true

# ── Authenticate with GHCR ───────────────────────────────────────────
echo "${GHCR_PAT}" | docker login ghcr.io -u dddictionary --password-stdin

# ── Pull and restart all stacks ──────────────────────────────────────
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.monitoring.yml up -d
docker compose -f docker-compose.router.yml up -d

# ── Smoke test ───────────────────────────────────────────────────────
if ! bash scripts/smoke-test.sh; then
  echo "Smoke tests failed! Rolling back to ${PREV_SHA}..."
  git reset --hard "$PREV_SHA"
  docker compose -f docker-compose.prod.yml pull
  docker compose -f docker-compose.prod.yml up -d
  docker compose -f docker-compose.router.yml up -d
  echo "Rollback complete."
  exit 1
fi

echo "Deploy successful!"
