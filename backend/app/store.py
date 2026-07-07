from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Iterable
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


@dataclass
class MemoryRecord:
    id: str
    user_id: str
    fact_text: str
    trust_tier: str
    source: str
    status: str = "active"
    ttl_days: int = 90
    created_at: datetime = field(default_factory=utc_now)
    superseded_by: str | None = None


class InMemoryStore:
    def __init__(self) -> None:
        self.memories: dict[str, MemoryRecord] = {}
        self.events: dict[str, list[dict]] = {}

    def list_active(self, user_id: str) -> list[MemoryRecord]:
        self.expire_stale(user_id)
        return [m for m in self.memories.values() if m.user_id == user_id and m.status == "active"]

    def list_all(self, user_id: str) -> list[MemoryRecord]:
        self.expire_stale(user_id)
        return [m for m in self.memories.values() if m.user_id == user_id]

    def get(self, memory_id: str) -> MemoryRecord | None:
        return self.memories.get(memory_id)

    def add(
        self,
        *,
        user_id: str,
        fact_text: str,
        trust_tier: str,
        source: str,
        status: str = "active",
        ttl_days: int = 90,
    ) -> MemoryRecord:
        memory = MemoryRecord(
            id=str(uuid4()),
            user_id=user_id,
            fact_text=fact_text,
            trust_tier=trust_tier,
            source=source,
            status=status,
            ttl_days=ttl_days,
        )
        self.memories[memory.id] = memory
        return memory

    def add_event(self, user_id: str, event_type: str, detail: dict) -> None:
        self.events.setdefault(user_id, []).append(
            {"event_type": event_type, "detail": detail, "created_at": utc_now().isoformat()}
        )

    def recent_events(self, user_id: str, limit: int = 10) -> list[dict]:
        return self.events.get(user_id, [])[-limit:]

    def expire_stale(self, user_id: str) -> None:
        now = utc_now()
        for memory in self.memories.values():
            if memory.user_id != user_id or memory.status != "active":
                continue
            if memory.created_at + timedelta(days=memory.ttl_days) < now:
                memory.status = "expired"

    def mark_conflicted(self, items: Iterable[MemoryRecord]) -> None:
        for item in items:
            item.status = "conflicted"

    def resolve(self, memory_id: str, action: str, supersede_fact_text: str | None = None) -> MemoryRecord | None:
        memory = self.memories.get(memory_id)
        if not memory:
            return None
        if action == "accept":
            memory.status = "active"
            return memory
        if action == "reject":
            memory.status = "expired"
            return memory
        if action == "supersede":
            new_memory = self.add(
                user_id=memory.user_id,
                fact_text=supersede_fact_text or memory.fact_text,
                trust_tier="high",
                source="user_stated",
                status="active",
                ttl_days=180,
            )
            memory.status = "superseded"
            memory.superseded_by = new_memory.id
            return new_memory
        return memory
