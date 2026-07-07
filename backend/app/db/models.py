"""SQLAlchemy ORM models for the Postgres + pgvector persistence layer.

These models define the schema that `alembic/versions/001_initial_memories.py`
creates. The in-memory store (InMemoryStore) mirrors this schema for dev.

Not yet wired into the routes — the current backend uses InMemoryStore.
This file is the migration target when Postgres is enabled.
"""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class Base(DeclarativeBase):
    pass


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    fact_text: Mapped[str] = mapped_column(Text, nullable=False)
    trust_tier: Mapped[str] = mapped_column(String(16), nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    ttl_days: Mapped[int | None] = mapped_column(Integer, nullable=True, default=90)
    superseded_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    conflicts_with: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    last_confirmed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    # Embedding stored as raw text (hex) in SQLite; as vector(1024) in Postgres via Alembic
    # embedding: handled by separate ALTER TABLE in the migration for pgvector support


class MemoryEvent(Base):
    __tablename__ = "memory_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    memory_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("memories.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
