"""Tests for GET /memories/search endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestMemorySearch:
    def test_search_returns_empty_for_unknown_user(self, client):
        r = client.get("/memories/search", params={"user_id": "nobody_abc", "q": "plan"})
        assert r.status_code == 200
        assert r.json() == []

    def test_search_finds_seeded_memory(self, client):
        client.post("/chat", json={"user_id": "search_user", "session_id": "s1", "message": "I'm on the Pro plan."})
        r = client.get("/memories/search", params={"user_id": "search_user", "q": "Pro plan", "top_k": 5})
        assert r.status_code == 200
        results = r.json()
        assert any("Pro" in m["fact_text"] for m in results)

    def test_search_respects_top_k(self, client):
        for i in range(5):
            client.post("/chat", json={"user_id": "topk_user", "session_id": f"s{i}", "message": f"My plan {i} is Pro."})
        r = client.get("/memories/search", params={"user_id": "topk_user", "q": "plan", "top_k": 2})
        assert r.status_code == 200
        assert len(r.json()) <= 2
