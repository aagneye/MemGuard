# MemGuard

Trust-aware memory agent demo for Qwen Cloud Global AI Hackathon (Track 1: MemoryAgent).

## What this is

A public demo site. Open it, chat with "Acme Cloud Support," and watch it remember you across sessions while refusing to be fooled by conflicting or poisoned facts. No login, no payment, no API keys required from a visitor.

- `/` — Screen C: landing page, "Launch Demo" button, no auth.
- `/demo` — Screens A + B: chat (with a demo-user switcher and new-session button) and the live Memory Inspector panel.
- `/dashboard` — optional bonus workspace (Google sign-in + team invites), not part of the judged demo flow.

See `docs/FRONTEND_SPEC.md` for the exact screen and API contract, and `docs/ARCHITECTURE.md` for the full system design.

## Current Progress

- FastAPI backend:
  - `POST /chat` — reply + `memory_events` (`stored` / `flagged` / `conflict`, with `fact` and `trust_tier`)
  - `GET /memories?user_id=` — active/conflicted memories with trust tier, source, status, and conflict pairing
  - `POST /memories/{id}/resolve` — `accept` / `reject` / `supersede`, auto-resolves the linked conflicting counterpart
  - `POST /session/new` — fresh `session_id` for the same `user_id`
  - `GET /demo/users` — preset demo users for the switch-user dropdown
  - `GET /health`
  - Optional bonus: `POST /auth/google/verify`, `GET /auth/me`, `/teams/*`
- Governance module: trust scorer (source → tier/TTL), poisoning keyword flag path, conflict detection with cross-linked pairs, resolve-driven counterpart resolution.
- Next.js frontend: landing page, `/demo` chat + Memory Inspector (with paired "Accept new / Keep old" conflict cards and inline `📌 remembered` / `⚠️ flagged` reply tags), `/dashboard` bonus workspace.
- Local infra: backend + frontend Dockerfiles, `docker-compose.yml`.
- Backend test suite covering trust scoring, poisoning rules, conflict detection, conflict-pair auto-resolution, session creation, and demo users.

## Quick Start

1. Copy `.env.example` to `.env` and set values (`QWEN_API_KEY` / `QWEN_BASE_URL` for the real Qwen Cloud model, or leave `LLM_PROVIDER=ollama` for local dev).
2. Start backend:
   - `cd backend`
   - `pip install -e .`
   - `uvicorn app.main:app --reload`
3. Start frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

Open `http://localhost:3000`, click **Launch Demo**.

## Next Session Targets

- Replace in-memory store with Postgres + pgvector + Redis.
- Add vector retrieval and model-based conflict adjudication (Qwen-assisted comparison).
- Add decay scheduler/check-on-read with demo time scaling.
- Deploy backend on Alibaba Cloud ECS and attach deployment proof links per `docs/SUBMISSION_CHECKLIST.md`.
