#!/usr/bin/env bash
set -euo pipefail

URL="https://4brar.me"
MAX_RETRIES=10
RETRY_DELAY=3

echo "Running smoke tests against ${URL}..."

# Wait for the app to be reachable after deploy
for i in $(seq 1 "$MAX_RETRIES"); do
  status=$(curl -sk -o /dev/null -w '%{http_code}' "${URL}/")
  if [ "$status" = "200" ]; then
    echo "App is reachable after ${i} attempts"
    break
  fi
  if [ "$i" -eq "$MAX_RETRIES" ]; then
    echo "FAIL: App never became reachable (last status: ${status})"
    exit 1
  fi
  echo "Waiting for app... (${i}/${MAX_RETRIES})"
  sleep "$RETRY_DELAY"
done

# Test critical routes
routes="/ /aboutme /work /education /hobbies /travels /timeline"
for route in $routes; do
  status=$(curl -sk -o /dev/null -w '%{http_code}' "${URL}${route}")
  if [ "$status" != "200" ]; then
    echo "FAIL: ${route} returned ${status}"
    exit 1
  fi
  echo "OK: ${route} returned 200"
done

# Test API endpoints
status=$(curl -sk -o /dev/null -w '%{http_code}' "${URL}/api/timeline_post")
if [ "$status" != "200" ]; then
  echo "FAIL: GET /api/timeline_post returned ${status}"
  exit 1
fi
echo "OK: GET /api/timeline_post returned 200"

# Test metrics endpoint
status=$(curl -sk -o /dev/null -w '%{http_code}' "${URL}/metrics")
if [ "$status" != "200" ]; then
  echo "FAIL: /metrics returned ${status}"
  exit 1
fi
echo "OK: /metrics returned 200"

echo "All smoke tests passed!"
