# MemGuard — Setup Guide

Complete guide for running MemGuard locally and deploying to Alibaba Cloud.

**Quick path:** clone → copy `.env` → `docker compose up` → open `http://localhost:3000/demo`.

---

## 0. Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Docker Desktop | latest | Postgres, Redis, backend, frontend containers |
| Python | 3.11+ | Backend (if running outside Docker) |
| Node.js | 20+ | Frontend (if running outside Docker) |
| Git | any | Clone the repo |

**Optional (recommended for free local LLM):**

- [Ollama](https://ollama.com/download) — run `qwen2.5:7b` locally without API costs

**Required for production demo / submission:**

- [Qwen Cloud (DashScope)](https://dashscope.aliyun.com/) API key — hackathon judging expects Qwen Cloud usage

---

## 1. Clone and configure

```bash
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
```

Edit `.env` at the repo root. Minimum for local dev with Ollama:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2.5:7b
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

For Qwen Cloud (production / demo recording):

```env
LLM_PROVIDER=qwen
QWEN_API_KEY=sk-your-dashscope-key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_CHAT_MODEL=qwen-plus
```

See `.env.example` for all variables (`DEMO_TIME_SCALE`, `RATE_LIMIT_RPM`, `DATABASE_URL`, etc.).

---

## 2. Run with Docker (recommended)

From the repo root:

```bash
docker compose -f infra/docker-compose.yml up --build
```

| Service | URL |
|---|---|
| Frontend (landing) | http://localhost:3000 |
| Demo | http://localhost:3000/demo |
| Backend API | http://localhost:8000 |
| OpenAPI docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

Stop:

```bash
docker compose -f infra/docker-compose.yml down
```

**Makefile shortcuts** (from repo root):

```bash
make up        # docker compose up
make up-d      # detached
make down      # stop
make seed      # pre-load demo memories
make verify    # run 5-beat replay script
make test      # backend pytest
```

---

## 3. Run without Docker (manual)

### 3a. Ollama (if using `LLM_PROVIDER=ollama`)

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "say hi"
```

Use a **Qwen-family** model so prompts behave similarly when you switch to DashScope.

### 3b. Backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3c. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000/demo.

---

## 4. Validate the install

### Health check

```bash
curl http://localhost:8000/health
# Expected: {"ok":true,"version":"0.3.0","provider":"ollama",...}
```

Or:

```bash
bash scripts/check_health.sh
```

### Smoke test (chat)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo_alice","session_id":"s1","message":"I am on the Pro plan, my timezone is IST"}'
```

### Seed and verify all 5 demo beats

```bash
pip install httpx   # if not already installed
python scripts/seed_demo_data.py --base-url http://localhost:8000
python scripts/replay_demo_beats.py --base-url http://localhost:8000
```

All beats should print `PASS` before you record the demo video. See [DEMO_GUIDE.md](DEMO_GUIDE.md) for the narration script.

---

## 5. Qwen Cloud account setup

1. Register for the hackathon on Devpost and claim Qwen Cloud hackathon credits.
2. In the DashScope console, create an **API key**. Store it only in `.env` — never commit it.
3. Confirm your region's compatible-mode base URL (typically `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`).
4. Sanity-check with curl:

```bash
curl https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $QWEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"say hi"}]}'
```

5. Set `LLM_PROVIDER=qwen` in `.env` and restart the backend.

**Important:** Record the demo video against a Qwen-backed deployment, not Ollama.

---

## 6. Postgres + Redis (optional, for persistence path)

The demo runs on an **in-memory store** by default — no database required for local testing.

To start Postgres (pgvector) and Redis alongside the app:

```bash
docker compose -f infra/docker-compose.yml up -d postgres redis
docker compose -f infra/docker-compose.yml exec postgres \
  psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

Apply migrations (when wiring Postgres as the live store):

```bash
cd backend
pip install alembic psycopg2-binary
alembic upgrade head
```

See [FUTURE_WORK.md](FUTURE_WORK.md) for the Postgres migration status.

---

## 7. Alibaba Cloud deployment

Full step-by-step: [infra/alibaba-cloud/ecs-setup.md](../infra/alibaba-cloud/ecs-setup.md).

Summary:

```bash
# On ECS (Ubuntu 22.04)
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
# Edit: LLM_PROVIDER=qwen, QWEN_API_KEY=..., CORS_ORIGINS=http://<ECS_IP>

cd infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Record a short video showing `docker compose ps` and `curl http://<ECS_IP>:8000/health` on the ECS box — required for submission.

Optional managed database: [infra/alibaba-cloud/rds-setup.md](../infra/alibaba-cloud/rds-setup.md).

---

## 8. Optional: Google OAuth + Dashboard

The public hackathon demo at `/demo` requires **no login**. Google OAuth and the `/dashboard` route are optional extras.

### Google Cloud Console

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project → **APIs & Services → OAuth consent screen**.
3. **Credentials → Create Credentials → OAuth client ID → Web application**.
4. Authorized JavaScript origins:
   - `http://localhost:3000`
   - your production frontend URL
5. Copy the **Client ID**.

### Environment variables

```env
GOOGLE_CLIENT_ID=<google-web-client-id>
NEXT_PUBLIC_GOOGLE_CLIENT_ID=<google-web-client-id>
```

- `NEXT_PUBLIC_GOOGLE_CLIENT_ID` — frontend Google Sign-In widget
- `GOOGLE_CLIENT_ID` — backend token verification

If `GOOGLE_CLIENT_ID` is empty, the backend uses a dev fallback profile.

### Validate OAuth flow

1. Open http://localhost:3000 (landing).
2. Sign in with Google → redirects to `/dashboard`.
3. Create a team, invite a member, send a chat message.

Auth/team APIs: `POST /auth/google/verify`, `GET /auth/me`, `POST /teams`, `GET /teams`, `POST /teams/{id}/invite`.

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Backend unreachable from frontend | Wrong `NEXT_PUBLIC_API_BASE` | Set to `http://localhost:8000` in `.env` |
| "Qwen API key is missing" in chat | `LLM_PROVIDER=qwen` without key | Set `QWEN_API_KEY` or switch to `ollama` |
| Ollama connection refused | Ollama not running | `ollama serve` or install Ollama |
| Empty memories after chat | Message has no extractable keywords | Try: "I'm on the Pro plan, timezone IST" |
| Docker port conflict | Port 3000/8000 in use | Stop other services or change ports in compose |
| `CREATE EXTENSION vector` fails | Wrong Postgres image | Use `pgvector/pgvector:pg16` from compose file |
| Decay not visible in demo | TTL too long | Set `DEMO_TIME_SCALE=1440` in `.env`, restart backend |
| CORS errors in browser | Origin not allowed | Add your URL to `CORS_ORIGINS` in `.env` |

---

## 10. Next steps

- Record demo: [DEMO_GUIDE.md](DEMO_GUIDE.md)
- Submission checklist: [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- Post-hackathon backlog: [FUTURE_WORK.md](FUTURE_WORK.md)
