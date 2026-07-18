# MemGuard — Submission Checklist

Maps Devpost's stated requirements directly to what will exist in this repo. Walk this top-to-bottom right before submitting.

- [x] **Public GitHub repo with MIT license** — root [`LICENSE`](../LICENSE) (MIT, GitHub-detectable). **You must set the GitHub repo to Public** (Settings → General → Danger Zone → Change visibility) so the license appears in the repository **About** section.
- [ ] **Working code + setup instructions** — `README.md` (quickstart) → `docs/SETUP.md` (full guide) → `docker compose -f infra/docker-compose.yml up --build`; verify with `scripts/replay_demo_beats.py`.
- [ ] **Alibaba Cloud deployment proof** — follow `infra/alibaba-cloud/ecs-setup.md`; record the video showing `docker compose ps` and `curl http://<ECS_IP>:8000/health`.
- [x] **Architecture diagram** — [`docs/architecture-diagram.png`](architecture-diagram.png) embedded in root [`README.md`](../README.md); code-mapped write-up in [`ARCHITECTURE_DIAGRAM.md`](ARCHITECTURE_DIAGRAM.md); Mermaid sources `architecture-diagram.mmd` + `architecture-diagram-overview.mmd`.
- [ ] **~3 minute demo video**, public on YouTube/Vimeo, covering all 5 beats. Run `python scripts/replay_demo_beats.py` first to confirm each beat works.
- [ ] **Text description** on Devpost form — copy the pitch + problem statement from `docs/ARCHITECTURE.md §1`.
- [ ] **Track declared**: Track 1 — MemoryAgent.
- [ ] **(Optional) Blog/social post** about the build journey.

---

## Build progress (auto-updated)

| Area | Status |
|---|---|
| MIT LICENSE | ✅ |
| pytest.ini + tests/__init__.py | ✅ |
| LLM fact extraction (2nd Qwen call) | ✅ `backend/app/llm_extract.py` |
| LLM conflict adjudication (3rd Qwen call) | ✅ `backend/app/llm_adjudicate.py` |
| Two-stage conflict detector in service_memory | ✅ |
| Structured JSON logging | ✅ `backend/app/logging_config.py` |
| Request correlation middleware | ✅ `backend/app/middleware_logging.py` |
| Rate limiter middleware | ✅ `backend/app/middleware_ratelimit.py` |
| Health endpoint enriched | ✅ `GET /health` returns version + provider |
| OpenAPI metadata + license + contact | ✅ `main.py` |
| docker-compose with Postgres (pgvector) + Redis | ✅ `infra/docker-compose.yml` |
| docker-compose.prod.yml override | ✅ `infra/docker-compose.prod.yml` |
| Backend Dockerfile HEALTHCHECK | ✅ |
| Backend + Frontend .dockerignore | ✅ |
| Nginx reverse proxy config | ✅ `infra/nginx/memguard.conf` |
| Alibaba Cloud ECS setup guide | ✅ `infra/alibaba-cloud/ecs-setup.md` |
| Demo seed data script | ✅ `scripts/seed_demo_data.py` |
| 5-beat demo replay verifier | ✅ `scripts/replay_demo_beats.py` |
| MCP tool server (search + write) | ✅ `backend/app/mcp_server.py` mounted at `/mcp` |
| Frontend Spinner component | ✅ |
| Frontend ErrorToast component | ✅ |
| Next.js layout metadata (OG, Twitter card) | ✅ |
| Custom 404 page | ✅ |
| next.config.js API proxy rewrite | ✅ |
| Backend integration test suite | ✅ `tests/test_chat_pipeline.py` |
| LLM extraction fallback tests | ✅ `tests/test_llm_extract_fallback.py` |
| Memory decay TTL tests | ✅ `tests/test_memory_decay.py` |
| Shared conftest.py with store isolation | ✅ |
| last_confirmed_at field + None-ttl support | ✅ |
| Documentation index | ✅ `docs/README.md` |
| Consolidated setup guide | ✅ `docs/SETUP.md` (root `setup.md` removed) |
| Post-submission backlog | ✅ `docs/FUTURE_WORK.md` |

---

## Documentation map

| Doc | Use when |
|---|---|
| [README.md](../README.md) | First clone — how to run locally |
| [docs/SETUP.md](SETUP.md) | Full env config, Qwen, Docker, ECS, OAuth |
| [docs/DEMO_GUIDE.md](DEMO_GUIDE.md) | Recording the demo video |
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | Devpost description + technical depth |
| [docs/FUTURE_WORK.md](FUTURE_WORK.md) | What to build after submission |

---

## Judging-criteria self-check

- [ ] **Technical Depth (30%)** — point to: `llm_extract.py` (2nd call), `llm_adjudicate.py` (3rd call), `mcp_server.py` (MCP integration), dual LLM provider switch in `llm.py`.
- [ ] **Innovation (30%)** — Memory Inspector shows trust tiers, provenance, supersede lifecycle, and conflict resolution side-by-side with chat.
- [ ] **Problem Value (25%)** — demo video explicitly says "memory poisoning", "OWASP Top 10 for Agentic Applications", and `flagged_poisoning` event is visible on screen.
- [ ] **Presentation (15%)** — activity feed (`/events`) visible and narrated, governance logic on screen, not just a plain chat log.
