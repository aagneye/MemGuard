# MemGuard — Architecture Diagram (Submission Artifact)

This document is the **hackathon submission architecture diagram** package. It maps the live codebase (not a paper design) so judges can see how **Qwen Cloud**, the **FastAPI backend**, **data stores**, and the **Next.js frontend** connect.

| Artifact | Path |
|---|---|
| **PNG (embed in README / Devpost)** | [`architecture-diagram.png`](architecture-diagram.png) |
| High-level Mermaid (readable on GitHub) | [`architecture-diagram-overview.mmd`](architecture-diagram-overview.mmd) |
| Deep Mermaid (module-level) | [`architecture-diagram.mmd`](architecture-diagram.mmd) |
| Narrative architecture | [`ARCHITECTURE.md`](ARCHITECTURE.md) |

---

## System at a glance

```
 Browser (Next.js :3000)
        │  HTTP JSON  (NEXT_PUBLIC_API_BASE)
        ▼
 FastAPI Backend (:8000)  ── optional Nginx /api in production
        │
        ├─► Governance (trust · poison · conflict · decay)
        ├─► SessionRepository + InMemoryStore
        │         └── Postgres+pgvector / Redis ready via docker-compose
        └─► LLM Provider (llm.py)
                  ├─ LLM_PROVIDER=qwen  → Qwen Cloud DashScope
                  │     Call 1: chat reply
                  │     Call 2: JSON fact extraction
                  │     Call 3: conflict adjudication
                  │     + text-embedding-v3 for vector Stage 1
                  └─ LLM_PROVIDER=ollama → local Qwen-family model (dev)
```

---

## Layer map → source files

### 1. Frontend (Next.js)

| UI piece | File | Talks to |
|---|---|---|
| Landing | `frontend/app/page.tsx` | Link to `/demo` |
| Demo shell | `frontend/app/demo/page.tsx` | Orchestrates panels |
| Chat | `frontend/components/ChatPanel.tsx` | `POST /chat` |
| Memory Inspector | `frontend/components/MemoryInspector.tsx` | `GET /memories`, `POST /memories/{id}/resolve` |
| Governance Log | `frontend/components/ActivityFeed.tsx` | `GET /events` |
| Search | `frontend/components/MemorySearchPanel.tsx` | `GET /memories/search` |
| API client | `frontend/lib/api.ts` | `NEXT_PUBLIC_API_BASE` |

### 2. Backend API (FastAPI on ECS)

| Concern | File |
|---|---|
| App entry, CORS, middleware, MCP mount | `backend/app/main.py` |
| Chat turn | `backend/app/routes_chat.py` |
| Memories CRUD / resolve / touch / search | `backend/app/routes_memories.py`, `routes_memories_search.py`, … |
| Events / sessions / demo | `routes_events.py`, `routes_sessions.py`, `routes_demo.py` |
| MCP tools | `backend/app/mcp_server.py` mounted at `/mcp` |

### 3. Governance (core MemGuard logic)

| Step | File | Role |
|---|---|---|
| Orchestrate candidate | `service_memory.py` | Trust → poison → conflict → persist + event |
| Trust tiers | `service_trust.py` | `user_stated` HIGH, `tool_inferred` MED, `document_extracted` LOW |
| Poisoning | `service_poison.py` | Sensitive keywords → `flagged_poisoning` |
| Conflict Stage 1 | `service_conflict.py` + `llm_embed.py` | Keyword + cosine similarity |
| Conflict Stage 2 | `llm_adjudicate.py` | Qwen: agree / conflict / duplicate / unrelated |
| Decay | `service_decay.py` | TTL + `DEMO_TIME_SCALE`, check-on-read |
| Fact extract | `llm_extract.py` (+ heuristic fallback) | Qwen JSON-only extraction |

### 4. Data

| Store | Status in code | Files |
|---|---|---|
| **InMemoryStore** | **Live runtime** | `store.py`, repositories in `state.py` |
| Postgres + pgvector | Schema + compose ready | `db/models.py`, `alembic/`, `infra/docker-compose.yml` |
| Redis | Compose service ready | `REDIS_URL` in config / `.env` |

### 5. Qwen Cloud connection

| Call | When | Module |
|---|---|---|
| Chat completion | Every `/chat` turn | `routes_chat.py` → OpenAI client in `llm.py` |
| Structured extract | After reply, per message | `llm_extract.py` |
| Conflict adjudication | When Stage 1 finds candidates | `llm_adjudicate.py` |
| Embeddings | Stage 1 vector / search | `llm_embed.py` (`text-embedding-v3`) |

Provider switch (`config.py` / `.env`):

- **Production / demo video:** `LLM_PROVIDER=qwen` + `QWEN_API_KEY` → DashScope compatible-mode base URL  
- **Local dev:** `LLM_PROVIDER=ollama` → `OLLAMA_BASE_URL` + Qwen-family model  

---

## Request path for one chat turn (judge-facing)

1. User types in **ChatPanel** → `sendChatMessage` (`lib/api.ts`).
2. **POST /chat** hits FastAPI (`routes_chat.py`).
3. Active memories loaded; **session history** built (`service_session.py`).
4. **LLM call #1** — chat reply via Qwen (or Ollama).
5. **LLM call #2** — JSON fact candidates (`llm_extract.py`).
6. For each candidate, **MemoryService**:
   - score trust → check poison → Stage 1 conflict → **LLM call #3** adjudicate → store / flag / conflict-link.
7. Response returns `reply` + `memory_events`.
8. Frontend refreshes **MemoryInspector** + **ActivityFeed**.

---

## Production topology (Alibaba Cloud)

See [`PRODUCTION.md`](PRODUCTION.md) and [`../infra/alibaba-cloud/ecs-setup.md`](../infra/alibaba-cloud/ecs-setup.md):

```
Internet → EIP → Nginx:80 → Frontend:3000
                      └─ /api → Backend:8000 → Qwen Cloud
                               └─ Postgres · Redis containers
```

---

## Regenerating the PNG

```bash
# From repo root (requires Node + @mermaid-js/mermaid-cli)
npx @mermaid-js/mermaid-cli -i docs/architecture-diagram-overview.mmd -o docs/architecture-diagram.png -b transparent
```

Or re-export from the design asset used for submission and overwrite `docs/architecture-diagram.png`.
