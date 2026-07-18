# MemGuard — Local Setup Guide

How to run MemGuard **on your machine** for development and testing.

**Production / Alibaba Cloud hosting** → see **[PRODUCTION.md](PRODUCTION.md)**  
**Hackathon “What to Submit” checklist** → see **[SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)**

---

## What you get locally

| Piece | Local choice |
|---|---|
| Backend | FastAPI on `localhost:8000` |
| Frontend | Next.js on `localhost:3000` |
| Reasoning + fact extraction | **Ollama** (Qwen-family model) *or* DashScope if you set a key |
| Memory | In-memory store by default (fast). Optional Docker Postgres + Redis |
| Governance | Trust scorer, poison guard, conflict detector, decay — all in the backend |

---

## Prerequisites

| Tool | Why |
|---|---|
| Git | Clone the repo |
| Python 3.11+ *(or 3.10 works for demo)* | Backend |
| Node.js 20+ | Frontend |
| [Ollama](https://ollama.com) | Local LLM (recommended for free local runs) |
| Docker Desktop *(optional)* | One-command stack with Postgres/Redis |

---

## Step 1 — Clone and create `.env`

```bash
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
```

### Local `.env` (Ollama — recommended)

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2.5-coder:7b
NEXT_PUBLIC_API_BASE=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Use any **Qwen-family** model you already have (`ollama list`). Examples: `qwen2.5-coder:7b`, `qwen2.5:14b-instruct-q4_K_M`.

### Optional — use Qwen Cloud even locally

```env
LLM_PROVIDER=qwen
QWEN_API_KEY=sk-your-dashscope-key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_CHAT_MODEL=qwen-plus
```

Get the key from [DashScope](https://dashscope.aliyun.com/). Never commit real keys.

---

## Step 2 — Start Ollama (if `LLM_PROVIDER=ollama`)

```bash
ollama serve
ollama list
# If your chosen model is missing:
# ollama pull qwen2.5-coder:7b
```

Without Ollama running, chat returns a fallback (“could not reach the model”) but memory governance still works.

---

## Step 3 — Run the app

### Option A — Manual (two terminals)

**Terminal 1 — backend**

Linux / macOS:

```bash
cd backend
python3 -m pip install fastapi "uvicorn[standard]" pydantic pydantic-settings openai httpx google-auth pytest
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Windows (PowerShell) — do **not** use bare `python` if you see *“Python was not found… Microsoft Store”*. That is the Store alias, not a real install. Use your installed `python.exe` (3.10+):

```powershell
cd backend
$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
# If 3.12 is missing, try Python310 instead:
# $py = "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
& $py -m pip install fastapi "uvicorn[standard]" pydantic pydantic-settings openai httpx google-auth pytest
& $py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Find your install if the path differs:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Programs\Python" -Recurse -Filter python.exe |
  Where-Object { $_.FullName -notmatch '\\Lib\\venv\\' } |
  Select-Object -ExpandProperty FullName
```

Optional fix so `python` works in new terminals: add that folder to PATH, or turn off **Settings → Apps → Advanced app settings → App execution aliases →** `python.exe` / `python3.exe`.

**Terminal 2 — frontend**

```bash
cd frontend
npm install
npm run dev
```

### Option B — Docker Compose

```bash
docker compose -f infra/docker-compose.yml up --build
```

This also starts Postgres (pgvector) and Redis containers for later persistence work.

---

## Step 4 — Open and verify

| URL | Purpose |
|---|---|
| http://localhost:3000/demo | Main demo (no login) |
| http://localhost:3000 | Landing |
| http://localhost:8000/docs | API docs |
| http://localhost:8000/health | Health JSON |

```bash
curl http://localhost:8000/health
```

Expect `"ok": true`. With Ollama: `"provider":"ollama"`.

Smoke chat:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"demo_alice\",\"session_id\":\"s1\",\"message\":\"I am on the Pro plan, my timezone is IST\"}"
```

Optional full 5-beat check (same `$py` as above on Windows):

```bash
python3 -m pip install httpx
python3 scripts/seed_demo_data.py --base-url http://localhost:8000
python3 scripts/replay_demo_beats.py --base-url http://localhost:8000
```

---

## Optional local extras

### Postgres + Redis containers

```bash
docker compose -f infra/docker-compose.yml up -d postgres redis
docker compose -f infra/docker-compose.yml exec postgres \
  psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

The live demo path still uses the in-memory store unless you wire Postgres (see [FUTURE_WORK.md](FUTURE_WORK.md)). Schema/migrations live under `backend/alembic/`.

### Google OAuth / dashboard

Not required for the public `/demo`. Optional steps remain under the dashboard routes if you enable `GOOGLE_CLIENT_ID` in `.env`.

---

## Troubleshooting (local)

| Symptom | Fix |
|---|---|
| `Python was not found… Microsoft Store` | Store alias stole `python`. Use full path to `Python312\python.exe` (see Step 3), or disable App execution aliases |
| `WinError 32` / file in use during `pip install` | Stop other Python/uvicorn windows first (`Ctrl+C`), then re-run install |
| `No module named 'fastapi'` | Install failed or incomplete — re-run the Step 3 `pip install` line, then start uvicorn |
| Chat: “could not reach the model” | Start `ollama serve`; match `OLLAMA_MODEL` to `ollama list` |
| Ollama `404` on `/v1/chat/completions` | Wrong/missing model name in `.env` |
| Frontend cannot reach API | `NEXT_PUBLIC_API_BASE=http://localhost:8000` |
| CORS errors | Add your origin to `CORS_ORIGINS` |
| Stats bar shows `0` but Inspector has memories | Refresh after chat; Inspector is source of truth |

---

## Next step — production on Alibaba Cloud

When local demo works, host the **FastAPI backend on Alibaba Cloud ECS** with **Qwen via DashScope** for the hackathon deployment proof:

→ **[PRODUCTION.md](PRODUCTION.md)**
