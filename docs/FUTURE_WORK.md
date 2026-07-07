# MemGuard — Future Work

The hackathon demo is feature-complete for judging. The items below are the natural next steps if you continue development after submission.

---

## Priority 1 — Production persistence (highest impact)

| Item | Status | Notes |
|---|---|---|
| Wire Postgres + pgvector as the live store | Stub only | `backend/app/db/models.py` and `alembic/versions/001_initial_memories.py` exist; routes still use `InMemoryStore` |
| Run Alembic migrations on startup | Not wired | `alembic upgrade head` works manually; add to ECS/docker entrypoint |
| Redis session memory in chat prompt | Partial | `repository_sessions.py` exists; session turns are in-memory only |
| Store embeddings in `memories.embedding` column | Not wired | `llm_embed.py` computes vectors but does not persist them yet |
| pgvector similarity search in `GET /memories/search` | Partial | Falls back to keyword match when embeddings are zero vectors |

---

## Priority 2 — Demo & submission polish

| Item | Status | Notes |
|---|---|---|
| Record ~3 min demo video | Pending | Follow `docs/DEMO_GUIDE.md` beat-by-beat |
| Record Alibaba Cloud deployment proof | Pending | Follow `infra/alibaba-cloud/ecs-setup.md` |
| Export architecture diagram PNG | Pending | Follow `docs/generate-architecture-png.md`, embed in README |
| Deploy to ECS with `LLM_PROVIDER=qwen` | Pending | Demo video must use Qwen, not Ollama |
| Devpost submission text | Pending | Pull from `docs/ARCHITECTURE.md` §1 pitch + demo scenario |

---

## Priority 3 — Optional features (built but not in main demo flow)

| Item | Status | Notes |
|---|---|---|
| Google OAuth + dashboard | Built, deprioritized | `/dashboard`, `/auth/*` routes exist; public demo uses `/demo` with no login |
| Team create / invite | Built, deprioritized | `/teams/*` routes exist; not needed for Track 1 judging |
| Role-based team permissions | Not built | Invite acceptance flow, member roles |
| API key auth for enterprise integration | Not built | For external memory-layer consumers |

---

## Priority 4 — Hardening & ops

| Item | Status | Notes |
|---|---|---|
| Replace in-memory rate limiter with Redis-backed limiter | Partial | `middleware_ratelimit.py` is process-local |
| Structured logging to Alibaba Cloud SLS | Partial | `logging_config.py` ready; needs SLS agent on ECS |
| HTTPS / TLS via Let's Encrypt on Nginx | Not configured | `infra/nginx/memguard.conf` is HTTP only |
| Managed RDS instead of container Postgres | Documented | See `infra/alibaba-cloud/rds-setup.md` |
| Load testing / soak tests | Not built | `scripts/load_test.py` could be added |
| Frontend E2E tests (Playwright) | Not built | Backend has 20+ pytest files |

---

## Priority 5 — Stretch goals

| Item | Status | Notes |
|---|---|---|
| MCP server registered with Qwen Cloud agent platform | Partial | `/mcp/tools` mounted; not registered as external tool in DashScope console |
| Background decay sweep job | Partial | Check-on-read works; no cron/scheduler for proactive expiry |
| Multi-tenant memory isolation (org/team scoping) | Not built | All memories keyed by `user_id` only |
| Memory export/import API | Partial | `scripts/export_memories.py` CLI only |
| Real-time Activity Feed via WebSocket | Not built | Frontend polls on each chat turn |

---

## How to pick up any item

1. Read `docs/ARCHITECTURE.md` for the intended design.
2. Check `docs/BUILD_PLAN.md` for original day-by-day intent.
3. Run `make test` or `cd backend && pytest tests/ -v` before and after changes.
4. Follow atomic commit rules in `.cursor/rules/commits.mdc`.
