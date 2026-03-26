#!/usr/bin/env bash
set -euo pipefail

COMPOSE="docker compose -f docker-compose.prod.yml"
SERVICE="myportfolio"
HEALTH_TIMEOUT=30

# Ensure nginx and mysql are running (no-op if already up)
$COMPOSE up -d mysql nginx

# Build the new app image
$COMPOSE build "$SERVICE"

# Capture old container ID(s)
OLD_IDS=$($COMPOSE ps -q "$SERVICE")

# Scale to 2: start new container alongside the old one
$COMPOSE up -d --no-deps --scale "$SERVICE=2" "$SERVICE"

# Wait for the new container to pass healthcheck
echo "Waiting for new container to be healthy..."
for i in $(seq 1 "$HEALTH_TIMEOUT"); do
  NEW_ID=$($COMPOSE ps -q "$SERVICE" | grep -v -F "$OLD_IDS" | head -1)
  if [ -n "$NEW_ID" ] && [ "$(docker inspect -f '{{.State.Health.Status}}' "$NEW_ID" 2>/dev/null)" = "healthy" ]; then
    echo "New container $NEW_ID is healthy"
    break
  fi
  if [ "$i" -eq "$HEALTH_TIMEOUT" ]; then
    echo "ERROR: New container failed to become healthy within ${HEALTH_TIMEOUT}s"
    exit 1
  fi
  echo "Waiting... ($i/$HEALTH_TIMEOUT)"
  sleep 2
done

# Stop old container(s)
if [ -n "$OLD_IDS" ]; then
  echo "$OLD_IDS" | xargs docker stop
  echo "$OLD_IDS" | xargs docker rm
fi

# Scale back to 1
$COMPOSE up -d --no-deps --scale "$SERVICE=1" --no-recreate "$SERVICE"
