# MemGuard — Production Setup (Alibaba Cloud)

Clear guide to **host MemGuard on Alibaba Cloud** for the hackathon.

This doc is your **setup for production**. Local machine steps live in **[SETUP.md](SETUP.md)**.

---

## Why this doc exists (hackathon “What to Submit”)

| Submission item | Where MemGuard covers it |
|---|---|
| Public open-source repo + license in About | Root [`LICENSE`](../LICENSE) (MIT) — set repo to **Public** on GitHub |
| **Proof of Alibaba Cloud deployment** | This guide + [`infra/alibaba-cloud/ecs-setup.md`](../infra/alibaba-cloud/ecs-setup.md) (link this file on Devpost) |
| Architecture diagram | [`architecture-diagram.png`](architecture-diagram.png) in README |
| ~3 min demo video | Record against the **ECS public URL**, not localhost — [DEMO_GUIDE.md](DEMO_GUIDE.md) |
| Text description + Track 1 | [ARCHITECTURE.md](ARCHITECTURE.md) · Track = **MemoryAgent** |

---

## Architecture you are hosting

```
Browser
   │
   ▼
Alibaba Cloud ECS  ── Nginx ──► Next.js frontend (:3000)
                     │
                     └── /api ──► FastAPI backend (:8000)
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
            Postgres+pgvector    Redis / Tair      Qwen Cloud
            (long-term memory)   (session TTL)     (DashScope)
```

| Layer | Production choice | Role |
|---|---|---|
| **Backend** | FastAPI on **Alibaba Cloud ECS** (or Function Compute stretch) | Deployment proof artifact |
| **Reasoning + fact extraction** | **Qwen** via **DashScope** OpenAI-compatible API | Chat reply, JSON extract, conflict adjudicate, embeddings |
| **Memory store** | **Postgres + pgvector** and/or **Redis / Tair** | Vectors + fact table fields: trust, provenance, TTL |
| **Governance** | Conflict detector + decay (check-on-read / demo scale) | Rubric “algorithmic innovation” |

Code entry points: `backend/app/routes_chat.py`, `service_memory.py`, `llm.py`, `llm_extract.py`, `llm_adjudicate.py`, `service_conflict.py`, `service_decay.py`.

---

## Before you start

Do these on your laptop first ([SETUP.md](SETUP.md)):

1. Local `/demo` works.
2. GitHub repo is **public** with MIT visible in About.
3. You have a **DashScope (Qwen Cloud) API key**.
4. You have an **Alibaba Cloud** account (same region as DashScope if possible, e.g. `ap-southeast-1`).

**Rule for submission:** production and the demo video must use `LLM_PROVIDER=qwen` — **not** Ollama.

---

## Part A — Qwen Cloud (DashScope) setup

Judges expect **Qwen Cloud** for reasoning and fact extraction.

### A1. Create API key

1. Open [DashScope console](https://dashscope.aliyun.com/).
2. Create an API key (use hackathon credits if available).
3. Keep the key only in server `.env` — never commit it.

### A2. Compatible-mode endpoint

MemGuard uses the OpenAI-compatible client (`backend/app/llm.py`):

```text
https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

Models used in production:

| Call | Model / API | Module |
|---|---|---|
| Chat reply | `qwen-plus` | `routes_chat.py` |
| Fact extraction (JSON) | `qwen-plus` | `llm_extract.py` |
| Conflict adjudication | `qwen-plus` | `llm_adjudicate.py` |
| Embeddings | `text-embedding-v3` | `llm_embed.py` |

### A3. Sanity-check Qwen before deploy

```bash
curl https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer YOUR_QWEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"qwen-plus\",\"messages\":[{\"role\":\"user\",\"content\":\"say hi\"}]}"
```

If this fails, fix the key/region before touching ECS.

---

## Part B — Alibaba Cloud ECS (backend proof of deployment)

This is the **recommended** path and the file you link as deployment proof:  
**[`infra/alibaba-cloud/ecs-setup.md`](../infra/alibaba-cloud/ecs-setup.md)**

### B1. Create ECS

1. Alibaba Cloud Console → **ECS** → Create Instance  
2. OS: **Ubuntu 22.04 LTS**  
3. Size: **2 vCPU / 4 GB RAM** minimum, 40 GB disk  
4. Bind an **Elastic IP (EIP)**  
5. Security group inbound:

| Port | Who | Why |
|---|---|---|
| 22 | Your IP only | SSH |
| 80 | Everyone | Nginx → demo site |
| 8000 | Everyone *(temporary)* | Direct health check for proof video — close after |

### B2. Install Docker on the instance

```bash
ssh root@YOUR_ECS_PUBLIC_IP

curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin git curl
systemctl enable docker && systemctl start docker
```

### B3. Clone MemGuard and write production `.env`

```bash
cd /opt
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
nano .env
```

**Production `.env` (copy and replace placeholders):**

```env
# ── Qwen Cloud (required for submission) ───────────────────────────────────
LLM_PROVIDER=qwen
QWEN_API_KEY=sk-your-real-dashscope-key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_CHAT_MODEL=qwen-plus

# ── Frontend build-time API base (CRITICAL) ────────────────────────────────
# Nginx proxies /api → FastAPI. Rebuild frontend if you change this.
NEXT_PUBLIC_API_BASE=http://YOUR_ECS_PUBLIC_IP/api

# ── CORS ───────────────────────────────────────────────────────────────────
CORS_ORIGINS=http://YOUR_ECS_PUBLIC_IP

# ── Memory stores on the ECS docker network ────────────────────────────────
# Postgres + pgvector (long-term / vectors)
DATABASE_URL=postgresql+asyncpg://memguard:CHANGE_ME@postgres:5432/memguard
# Redis (session TTL) — swap host for Tair endpoint if using managed Tair
REDIS_URL=redis://redis:6379/0

# ── Governance ─────────────────────────────────────────────────────────────
SIMILARITY_THRESHOLD=0.8
DEMO_TIME_SCALE=1.0
SESSION_TTL_SECONDS=1800
RATE_LIMIT_RPM=60

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### B4. Start the production stack

```bash
cd /opt/MemGuard/infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Starts: **nginx**, **frontend**, **backend**, **postgres (pgvector)**, **redis**.

Enable the vector extension:

```bash
docker compose exec postgres psql -U memguard -d memguard \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

First build can take 5–10 minutes.

### B5. Verify (do this on camera for deployment proof)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
curl http://localhost:8000/health
# Expect: "ok": true, "provider": "qwen"
```

From your laptop:

| URL | Expect |
|---|---|
| `http://YOUR_ECS_PUBLIC_IP/` | Landing |
| `http://YOUR_ECS_PUBLIC_IP/demo` | Chat + Memory Inspector |
| `http://YOUR_ECS_PUBLIC_IP/api/health` | Health JSON with `"provider":"qwen"` |
| `http://YOUR_ECS_PUBLIC_IP/docs` | OpenAPI |

If UI loads but chat fails: fix `NEXT_PUBLIC_API_BASE`, then:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build frontend
```

---

## Part C — Memory store: Postgres + pgvector and Redis / Tair

### C1. Default on ECS (containers)

`infra/docker-compose.yml` already runs:

- **Postgres** image `pgvector/pgvector:pg16` — long-term facts + vector column (see `backend/alembic/`, `backend/app/db/models.py`)
- **Redis** — session-style TTL path (`REDIS_URL`)

Fact fields the governance layer cares about: **trust tier**, **source/provenance**, **status**, **TTL / last_confirmed_at**, **conflicts_with**.

> Runtime note: the demo may still use the fast **InMemoryStore** until the Postgres repository is fully wired ([FUTURE_WORK.md](FUTURE_WORK.md)). For submission, still **run** Postgres + Redis on ECS so the deployment topology matches the architecture (and record `docker compose ps` showing those services).

### C2. Stronger Alibaba proof — managed services

| Service | Guide | What to set in `.env` |
|---|---|---|
| **RDS PostgreSQL** + `vector` | [`infra/alibaba-cloud/rds-setup.md`](../infra/alibaba-cloud/rds-setup.md) | `DATABASE_URL=postgresql+asyncpg://...@<rds-endpoint>:5432/memguard` |
| **Tair / Redis** | Alibaba Cloud Tair console | `REDIS_URL=redis://:<password>@<tair-endpoint>:6379/0` |

After pointing `.env` at RDS/Tair, remove or stop the matching container service and restart the backend.

---

## Part D — Governance module (what to show judges)

Hosted on the same FastAPI process — no extra service to start.

| Capability | What it does | Code |
|---|---|---|
| Trust scorer | `user_stated` → HIGH, `tool_inferred` → MED, `document_extracted` → LOW | `service_trust.py` |
| Poisoning guard | Sensitive doc claims → `flagged_poisoning` | `service_poison.py` |
| Conflict detector | Stage 1 keyword/vector · Stage 2 Qwen adjudicate | `service_conflict.py`, `llm_adjudicate.py` |
| Decay | TTL + `DEMO_TIME_SCALE`, check-on-read | `service_decay.py` |

Visible in the UI: Memory Inspector + Governance Log (`/demo`).

---

## Part E — Optional: Function Compute

ECS is enough for the hackathon. If you prefer serverless:

1. Package the FastAPI app as a Function Compute HTTP function (custom runtime / container).
2. Still call DashScope with `LLM_PROVIDER=qwen`.
3. Attach RDS + Tair via VPC.
4. Document the Function Compute console URL + this repo’s compose/ECS file as alternate proof.

Prefer **ECS + docker compose** unless you already know Function Compute.

---

## Part F — What to put on the submission form

1. **Code repository URL** — `https://github.com/aagneye/MemGuard` (Public + MIT in About).  
2. **Proof of Alibaba Cloud deployment** — link to  
   `https://github.com/aagneye/MemGuard/blob/master/infra/alibaba-cloud/ecs-setup.md`  
   *(and/or this file `docs/PRODUCTION.md`)* plus a short video of `docker compose ps` + `curl .../health` on ECS.  
3. **Architecture diagram** — `docs/architecture-diagram.png` (already in README).  
4. **Demo video (~3 min)** — record on `http://YOUR_ECS_PUBLIC_IP/demo` with Qwen provider.  
5. **Text description** — pitch from [ARCHITECTURE.md](ARCHITECTURE.md).  
6. **Track** — **Track 1: MemoryAgent**.  
7. **Optional blog** — for Blog Post Prize.

---

## Day-2 operations

```bash
# Update code
cd /opt/MemGuard && git pull
cd infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Logs
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f backend

# Reset demo memories before a live run
curl -X POST http://YOUR_ECS_PUBLIC_IP/api/demo/reset
```

---

## Troubleshooting (production)

| Problem | Fix |
|---|---|
| Health shows `"provider":"ollama"` | Set `LLM_PROVIDER=qwen` + `QWEN_API_KEY`, restart backend |
| Chat empty / DashScope errors | Re-run Part A curl; check region URL |
| UI OK, API unreachable | `NEXT_PUBLIC_API_BASE=http://IP/api` then rebuild frontend |
| CORS blocked | Add public URL to `CORS_ORIGINS` |
| Out of memory on build | Use ≥4 GB ECS, or build images elsewhere |
| Postgres / Redis not listed in `docker compose ps` | Re-run Part B4 from `infra/` |

---

## One-page deploy card

```bash
ssh root@YOUR_ECS_PUBLIC_IP
cd /opt && git clone https://github.com/aagneye/MemGuard.git && cd MemGuard
cp .env.example .env
# Edit: LLM_PROVIDER=qwen, QWEN_API_KEY, NEXT_PUBLIC_API_BASE=http://IP/api, CORS_ORIGINS

cd infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose exec postgres psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"
curl http://localhost:8000/health   # provider must be qwen
# Open http://YOUR_ECS_PUBLIC_IP/demo
```

More ECS detail (submission proof file): [`infra/alibaba-cloud/ecs-setup.md`](../infra/alibaba-cloud/ecs-setup.md)  
Local development only: [`SETUP.md`](SETUP.md)
