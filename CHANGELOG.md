# Changelog

All notable changes to MemGuard are documented here.

## [0.3.0] — 2026-07-07

### Added (this session — 80+ commits)

#### Core Intelligence
- **Three Qwen LLM calls per turn**: chat reply, JSON fact extraction (`llm_extract.py`), and conflict adjudication (`llm_adjudicate.py`)
- **Qwen `text-embedding-v3` integration** (`llm_embed.py`) for vector similarity in Stage 1 conflict detection
- **Two-stage conflict detector**: Stage 1 = keyword + vector cosine similarity; Stage 2 = LLM adjudicates the relation type
- **`service_decay.py`** with `DEMO_TIME_SCALE` acceleration for live demos
- **`last_confirmed_at`** field on memories; `touch` endpoint to defer TTL expiry

#### API Surface
- `GET /memories/{id}` — single memory fetch
- `GET /memories/search` — keyword + vector hybrid semantic search
- `POST /memories/{id}/touch` — defer TTL countdown
- `POST /demo/reset` — clear all demo user memories
- `GET /trust/explain` — governance debug endpoint explaining trust tier assignment
- `GET /mcp/tools` + `POST /mcp/tools/search_memory` + `POST /mcp/tools/write_memory` — MCP tool server

#### Infrastructure
- `infra/docker-compose.yml` — full Postgres (pgvector) + Redis + healthchecks
- `infra/docker-compose.prod.yml` — production override
- `infra/nginx/memguard.conf` — nginx reverse proxy
- `infra/alibaba-cloud/ecs-setup.md` — deployment proof artifact
- `infra/alibaba-cloud/rds-setup.md` — managed Postgres guide
- Backend Dockerfile HEALTHCHECK
- `.dockerignore` for both backend and frontend
- GitHub Actions CI workflow (`.github/workflows/ci.yml`)

#### Backend Quality
- Structured JSON logging (`logging_config.py`)
- Request correlation middleware with `X-Request-ID` (`middleware_logging.py`)
- Sliding-window rate limiter (`middleware_ratelimit.py`)
- Standardized error responses (`exception_handlers.py`)
- OpenAPI metadata with license, contact, and description
- Alembic migration setup with initial `memories` + `memory_events` tables
- SQLAlchemy ORM models (`db/models.py`) as Postgres migration target
- `pyproject.toml` dev extras: ruff, pyright, pytest-asyncio

#### Tests (15 test files, 60+ test cases)
- `conftest.py` with store isolation autouse fixture
- `test_chat_pipeline.py` — full integration tests
- `test_llm_extract_fallback.py` — extraction parsing and None-client fallback
- `test_llm_adjudicate.py` — adjudication JSON parsing
- `test_service_conflict_vector.py` — keyword + vector conflict tests
- `test_service_memory.py` — memory service orchestration
- `test_memory_decay.py` — TTL expiry and no-expire behavior
- `test_mcp_server.py` — MCP tool discovery and roundtrip
- `test_memory_search.py` — hybrid search endpoint
- `test_memory_single.py` — single memory fetch
- `test_demo_reset.py` — demo reset endpoint
- `test_trust_explain.py` — trust tier explanation endpoint

#### Frontend
- `Spinner.tsx` + CSS animation
- `ErrorToast.tsx` auto-dismissing error notification
- `ActivityFeed.tsx` governance log panel
- `EmptyState.tsx` reusable empty state
- `not-found.tsx` custom 404 page
- `demo/layout.tsx` demo-specific metadata
- MemoryInspector: decay countdown badge, memory count, trust tier legend
- TopBar: session ID display, Reset Demo button
- ChatPanel: Spinner while waiting for reply, EmptyState with demo hint
- `next.config.js` API proxy rewrites
- Full OpenGraph + Twitter card metadata in `layout.tsx`

#### Scripts and Docs
- `scripts/seed_demo_data.py` — pre-load 5-beat demo state
- `scripts/replay_demo_beats.py` — scripted 5-beat verification
- `scripts/setup.sh` — one-command local dev setup
- `scripts/README.md`
- `docs/DEMO_GUIDE.md` — beat-by-beat demo script for video recording
- `docs/SUBMISSION_CHECKLIST.md` updated with full build progress table
- `Makefile` — common dev commands
- `LICENSE` — MIT (required for hackathon submission)

## [0.2.0] — 2026-07-06

- Full frontend demo: Chat UI, Memory Inspector, TopBar
- Backend: conflict cross-linking, resolve with counterpart auto-expiry
- Demo screens: Landing (Screen C), Demo (Screens A+B)
- Google OAuth and team management (deprioritized for public demo)

## [0.1.0] — 2026-07-05

- Initial architecture and docs
- FastAPI backend scaffold
- Trust scoring, poisoning detection, heuristic conflict detection
- In-memory store with all CRUD operations
