#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:3000}"
WEB_URL="${WEB_URL:-http://localhost:8080}"
MAX_RETRIES="${MAX_RETRIES:-10}"
RETRY_INTERVAL="${RETRY_INTERVAL:-3}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_service() {
  local name="$1"
  local url="$2"
  local retries=0

  echo -n "Checking $name ($url)... "

  while [ $retries -lt $MAX_RETRIES ]; do
    if curl -sf "$url" > /dev/null 2>&1; then
      echo -e "${GREEN}OK${NC}"
      return 0
    fi
    retries=$((retries + 1))
    sleep "$RETRY_INTERVAL"
  done

  echo -e "${RED}FAILED${NC} (after $MAX_RETRIES attempts)"
  return 1
}

echo "=== AgentScrumMaster Health Check ==="
echo ""

FAILED=0

check_service "API Server" "$API_URL/api/healthz" || FAILED=$((FAILED + 1))
check_service "Intro Video" "$WEB_URL/health" || FAILED=$((FAILED + 1))

echo ""

if [ $FAILED -eq 0 ]; then
  echo -e "${GREEN}All services healthy${NC}"
  exit 0
else
  echo -e "${RED}$FAILED service(s) unhealthy${NC}"
  exit 1
fi
