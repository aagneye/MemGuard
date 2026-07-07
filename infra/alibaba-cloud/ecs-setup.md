# MemGuard — Alibaba Cloud ECS Deployment

This file is the **submission proof artifact** linked in the hackathon submission form to demonstrate that the backend runs on Alibaba Cloud. Redact all real credentials before committing; the deployment video records the live ECS instance.

## 1. Provision ECS instance

1. Alibaba Cloud Console → ECS → Create Instance.
2. Recommended spec: 2 vCPU / 4 GB RAM / 40 GB SSD (ecs.g7.large or equivalent in `ap-southeast-1` or nearest region to DashScope endpoint).
3. OS: Ubuntu 22.04 LTS 64-bit.
4. Security group — add inbound rules:
   - Port 22 (SSH) — your IP only
   - Port 80 (HTTP) — 0.0.0.0/0
   - Port 8000 (backend direct, for deployment proof) — 0.0.0.0/0 (close after recording)
5. Assign or allocate a static public IP (EIP).

## 2. Install Docker on the ECS instance

```bash
ssh root@<ECS_PUBLIC_IP>
curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin curl
systemctl enable docker
systemctl start docker
```

## 3. Clone the repo and configure environment

```bash
cd /opt
git clone https://github.com/aagneye/MemGuard.git
cd MemGuard
cp .env.example .env
```

Edit `.env` with your real values:

```env
LLM_PROVIDER=qwen
QWEN_API_KEY=<your-dashscope-api-key>
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_CHAT_MODEL=qwen-plus
DATABASE_URL=postgresql+asyncpg://memguard:memguard@postgres:5432/memguard
REDIS_URL=redis://redis:6379/0
CORS_ORIGINS=http://<ECS_PUBLIC_IP>,https://<YOUR_DOMAIN>
```

## 4. Start all services

```bash
cd /opt/MemGuard/infra
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Verify the pgvector extension loads:

```bash
docker compose exec postgres psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## 5. Verify deployment (record this as the proof video)

```bash
# Show running containers
docker compose ps

# Hit the health endpoint
curl http://<ECS_PUBLIC_IP>:8000/health

# Should return:
# {"ok":true,"version":"0.3.0","provider":"qwen",...}
```

Open `http://<ECS_PUBLIC_IP>/` in a browser to confirm the landing page loads.

## 6. Alibaba Cloud services used

| Service | How used |
|---|---|
| ECS | Runs backend, frontend, postgres, redis as Docker containers |
| EIP (Elastic IP) | Static public IP for the deployed demo |
| Security Group | Inbound rules for HTTP/HTTPS/SSH |
| DashScope (Qwen Cloud) | LLM provider for chat, extraction, and adjudication calls |

## 7. Optional: Alibaba Cloud RDS for PostgreSQL

If time allows, replace the containerized postgres with managed RDS:

1. RDS Console → Create PostgreSQL 16 instance.
2. Enable `vector` extension in parameter group.
3. Update `DATABASE_URL` in `.env` to the RDS endpoint.
4. Remove the `postgres` service from `docker-compose.yml` for the ECS run.

RDS connection string format (redacted example):
```
DATABASE_URL=postgresql+asyncpg://memguard:<password>@<rds-endpoint>.mysql.rds.aliyuncs.com:5432/memguard
```
