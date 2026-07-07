# MemGuard — Project Structure

Monorepo. One repo, three deployable pieces (`backend`, `frontend`, `infra`), plus `docs` and `scripts`. This layout is what gets scaffolded in the *next* session — nothing here exists yet except this plan.

```
memguard/
├── LICENSE                          # MIT or Apache-2.0 — required, must be visible in GitHub "About"
├── README.md                        # pitch, architecture diagram embed, setup quickstart, demo links
├── .env.example                     # all env vars, no real secrets
├── .gitignore
│
├── backend/                         # FastAPI service
│   ├── pyproject.toml                # deps via uv or poetry
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py                   # FastAPI app, router mounting, CORS
│   │   ├── config.py                 # pydantic Settings, reads .env (LLM_PROVIDER, DB_URL, etc.)
│   │   ├── db/
│   │   │   ├── session.py            # async SQLAlchemy engine/session
│   │   │   ├── models.py             # Memory, MemoryEvent ORM models
│   │   │   └── migrations/           # alembic migrations (001_init, 002_add_events, ...)
│   │   ├── redis_client.py           # session-turn read/write, TTL config
│   │   ├── llm/
│   │   │   ├── base.py               # LLMProvider ABC: chat(), extract_facts(), compare_facts()
│   │   │   ├── qwen_provider.py       # DashScope compatible-mode client
│   │   │   ├── ollama_provider.py     # local Ollama client (qwen2.5 model)
│   │   │   └── factory.py            # get_provider() reads LLM_PROVIDER env
│   │   ├── governance/
│   │   │   ├── trust_scorer.py        # source -> tier/ttl table + confidence downgrade
│   │   │   ├── conflict_detector.py   # stage-1 vector search + stage-2 LLM adjudication
│   │   │   ├── poisoning_rules.py     # sensitive-keyword allowlist for document_extracted facts
│   │   │   └── decay.py               # check-on-read expiry query, DEMO_TIME_SCALE handling
│   │   ├── orchestrator.py           # the /chat pipeline: retrieve -> prompt -> reply -> extract -> govern -> persist
│   │   ├── schemas.py                 # pydantic request/response models
│   │   ├── routes/
│   │   │   ├── chat.py                # POST /chat
│   │   │   ├── memories.py            # GET /memories, POST /memories/{id}/resolve
│   │   │   └── health.py              # GET /health (needed for ECS/LB checks + deployment proof)
│   │   └── mcp/                       # STRETCH: only after 5 demo beats work
│   │       └── server.py              # exposes search_memory / write_memory as MCP tools
│   └── tests/
│       ├── test_trust_scorer.py
│       ├── test_conflict_detector.py
│       └── test_chat_flow.py
│
├── frontend/                        # Next.js chat UI
│   ├── package.json
│   ├── Dockerfile
│   ├── app/
│   │   ├── page.tsx                  # chat panel
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageInput.tsx
│   │   ├── MemoryInspector/
│   │   │   ├── ActiveMemoryList.tsx
│   │   │   ├── PendingReviewList.tsx
│   │   │   └── ActivityFeed.tsx
│   │   └── SessionSwitcher.tsx        # dev control to jump to "Session 2" for the recall demo beat
│   └── lib/
│       └── api.ts                    # typed fetch wrappers for /chat, /memories, /resolve
│
├── infra/                           # deployment
│   ├── docker-compose.yml            # backend + postgres(pgvector) + redis, local & ECS use the same file
│   ├── docker-compose.prod.yml       # overrides: restart policies, env_file, nginx
│   ├── nginx/
│   │   └── memguard.conf             # reverse proxy: / -> frontend, /api -> backend
│   └── alibaba-cloud/
│       ├── ecs-setup.md              # step-by-step ECS provisioning notes (the "proof file" the submission links to)
│       └── rds-setup.md              # optional stretch: managed Postgres+pgvector path
│
├── scripts/
│   ├── seed_demo_user.py             # creates the fictional "Acme Cloud" user + resets memory state before recording
│   ├── replay_demo_beats.py          # scripted API calls that walk all 5 demo beats, for pre-recording sanity checks
│   └── eval_conflict_cases.py        # a handful of adversarial poisoning/conflict test inputs + expected verdicts
│
└── docs/
    ├── ARCHITECTURE.md               # this planning doc
    ├── PROJECT_STRUCTURE.md          # this file
    ├── SETUP.md                      # full local + cloud setup guide
    ├── BUILD_PLAN.md                 # hour-by-hour build order against the deadline
    ├── SUBMISSION_CHECKLIST.md       # devpost requirements mapped to repo artifacts
    └── architecture-diagram.png      # exported/cleaned version of the mermaid diagram, for the README + submission
```

## Conventions

- **Backend**: Python 3.11+, FastAPI, async SQLAlchemy 2.x, Alembic for migrations, `uv` for dependency management (fast installs matter when you're setting up on a fresh ECS box under time pressure).
- **Frontend**: Next.js App Router, TypeScript, Tailwind CSS, no heavy state library needed — `useState`/`useSWR` is enough for this scope.
- **Config**: every tunable (LLM provider, TTLs, similarity threshold, demo time scale) lives in `.env` / `config.py`, never hardcoded — this is what lets you demo decay in seconds instead of days without touching code.
- **One .env.example, fully commented**, so setup is copy-paste-able (see `docs/SETUP.md`).
- **Commit hygiene**: this repo follows the workspace's atomic-commit rule (`cursorrules`) — one logical change per commit, `<type>(<file>): <description>` format, docs/config/feature/test changes committed separately.
