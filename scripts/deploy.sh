#!/usr/bin/env bash
set -euo pipefail

cd /root/portfolio

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
