# MemGuard Documentation

All project documentation lives in this folder.

## Start here

| Document | Purpose |
|---|---|
| [SETUP.md](SETUP.md) | **Local dev, Qwen/Ollama config, Docker, troubleshooting** |
| [PRODUCTION.md](PRODUCTION.md) | **Deploy to Alibaba Cloud ECS — full production guide** |
| [DEMO_GUIDE.md](DEMO_GUIDE.md) | Beat-by-beat script for recording the 3-minute demo video |
| [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) | Devpost requirements mapped to repo artifacts |

## Architecture & planning

| Document | Purpose |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Full system design, data model, governance logic, API contract |
| [FRONTEND_SPEC.md](FRONTEND_SPEC.md) | Demo screens (Chat, Memory Inspector, Landing) and UI contract |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Monorepo layout and file map |
| [BUILD_PLAN.md](BUILD_PLAN.md) | Original day-by-day hackathon build order |
| [FUTURE_WORK.md](FUTURE_WORK.md) | Post-submission development backlog |

## Deployment & ops

| Document | Purpose |
|---|---|
| [../infra/alibaba-cloud/ecs-setup.md](../infra/alibaba-cloud/ecs-setup.md) | ECS provisioning and deployment proof steps |
| [../infra/alibaba-cloud/rds-setup.md](../infra/alibaba-cloud/rds-setup.md) | Optional managed Postgres + pgvector |
| [generate-architecture-png.md](generate-architecture-png.md) | How to export the architecture diagram for submission |

## Scripts

See [../scripts/README.md](../scripts/README.md) for `seed_demo_data.py`, `replay_demo_beats.py`, and other helpers.
