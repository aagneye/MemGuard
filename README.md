# MemGuard — Trust-Aware Memory Agent

> **Qwen Cloud Global AI Hackathon 2026 — Track 1: MemoryAgent**

MemGuard is an open-source agent memory layer that **scores every memory for trust and provenance**, catches conflicting or poisoned facts before acting on them, and forgets what's gone stale — all powered by Qwen Cloud.

---

## The Problem

AI agents that remember things across sessions face a critical threat: **memory poisoning**. A malicious document, a crafted tool call, or a simple user mistake can silently overwrite a trusted fact with a false one. OWASP's Top 10 for Agentic Applications lists memory injection as a top-tier risk.

Most memory systems are dumb key-value stores. MemGuard is different: every fact has a trust tier, a source, a TTL, and a lifecycle.

---

## Architecture

```
User Message
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  FastAPI Backend (MemGuard)                             │
│                                                         │
│  ① chat_reply()        — Qwen Chat LLM (qwen-plus)     │
│  ② extract_facts()     — Qwen (JSON-only output)       │
│  ③ adjudicate_conflict() — Qwen (stage 2 detection)    │
│                                                         │
│  Governance Module:                                     │
│    • Trust Scorer   (user_stated=HIGH, doc=LOW)        │
│    • Conflict Detector (keyword + vector Stage 1)       │
│    • Poisoning Guard  (sensitive claim flagging)        │
│    • Decay Scheduler  (TTL + demo_time_scale)          │
│                                                         │
│  MCP Tool Server: /mcp/tools/search_memory             │
│                   /mcp/tools/write_memory              │
└────────────────────┬────────────────────────────────────┘
                     │
              ┌──────▼──────┐
              │ InMemoryStore│  ← dev (zero config)
              └──────┬───────┘
                     │ (migration path)
              ┌──────▼───────┐
              │ Postgres     │  ← prod (pgvector + Alembic)
              │ + Redis      │
              └──────────────┘
```

---

## Demo Screens

| Screen | Route | Description |
|---|---|---|
| **Landing** | `/` | "What is MemGuard" + Launch Demo button |
| **Chat + Inspector** | `/demo` | Chat panel + Memory Inspector + Governance Log |

---

## The 5 Demo Beats

1. **High-trust capture** — "I'm on the Pro plan, my timezone is IST." → three `HIGH · user_stated · active` memories.
2. **Cross-session recall** — New session, ask "What's my plan?" → agent recalls without being told again.
3. **Poisoning refusal** — Forward a document granting admin access → flagged with `🛡️` in the governance log.
4. **Conflict resolution** — "Actually I'm on Enterprise now." → old/new cards appear, judge presses **Accept new**.
5. **Decay** — Set `DEMO_TIME_SCALE=1440` to watch memories expire in real time.

---

## Three Qwen LLM Calls Per Turn

1. `chat_reply()` — chat turn response (qwen-plus)
2. `extract_facts_via_llm()` — structured JSON fact extraction (qwen-plus, zero temperature)
3. `adjudicate_conflict()` — Stage 2 conflict classification: agree/conflict/duplicate/unrelated (qwen-plus)

Plus `embed_text()` — vector embeddings via `text-embedding-v3` for Stage 1 conflict scoring.

---

## Quick Start (Local Dev — No API Key Required)

```bash
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
# Default: LLM_PROVIDER=ollama + qwen2.5:7b — run: ollama pull qwen2.5:7b

# Start everything
docker compose -f infra/docker-compose.yml up

# Open the demo
open http://localhost:3000
```

## Quick Start (Qwen Cloud Production)

```bash
cp .env.example .env
# Set: LLM_PROVIDER=qwen, QWEN_API_KEY=<your-dashscope-key>
docker compose -f infra/docker-compose.yml -f infra/docker-compose.prod.yml up -d --build
```

---

## API Surface

| Method | Path | Purpose |
|---|---|---|
| POST | `/chat` | Send message, get reply + memory events |
| GET | `/memories` | List all memories for a user |
| GET | `/memories/search` | Semantic search over user's memories |
| GET | `/memories/{id}` | Fetch single memory by ID |
| POST | `/memories/{id}/resolve` | Accept / reject / supersede a conflicted memory |
| POST | `/memories/{id}/touch` | Reset TTL countdown for a memory |
| GET | `/events` | Governance log for a user |
| POST | `/session/new` | Create a new session |
| GET | `/demo/users` | List preset demo users |
| POST | `/demo/reset` | Clear all demo memories for a fresh run |
| GET | `/mcp/tools` | MCP tool discovery for Qwen agents |
| POST | `/mcp/tools/search_memory` | MCP: search memories |
| POST | `/mcp/tools/write_memory` | MCP: write a memory |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive OpenAPI UI |

---

## Project Structure

```
MemGuard/
├── backend/
│   ├── app/
│   │   ├── llm.py              # Qwen/Ollama client
│   │   ├── llm_extract.py      # 2nd Qwen call — JSON fact extraction
│   │   ├── llm_adjudicate.py   # 3rd Qwen call — conflict classification
│   │   ├── llm_embed.py        # text-embedding-v3 calls
│   │   ├── service_memory.py   # Core orchestration
│   │   ├── service_conflict.py # Stage 1: keyword + vector
│   │   ├── service_decay.py    # TTL with demo_time_scale
│   │   ├── service_trust.py    # Trust tier scoring
│   │   ├── service_poison.py   # Poisoning detection
│   │   ├── mcp_server.py       # MCP tool server (mounted at /mcp)
│   │   ├── db/models.py        # SQLAlchemy ORM (Postgres migration target)
│   │   └── ...
│   ├── alembic/                # Database migrations
│   └── tests/                  # pytest test suite (15 test files)
├── frontend/
│   ├── components/
│   │   ├── ChatPanel.tsx
│   │   ├── MemoryInspector.tsx # Trust badges, decay badges, conflict cards
│   │   ├── ActivityFeed.tsx    # Governance log
│   │   ├── TopBar.tsx
│   │   └── ...
│   └── app/
│       ├── page.tsx            # Landing
│       └── demo/page.tsx       # Main demo screen
├── infra/
│   ├── docker-compose.yml      # Postgres + Redis + backend + frontend
│   ├── docker-compose.prod.yml # Production override
│   ├── nginx/memguard.conf     # Reverse proxy
│   └── alibaba-cloud/          # ECS + RDS deployment guides
├── scripts/
│   ├── seed_demo_data.py       # Pre-load demo users
│   └── replay_demo_beats.py    # Verify 5 beats pass
└── docs/
    ├── ARCHITECTURE.md
    ├── DEMO_GUIDE.md           # Beat-by-beat demo script
    └── SUBMISSION_CHECKLIST.md
```

---

## Running Tests

```bash
cd backend
pip install -e ".[dev]"
pytest tests/ -v
```

---

## License

MIT — see [LICENSE](LICENSE).
