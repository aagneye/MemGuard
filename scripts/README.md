# MemGuard Scripts

Helper scripts for demo preparation, deployment verification, and local development.

## Available scripts

| Script | Purpose |
|---|---|
| `seed_demo_data.py` | Pre-load Alice, Bob, and Carol with demo memories for each of the 5 beats. Run this before recording the demo video. |
| `replay_demo_beats.py` | Scripted walkthrough of all 5 demo beats. Returns a pass/fail for each. Run before recording to confirm the backend works end-to-end. |

## Quick usage

```bash
# Start the backend first (from infra/)
docker compose up -d backend

# Seed demo data
python scripts/seed_demo_data.py --base-url http://localhost:8000

# Verify all 5 beats pass
python scripts/replay_demo_beats.py --base-url http://localhost:8000 --verbose
```

## Requirements

```bash
pip install httpx
```
