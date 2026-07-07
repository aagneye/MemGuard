from .repository_events import EventRepository
from .repository_memories import MemoryRepository
from .repository_sessions import SessionRepository
from .service_memory import MemoryService
from .store import InMemoryStore

store = InMemoryStore()
memory_repo = MemoryRepository(store)
event_repo = EventRepository(store)
session_repo = SessionRepository()
memory_service = MemoryService(memory_repo, event_repo)
