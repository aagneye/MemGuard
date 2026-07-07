"""Tests for memory decay (TTL) behavior.

The decay check is applied on-read: when a memory's last_confirmed_at +
ttl_days is in the past, the status changes to 'expired'. Tests use the
InMemoryStore directly to avoid HTTP overhead.
"""
import pytest
from datetime import datetime, timedelta, timezone

from app.store import InMemoryStore, MemoryRecord


def _past(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


class TestMemoryDecay:
    def test_memory_expires_when_ttl_exceeded(self):
        store = InMemoryStore()
        mem_id = store.add_memory("user1", "I prefer concise replies", "high", "user_stated", ttl_days=1)
        # Back-date last_confirmed_at to force expiry
        store.memories[mem_id].last_confirmed_at = _past(days=2)

        active = store.active_memories_for("user1")
        assert not any(m.id == mem_id for m in active)

    def test_memory_survives_within_ttl(self):
        store = InMemoryStore()
        mem_id = store.add_memory("user2", "Timezone is IST", "high", "user_stated", ttl_days=30)
        store.memories[mem_id].last_confirmed_at = _past(days=5)

        active = store.active_memories_for("user2")
        assert any(m.id == mem_id for m in active)

    def test_memory_with_no_ttl_never_expires(self):
        store = InMemoryStore()
        mem_id = store.add_memory("user3", "On the Pro plan", "high", "user_stated", ttl_days=None)
        store.memories[mem_id].last_confirmed_at = _past(days=9999)

        active = store.active_memories_for("user3")
        assert any(m.id == mem_id for m in active)
