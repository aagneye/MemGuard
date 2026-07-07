"""Tests for POST /demo/reset endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestDemoReset:
    def test_reset_clears_demo_user_memories(self, client):
        client.post("/chat", json={"user_id": "demo_alice", "session_id": "s1", "message": "I'm on the Pro plan."})
        memories_before = client.get("/memories", params={"user_id": "demo_alice"}).json()
        assert len(memories_before) > 0

        r = client.post("/demo/reset")
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is True
        assert "demo_alice" in body["cleared_users"]

        memories_after = client.get("/memories", params={"user_id": "demo_alice"}).json()
        assert memories_after == []

    def test_reset_returns_cleared_user_list(self, client):
        r = client.post("/demo/reset")
        assert r.status_code == 200
        assert isinstance(r.json()["cleared_users"], list)
