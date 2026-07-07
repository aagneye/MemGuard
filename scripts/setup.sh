#!/usr/bin/env bash
# One-command local dev setup for MemGuard.
# Run: bash scripts/setup.sh
set -e

echo "==> MemGuard local dev setup"

# 1. Copy .env.example if .env doesn't exist
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  Created .env from .env.example — fill in your QWEN_API_KEY if needed."
else
  echo "  .env already exists, skipping copy."
fi

# 2. Check for Docker
if ! command -v docker &> /dev/null; then
  echo "  ERROR: Docker not found. Install from https://docs.docker.com/get-docker/"
  exit 1
fi

# 3. Start Postgres + Redis (skip if already running)
echo "==> Starting Postgres + Redis via docker compose..."
docker compose -f infra/docker-compose.yml up -d postgres redis

echo "==> Waiting for Postgres to be healthy..."
sleep 5

# 4. Install backend Python deps
if command -v python3 &> /dev/null; then
  echo "==> Installing backend dependencies..."
  cd backend
  python3 -m pip install -e ".[dev]" --quiet
  cd ..
else
  echo "  Python3 not found, skipping backend install. Run manually: cd backend && pip install -e '.[dev]'"
fi

# 5. Install frontend Node deps
if command -v npm &> /dev/null; then
  echo "==> Installing frontend dependencies..."
  cd frontend && npm install --silent && cd ..
else
  echo "  npm not found, skipping frontend install."
fi

echo ""
echo "Setup complete! Start the full stack with:"
echo "  docker compose -f infra/docker-compose.yml up"
echo ""
echo "Or start individually:"
echo "  cd backend && uvicorn app.main:app --reload"
echo "  cd frontend && npm run dev"
