# MemGuard — Alibaba Cloud RDS Setup (Optional)

Use managed RDS instead of the containerized Postgres for better reliability.

## 1. Create an RDS PostgreSQL 16 instance

1. Alibaba Cloud Console → RDS → Create Instance.
2. Database Engine: PostgreSQL 16.
3. Storage: 20 GB SSD (sufficient for hackathon scale).
4. Network: same VPC as your ECS instance.
5. Instance type: rds.pg.c1m2.2c4g or equivalent.
6. Enable public endpoint for initial setup (disable after migration).

## 2. Enable pgvector extension

In the RDS console:
1. Click the instance → Parameter Groups.
2. Search for `shared_preload_libraries` → add `vector`.
3. Apply and restart the instance.

Alternatively, run after connecting:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 3. Create database and user

```sql
CREATE DATABASE memguard;
CREATE USER memguard WITH PASSWORD '<strong-password>';
GRANT ALL PRIVILEGES ON DATABASE memguard TO memguard;
```

## 4. Update .env

```env
DATABASE_URL=postgresql+asyncpg://memguard:<password>@<rds-endpoint>.mysql.rds.aliyuncs.com:5432/memguard
```

## 5. Run Alembic migrations

```bash
cd /opt/MemGuard/backend
pip install alembic psycopg2-binary
alembic upgrade head
```

## 6. Remove postgres service from docker-compose

In `docker-compose.yml`, comment out or remove the `postgres` service block.
Update the `backend` service's `depends_on` to remove the postgres dependency.
