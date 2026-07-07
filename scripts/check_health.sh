#!/usr/bin/env bash
# Verify the backend is running and healthy.
# Usage: bash scripts/check_health.sh [BASE_URL]
# Default BASE_URL: http://localhost:8000

BASE_URL="${1:-http://localhost:8000}"

echo "Checking MemGuard backend at ${BASE_URL}..."

response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health" 2>/dev/null)

if [ "$response" = "200" ]; then
  body=$(curl -s "${BASE_URL}/health")
  echo "  ✓ Health check PASSED (HTTP 200)"
  echo "  ${body}"

  # Also check MCP tools
  mcp_response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/mcp/tools" 2>/dev/null)
  if [ "$mcp_response" = "200" ]; then
    echo "  ✓ MCP tool server reachable"
  else
    echo "  ✗ MCP tool server returned HTTP ${mcp_response}"
  fi

  # Check OpenAPI docs
  docs_response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/docs" 2>/dev/null)
  if [ "$docs_response" = "200" ]; then
    echo "  ✓ OpenAPI docs reachable at ${BASE_URL}/docs"
  fi

  exit 0
else
  echo "  ✗ Health check FAILED (HTTP ${response})"
  echo "  Make sure the backend is running: make up OR cd backend && uvicorn app.main:app --reload"
  exit 1
fi
