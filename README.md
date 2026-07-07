# MemGuard

Trust-aware memory agent demo for Qwen Cloud Global AI Hackathon (Track 1: MemoryAgent).

## Current Progress

This commit set delivers roughly 35-45% of the build:

- FastAPI backend with core endpoints:
  - `POST /chat`
  - `GET /memories`
  - `POST /memories/{id}/resolve`
  - `GET /health`
- Baseline governance logic:
  - trust scoring by source
  - poisoning flag path
  - basic conflict detection + resolve actions
  - memory event emission
- Next.js frontend:
  - chat UI
  - session selector
  - Memory Inspector panel
  - conflict resolve actions
- Local infra:
  - backend + frontend docker setup
  - env template

## Quick Start

1. Copy `.env.example` to `.env` and set values.
2. Start backend:
   - `cd backend`
   - `pip install -e .`
   - `uvicorn app.main:app --reload`
3. Start frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

Then open `http://localhost:3000`.

## Next Session Targets

- Replace in-memory store with Postgres + pgvector + Redis.
- Add vector retrieval and model-based conflict adjudication.
- Add decay scheduler/check-on-read with demo time scaling.
- Deploy on Alibaba ECS and attach proof links.
