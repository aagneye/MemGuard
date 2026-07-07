# MemGuard

**Trust-Aware Memory Agent** — scores every memory for trust and provenance, detects conflicts and poisoning, and forgets stale facts. Built for the [Qwen Cloud Global AI Hackathon 2026](https://devpost.com) (Track 1: MemoryAgent).

MIT License · [Full docs](docs/README.md)

---

## Run locally

### Option A — Docker (easiest)

```bash
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
docker compose -f infra/docker-compose.yml up --build
```

Open **http://localhost:3000/demo** — no login required.

### Option B — Manual (backend + frontend separately)

**Terminal 1 — backend:**

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — frontend:**

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000/demo**.

### LLM provider

| Mode | `.env` setting | Requirement |
|---|---|---|
| Local dev (free) | `LLM_PROVIDER=ollama` | [Ollama](https://ollama.com) + `ollama pull qwen2.5:7b` |
| Production / demo video | `LLM_PROVIDER=qwen` | DashScope API key in `QWEN_API_KEY` |

Copy `.env.example` to `.env` and fill in values. Full variable reference: [docs/SETUP.md](docs/SETUP.md).

---

## Verify it works

```bash
# Health
curl http://localhost:8000/health

# Seed demo data and run all 5 beats
pip install httpx
python scripts/seed_demo_data.py
python scripts/replay_demo_beats.py
```

---

## What you'll see

| URL | Screen |
|---|---|
| http://localhost:3000 | Landing page |
| http://localhost:3000/demo | Chat + Memory Inspector + Governance Log |
| http://localhost:8000/docs | API documentation |

Pick **Alice** from the demo user dropdown and try:

> I'm on the Pro plan, my timezone is IST, and please always reply concisely.

Memories appear in the inspector with trust tiers. Click **New Session** and ask "What's my plan?" to see cross-session recall.

---

## Run tests

```bash
cd backend
pip install -e ".[dev]"
pytest tests/ -v
```

Or from repo root: `make test`

---

## Documentation

| Doc | What it covers |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | Full setup: Docker, Qwen, Ollama, ECS deploy, OAuth, troubleshooting |
| [docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md) | Beat-by-beat demo video script |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and governance logic |
| [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md) | Hackathon submission requirements |
| [docs/FUTURE_WORK.md](docs/FUTURE_WORK.md) | Post-submission development backlog |
| [docs/README.md](docs/README.md) | Index of all documentation |

---

## Project layout

```
MemGuard/
├── backend/          FastAPI + governance module + MCP server
├── frontend/         Next.js demo UI
├── infra/            Docker Compose, Nginx, Alibaba Cloud guides
├── scripts/          Seed data, demo replay, health check
└── docs/             Architecture, setup, demo guide
```

---

## Deploy to production

```bash
# Set LLM_PROVIDER=qwen and QWEN_API_KEY in .env first
docker compose -f infra/docker-compose.yml -f infra/docker-compose.prod.yml up -d --build
```

Step-by-step ECS guide: [infra/alibaba-cloud/ecs-setup.md](infra/alibaba-cloud/ecs-setup.md)

---

## License

MIT — see [LICENSE](LICENSE).
