"""Initial memories and events tables.

Revision ID: 001
Creates:
  - memories: persistent fact store with pgvector embedding column
  - memory_events: audit log of all memory lifecycle changes
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "memories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("fact_text", sa.Text, nullable=False),
        sa.Column("trust_tier", sa.String(16), nullable=False),
        sa.Column("source", sa.String(32), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("ttl_days", sa.Integer, nullable=True),
        sa.Column("superseded_by", sa.String(36), nullable=True),
        sa.Column("conflicts_with", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_confirmed_at", sa.DateTime(timezone=True), nullable=False),
        # Embedding column: vector(1024) for text-embedding-v3
        # Added as raw SQL since SQLAlchemy doesn't have a built-in Vector type
    )
    op.execute("ALTER TABLE memories ADD COLUMN IF NOT EXISTS embedding vector(1024)")
    op.execute("CREATE INDEX IF NOT EXISTS memories_embedding_idx ON memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)")

    op.create_table(
        "memory_events",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()::text")),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("memory_id", sa.String(36), nullable=True),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("detail", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("memory_events")
    op.drop_table("memories")
