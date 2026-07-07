"""Tests for GET /memories/{id}/similar endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestSimilarMemories:
    def test_similar_returns_empty_when_no_other_memories(self, client):
        client.post("/chat", json={"user_id": "sim_user", "session_id": "s1", "message": "I'm on the Pro plan."})
        mems = client.get("/memories", params={"user_id": "sim_user"}).json()
        assert len(mems) > 0
        mem_id = mems[0]["id"]

        r = client.get(f"/memories/{mem_id}/similar")
        assert r.status_code == 200

    def test_similar_returns_404_for_unknown(self, client):
        r = client.get("/memories/nonexistent-id/similar")
        assert r.status_code == 404

    def test_similar_excludes_source_memory(self, client):
        client.post("/chat", json={"user_id": "sim_user2", "session_id": "s1", "message": "I'm on the Pro plan."})
        client.post("/chat", json={"user_id": "sim_user2", "session_id": "s2", "message": "My timezone is IST."})
        mems = client.get("/memories", params={"user_id": "sim_user2"}).json()
        assert len(mems) > 0
        mem_id = mems[0]["id"]

        r = client.get(f"/memories/{mem_id}/similar?top_k=5")
        assert r.status_code == 200
        results = r.json()
        assert all(m["id"] != mem_id for m in results)
