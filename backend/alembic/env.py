"""Alembic environment for MemGuard database migrations.

Usage:
  cd backend
  alembic upgrade head     # apply all migrations
  alembic revision --autogenerate -m "add memories table"  # generate new migration

Set DATABASE_URL in .env before running. For pgvector support:
  1. Ensure your Postgres instance has the vector extension installed.
  2. Run: docker compose exec postgres psql -U memguard -d memguard -c "CREATE EXTENSION IF NOT EXISTS vector;"
"""
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

try:
    from app.config import settings as app_settings
    config.set_main_option("sqlalchemy.url", app_settings.database_url.replace("+asyncpg", ""))
except Exception:
    pass

target_metadata = None


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
