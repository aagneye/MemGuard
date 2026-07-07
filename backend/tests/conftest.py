"""Shared pytest fixtures for backend tests."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import InMemoryStore
from app.state import memory_repo, event_repo, session_repo


@pytest.fixture
def client():
    """TestClient for the full FastAPI application."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def fresh_store():
    """A fresh InMemoryStore with no data."""
    return InMemoryStore()


@pytest.fixture(autouse=True)
def isolate_store():
    """Clear the global in-memory store before each test so tests don't bleed state."""
    memory_repo._store.memories.clear()
    memory_repo._store.events.clear()
    memory_repo._store.sessions.clear()
    yield
    memory_repo._store.memories.clear()
    memory_repo._store.events.clear()
    memory_repo._store.sessions.clear()
