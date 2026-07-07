from .store import InMemoryStore, MemoryRecord


class MemoryRepository:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def active_for_user(self, user_id: str) -> list[MemoryRecord]:
        return self.store.list_active(user_id)

    def all_for_user(self, user_id: str) -> list[MemoryRecord]:
        return self.store.list_all(user_id)

    def create(
        self,
        *,
        user_id: str,
        fact_text: str,
        trust_tier: str,
        source: str,
        status: str = "active",
        ttl_days: int = 90,
    ) -> MemoryRecord:
        return self.store.add(
            user_id=user_id,
            fact_text=fact_text,
            trust_tier=trust_tier,
            source=source,
            status=status,
            ttl_days=ttl_days,
        )

    def resolve(self, memory_id: str, action: str, supersede_fact_text: str | None = None) -> MemoryRecord | None:
        return self.store.resolve(memory_id, action, supersede_fact_text)

    def mark_conflicted(self, records: list[MemoryRecord]) -> None:
        self.store.mark_conflicted(records)

    def link_conflict(self, first_id: str, second_id: str) -> None:
        self.store.link_conflict(first_id, second_id)
