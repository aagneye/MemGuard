from .store import InMemoryStore


class EventRepository:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def add(self, user_id: str, event_type: str, detail: dict) -> None:
        self.store.add_event(user_id, event_type, detail)

    def recent(self, user_id: str, limit: int = 20) -> list[dict]:
        return self.store.recent_events(user_id, limit=limit)
