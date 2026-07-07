# MemGuard Scripts

Helper scripts for demo preparation, deployment verification, and local development.

## Available scripts

| Script | Purpose |
|---|---|
| `seed_demo_data.py` | Pre-load Alice, Bob, and Carol with demo memories for each of the 5 beats. Run this before recording the demo video. |
| `replay_demo_beats.py` | Scripted walkthrough of all 5 demo beats. Returns a pass/fail for each. Run before recording to confirm the backend works end-to-end. |
| `check_health.sh` | Verify backend health, MCP tools, and OpenAPI docs are reachable. |
| `export_memories.py` | Export a user's memories to JSON or CSV. |
| `setup.sh` | One-command local dev bootstrap (`.env`, deps, Postgres/Redis). |

Full environment setup: [docs/SETUP.md](../docs/SETUP.md).

## Quick usage

```bash
# Start the backend first (from repo root)
docker compose -f infra/docker-compose.yml up -d backend

# Seed demo data
python scripts/seed_demo_data.py --base-url http://localhost:8000

# Verify all 5 beats pass
python scripts/replay_demo_beats.py --base-url http://localhost:8000 --verbose
```

## Requirements

```bash
pip install httpx
```
