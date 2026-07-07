# MemGuard — Production Deployment Guide

End-to-end guide to take MemGuard from your working local setup to a **public, Qwen-backed production deployment** on Alibaba Cloud ECS.

**You already have local working?** Skip to [§4 Deploy to Alibaba Cloud ECS](#4-deploy-to-alibaba-cloud-ecs).

Related docs:
- Local dev: [SETUP.md](SETUP.md)
- ECS detail / submission proof: [../infra/alibaba-cloud/ecs-setup.md](../infra/alibaba-cloud/ecs-setup.md)
- Managed Postgres (optional): [../infra/alibaba-cloud/rds-setup.md](../infra/alibaba-cloud/rds-setup.md)
- Demo video script: [DEMO_GUIDE.md](DEMO_GUIDE.md)

---

## 1. What production looks like

```
Internet
    │
    ▼
┌─────────────────────────────────────────┐
│  Alibaba Cloud ECS (Ubuntu 22.04)       │
│                                         │
│  Nginx :80  ──► frontend :3000 (Next.js)│
│            └──► backend  :8000 (FastAPI)│
│                                         │
│  postgres (pgvector)  redis             │
└─────────────────────────────────────────┘
    │
    ▼
DashScope (Qwen Cloud) — chat, extraction, adjudication, embeddings
```

| URL (after deploy) | What it serves |
|---|---|
| `http://<ECS_IP>/` | Landing page |
| `http://<ECS_IP>/demo` | Main demo (judged screen) |
| `http://<ECS_IP>/docs` | API documentation |
| `http://<ECS_IP>/api/*` | Backend API (via Nginx proxy) |

---

## 2. Pre-deploy checklist

Before you touch the cloud:

- [ ] Local demo works at `http://localhost:3000/demo` (chat + Memory Inspector)
- [ ] `python scripts/replay_demo_beats.py` passes all 5 beats (backend on `:8000`)
- [ ] Qwen Cloud (DashScope) API key obtained and tested
- [ ] GitHub repo is **public** with MIT license visible
- [ ] `.env` values ready (see §3) — **never commit real keys**

**Hackathon requirement:** Production demo and video must use **`LLM_PROVIDER=qwen`**, not Ollama.

---

## 3. Production `.env`

On the server, create `/opt/MemGuard/.env` from `.env.example`:

```env
# ── LLM (required for production) ─────────────────────────────────────────
LLM_PROVIDER=qwen
QWEN_API_KEY=sk-your-dashscope-key-here
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_CHAT_MODEL=qwen-plus

# ── Frontend (CRITICAL — baked in at Next.js build time) ─────────────────
# Use your ECS public IP or domain. Nginx proxies /api → backend.
NEXT_PUBLIC_API_BASE=http://YOUR_ECS_PUBLIC_IP/api

# ── CORS ─────────────────────────────────────────────────────────────────
CORS_ORIGINS=http://YOUR_ECS_PUBLIC_IP,https://YOUR_DOMAIN_IF_ANY

# ── Database (container names match docker-compose service names) ────────
DATABASE_URL=postgresql+asyncpg://memguard:memguard@postgres:5432/memguard
REDIS_URL=redis://redis:6379/0

# ── Governance tuning ────────────────────────────────────────────────────
DEMO_TIME_SCALE=1.0
RATE_LIMIT_RPM=60
SIMILARITY_THRESHOLD=0.8
SESSION_TTL_SECONDS=1800

# ── Server ───────────────────────────────────────────────────────────────
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

Replace `YOUR_ECS_PUBLIC_IP` with your Elastic IP after provisioning.

**Security:** Change the default Postgres password (`memguard`) if the database port is ever exposed. For the default compose setup, Postgres is internal to Docker only.

---

## 4. Deploy to Alibaba Cloud ECS

### 4.1 Provision the server

1. [Alibaba Cloud Console](https://www.alibabacloud.com/) → **ECS** → **Create Instance**
2. **Region:** pick one close to DashScope (e.g. `ap-southeast-1`)
3. **Image:** Ubuntu 22.04 LTS 64-bit
4. **Instance type:** 2 vCPU / 4 GB RAM minimum (e.g. `ecs.g7.large`)
5. **Storage:** 40 GB SSD
6. **Elastic IP (EIP):** allocate and bind a static public IP
7. **Security group inbound rules:**

| Port | Source | Purpose |
|---|---|---|
| 22 | Your IP only | SSH |
| 80 | 0.0.0.0/0 | HTTP (Nginx) |
| 443 | 0.0.0.0/0 | HTTPS (optional, after TLS setup) |
| 8000 | 0.0.0.0/0 | Temporary — for deployment proof video only; close after |

### 4.2 Install Docker on ECS

```bash
ssh root@YOUR_ECS_PUBLIC_IP

curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin git curl
systemctl enable docker
systemctl start docker
```

### 4.3 Clone and configure

```bash
cd /opt
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
nano .env   # fill in QWEN_API_KEY, NEXT_PUBLIC_API_BASE, CORS_ORIGINS
```

Set `NEXT_PUBLIC_API_BASE=http://YOUR_ECS_PUBLIC_IP/api` **before** building — Next.js embeds this at build time.

### 4.4 Build and start (production compose)

```bash
cd /opt/MemGuard/infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

This starts:
- **postgres** (pgvector), **redis**, **backend** (2 workers), **frontend** (production build), **nginx** (port 80)

First build takes 5–10 minutes (frontend `npm run build`).

### 4.5 Enable pgvector extension

```bash
cd /opt/MemGuard/infra
docker compose exec postgres psql -U memguard -d memguard \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

> **Note:** The app currently uses an in-memory store for memories. Postgres/Redis are running and ready for the persistence migration described in [FUTURE_WORK.md](FUTURE_WORK.md). The demo works without additional DB wiring.

### 4.6 Watch logs during first boot

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
```

Wait until you see backend `MemGuard starting` and frontend `Ready`.

---

## 5. Verify production

Run these on the ECS box or from your laptop:

```bash
# All containers healthy
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps

# Backend health
curl http://YOUR_ECS_PUBLIC_IP/api/health
# or directly: curl http://YOUR_ECS_PUBLIC_IP:8000/health

# Expected: {"ok":true,"version":"0.3.0","provider":"qwen",...}

# Seed demo data (from ECS host, with Python + httpx installed)
pip install httpx
python scripts/seed_demo_data.py --base-url http://YOUR_ECS_PUBLIC_IP/api

# Verify all 5 beats
python scripts/replay_demo_beats.py --base-url http://YOUR_ECS_PUBLIC_IP/api
```

**Browser checks:**

| URL | Expected |
|---|---|
| `http://YOUR_ECS_PUBLIC_IP/` | Landing page with "Launch Demo" |
| `http://YOUR_ECS_PUBLIC_IP/demo` | Chat + Memory Inspector (your screenshot) |
| `http://YOUR_ECS_PUBLIC_IP/docs` | FastAPI Swagger UI |

If the demo loads but chat fails with a network error, `NEXT_PUBLIC_API_BASE` is wrong — it must be `http://YOUR_ECS_PUBLIC_IP/api` and you must **rebuild** the frontend:

```bash
cd /opt/MemGuard/infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build frontend
```

---

## 6. Record deployment proof (hackathon submission)

Record a **short separate video** (not the main demo) showing:

1. SSH into ECS: `ssh root@YOUR_ECS_PUBLIC_IP`
2. `docker compose ps` — all services `running`
3. `curl http://localhost:8000/health` — JSON with `"provider":"qwen"`
4. Browser on the ECS public IP showing `/demo` loading

Link this video + [ecs-setup.md](../infra/alibaba-cloud/ecs-setup.md) in your Devpost submission.

---

## 7. Record the main demo video

Follow [DEMO_GUIDE.md](DEMO_GUIDE.md) beat-by-beat against the **production URL** (`http://YOUR_ECS_PUBLIC_IP/demo`), not localhost.

Before recording:

```bash
python scripts/seed_demo_data.py --base-url http://YOUR_ECS_PUBLIC_IP/api
python scripts/replay_demo_beats.py --base-url http://YOUR_ECS_PUBLIC_IP/api
```

Use **Alice** in the demo user dropdown. Narrate trust tiers, poisoning, conflict resolution, and the governance log.

---

## 8. Optional: custom domain + HTTPS

1. Point your domain's **A record** to the ECS Elastic IP.
2. Update `.env`:
   ```env
   NEXT_PUBLIC_API_BASE=https://yourdomain.com/api
   CORS_ORIGINS=https://yourdomain.com
   ```
3. Rebuild frontend: `docker compose ... up -d --build frontend`
4. Install Certbot on ECS and obtain a certificate, or use Alibaba Cloud SSL.
5. Update `infra/nginx/memguard.conf` to listen on 443 with SSL cert paths.

---

## 9. Optional: managed RDS instead of container Postgres

For stronger "Alibaba Cloud services" proof, use RDS:

See [rds-setup.md](../infra/alibaba-cloud/rds-setup.md).

Summary: create RDS PostgreSQL 16 → enable `vector` extension → update `DATABASE_URL` in `.env` → remove `postgres` service from compose → redeploy.

---

## 10. Day-2 operations

### Update to latest code

```bash
cd /opt/MemGuard
git pull
cd infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### View logs

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f frontend
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f nginx
```

### Restart a single service

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml restart backend
```

### Reset demo state (before a live presentation)

```bash
curl -X POST http://YOUR_ECS_PUBLIC_IP/api/demo/reset
```

Or click **Reset Demo** in the UI.

### Stop everything

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```

---

## 11. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Demo UI loads, chat says "Backend unreachable" | Wrong `NEXT_PUBLIC_API_BASE` | Set to `http://IP/api`, rebuild frontend |
| CORS error in browser console | Origin not in `CORS_ORIGINS` | Add your public URL to `.env`, restart backend |
| `"provider":"ollama"` in health | Forgot to set Qwen | `LLM_PROVIDER=qwen` + `QWEN_API_KEY` in `.env`, restart backend |
| Qwen API errors | Invalid key or wrong region URL | Test with curl (see [SETUP.md](SETUP.md) §5) |
| `docker compose` build fails on frontend | Out of memory on small ECS | Use 4 GB+ RAM instance; or build frontend locally and push image |
| Port 80 connection refused | Nginx not started | `docker compose ps`; check nginx logs |
| Memories don't persist after restart | In-memory store (by design) | See [FUTURE_WORK.md](FUTURE_WORK.md) for Postgres wiring |

---

## 12. Submission checklist

Walk [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) before submitting to Devpost:

- [ ] Public GitHub repo + MIT license
- [ ] Production URL works (`/demo`)
- [ ] Alibaba Cloud deployment proof video
- [ ] ~3 min demo video (5 beats)
- [ ] Architecture diagram PNG in README
- [ ] Track 1 — MemoryAgent declared

---

## Quick reference — one-page deploy

```bash
# On ECS (Ubuntu 22.04, Docker installed)
cd /opt && git clone https://github.com/aagneye/MemGuard.git && cd MemGuard
cp .env.example .env
# Edit: LLM_PROVIDER=qwen, QWEN_API_KEY, NEXT_PUBLIC_API_BASE=http://IP/api, CORS_ORIGINS

cd infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose exec postgres psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"

curl http://localhost:8000/health
# Open http://YOUR_ECS_PUBLIC_IP/demo in browser
```
