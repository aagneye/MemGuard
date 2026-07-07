# MemGuard — Setup Guide

Covers local dev setup and Alibaba Cloud deployment. This is written now, ahead of the build session, so the next session is pure execution against a checklist.

---

## 0. Prerequisites

Install before the build session starts:

- **Docker Desktop** (Windows) — for Postgres+pgvector and Redis containers, and later for the ECS deployment.
- **Python 3.11+** and `uv` (or `poetry`) for the backend.
- **Node.js 20+** and `pnpm`/`npm` for the frontend.
- **Ollama** — [ollama.com](https://ollama.com/download) — local LLM runtime for dev/offline iteration.
- **Git** + a GitHub account, repo created as **public with a license** (MIT recommended) from the start — the license must be visible in the "About" section for submission, easiest to get right on day 1 rather than fix later.
- **Alibaba Cloud account** — sign up, note region (pick one close to you / to Qwen Cloud's compatible-mode endpoint region for lowest latency).
- **Qwen Cloud (DashScope) account** — sign up via the hackathon's Qwen Cloud link, claim the hackathon credit coupon, generate an API key.

---

## 1. Qwen Cloud (DashScope) account setup

1. Register on Devpost for the hackathon (if not already done).
2. Sign up for Qwen Cloud via the hackathon's referral link and submit the coupon form for free hackathon credits.
3. Join the Qwen Cloud Discord (support channel if you get blocked on quota/keys).
4. In the DashScope console, generate an **API key**. Store it only in `.env` (never commit it).
5. Confirm the OpenAI-compatible base URL for your account region, typically:
   ```
   https://dashscope-intl.aliyuncs.com/compatible-mode/v1
   ```
6. Sanity check with a raw curl before writing any app code:
   ```bash
   curl https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen-plus","messages":[{"role":"user","content":"say hi"}]}'
   ```

---

## 2. Ollama local setup (dev-only LLM stand-in)

1. Install Ollama, then pull a Qwen-family model so dev prompts transfer cleanly to DashScope later:
   ```bash
   ollama pull qwen2.5:7b
   ```
2. Verify it serves locally on the default port:
   ```bash
   ollama run qwen2.5:7b "say hi"
   curl http://localhost:11434/api/tags
   ```
3. Ollama's OpenAI-compatible endpoint is `http://localhost:11434/v1` — the backend's `OllamaProvider` points here when `LLM_PROVIDER=ollama`.
4. **Embeddings are always Qwen's `text-embedding-v3` API**, even in local dev — do not use a local embedding model. This keeps the pgvector column dimension consistent between dev and prod and avoids re-embedding everything before deployment.

---

## 3. Environment variables (`.env`)

Create `.env` from `.env.example` at repo root (backend reads it via `pydantic-settings`):

```bash
# --- LLM provider switch ---
LLM_PROVIDER=ollama              # ollama (local dev) | qwen (deployed/demo)

# --- Qwen Cloud (DashScope) ---
DASHSCOPE_API_KEY=sk-...
DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_CHAT_MODEL=qwen-plus
QWEN_EMBEDDING_MODEL=text-embedding-v3

# --- Ollama (local dev only) ---
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_CHAT_MODEL=qwen2.5:7b

# --- Postgres ---
DATABASE_URL=postgresql+asyncpg://memguard:memguard@localhost:5432/memguard

# --- Redis ---
REDIS_URL=redis://localhost:6379/0
SESSION_TTL_SECONDS=1800

# --- Governance tuning ---
CONFLICT_SIMILARITY_THRESHOLD=0.80
DEMO_TIME_SCALE=1                # set to e.g. 1440 to compress "days" into "minutes" for a live decay demo

# --- App ---
CORS_ORIGINS=http://localhost:3000
```

---

## 4. Local dev bring-up

```bash
git clone <your-repo-url> memguard && cd memguard
cp .env.example .env   # fill in DASHSCOPE_API_KEY at minimum

# 1. Data layer
docker compose -f infra/docker-compose.yml up -d postgres redis

# 2. Confirm pgvector extension loads (image: pgvector/pgvector:pg16)
docker compose exec postgres psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 3. Backend
cd backend
uv sync                       # or: poetry install
uv run alembic upgrade head   # applies migrations from db/migrations
uv run uvicorn app.main:app --reload --port 8000

# 4. Frontend (new terminal)
cd frontend
pnpm install
pnpm dev   # http://localhost:3000, expects backend at http://localhost:8000
```

Smoke test:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo_user","session_id":"s1","message":"I am on the Pro plan, my timezone is IST"}'
```

Run the scripted demo replay before ever hitting record:
```bash
uv run python scripts/replay_demo_beats.py
```

---

## 5. Alibaba Cloud deployment

**Do this on Day 1**, right after the local loop works — not after the full feature set is built. Even a bare `/health` endpoint reachable from the public internet is enough to bank the deployment proof early.

### 5.1 Provision ECS

1. Alibaba Cloud console → ECS → create instance (smallest general-purpose instance is enough; e.g. 2 vCPU / 4GB). OS: Ubuntu 22.04 LTS.
2. Configure the security group: allow inbound `22` (SSH, your IP only), `80`/`443` (HTTP/HTTPS, public), and temporarily `8000`/`3000` while testing without Nginx.
3. Note the public IP — this is what the deployment-proof recording will show.

### 5.2 Install Docker on the ECS instance

```bash
ssh root@<ecs-public-ip>
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin
```

### 5.3 Ship the app

```bash
# on your machine
git clone <your-repo-url> && cd memguard
scp -r . root@<ecs-public-ip>:/opt/memguard   # or just git clone directly on the box

# on the ECS box
cd /opt/memguard
cp .env.example .env
# edit .env: LLM_PROVIDER=qwen, real DASHSCOPE_API_KEY, DATABASE_URL pointing at the postgres container service name
docker compose -f infra/docker-compose.yml -f infra/docker-compose.prod.yml up -d --build
docker compose exec postgres psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"
docker compose exec backend alembic upgrade head
```

### 5.4 Nginx reverse proxy (optional but recommended polish)

Point `infra/nginx/memguard.conf` at the frontend (port 3000) and backend (`/api` → port 8000), run Nginx as a fourth container or install it on the host, then lock the security group back down to just `22/80/443`.

### 5.5 Capture the deployment proof

1. Record a **short, separate** screen capture: show a terminal on the ECS box (`docker ps`, `curl http://localhost/health`), and a browser hitting the public IP/domain — proving the backend genuinely runs on Alibaba Cloud, not localhost.
2. In the submission, link this recording alongside a pointer to `infra/alibaba-cloud/ecs-setup.md` (or the `docker-compose.prod.yml` / RDS connection setup, secrets redacted) as the "repo file that demonstrates Alibaba Cloud usage."

### 5.6 Optional stretch: RDS for PostgreSQL instead of containerized Postgres

Only attempt if Day 1 finishes early. Provision Alibaba Cloud RDS for PostgreSQL, enable the `vector` extension via the RDS console/parameter group, update `DATABASE_URL` to point at the RDS endpoint, drop the `postgres` service from `docker-compose.prod.yml`. Document the connection setup (redacted) in `infra/alibaba-cloud/rds-setup.md` — this becomes an even stronger "Alibaba Cloud service usage" proof file than a containerized DB.

---

## 6. Switching providers for the actual demo recording

Local dev defaults to `LLM_PROVIDER=ollama` to iterate fast/free. Before recording the **3-minute demo video**, always run against the **deployed Alibaba Cloud instance with `LLM_PROVIDER=qwen`** — the hackathon is judged on Qwen Cloud usage, so the demo video must show the real thing, not the Ollama fallback.

---

## 7. Troubleshooting quick-reference

| Symptom | Likely cause | Fix |
|---|---|---|
| `CREATE EXTENSION vector` fails | Wrong Postgres image | Use `pgvector/pgvector:pg16`, not plain `postgres:16` |
| Embedding dimension mismatch error on insert | Local embedding model used instead of Qwen's | Always call Qwen `text-embedding-v3` for embeddings, even in dev |
| Ollama model responds very differently than Qwen | Used a non-Qwen local model | Use `qwen2.5:7b` (or newer Qwen family) via Ollama, not llama/mistral |
| Conflict detector never fires | Similarity threshold too high, or embeddings not being written | Log raw cosine distances during dev; start threshold at 0.80 and tune down |
| ECS box unreachable | Security group not opened, or Docker not exposing ports | Check security group inbound rules and `docker compose ps` port bindings |
| Decay never triggers in demo | `ttl_days`/`DEMO_TIME_SCALE` too conservative | Set `DEMO_TIME_SCALE` high (e.g. 1440) only in the demo `.env`, never in the real deployment default |
