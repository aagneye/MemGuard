"""Tests for GET /memories/{id} single memory endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestSingleMemory:
    def test_get_memory_after_chat(self, client):
        r = client.post("/chat", json={"user_id": "single_user", "session_id": "s1", "message": "I'm on the Pro plan."})
        memories = client.get("/memories", params={"user_id": "single_user"}).json()
        assert len(memories) > 0
        mem_id = memories[0]["id"]

        r2 = client.get(f"/memories/{mem_id}")
        assert r2.status_code == 200
        body = r2.json()
        assert body["id"] == mem_id
        assert body["user_id"] == "single_user"
        assert "days_remaining" in body

    def test_get_nonexistent_memory_returns_404(self, client):
        r = client.get("/memories/does-not-exist")
        assert r.status_code == 404
