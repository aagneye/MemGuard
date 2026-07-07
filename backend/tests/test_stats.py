"""Tests for GET /stats endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestUserStats:
    def test_stats_empty_user(self, client):
        r = client.get("/stats", params={"user_id": "nobody_stats"})
        assert r.status_code == 200
        body = r.json()
        assert body["total_memories"] == 0
        assert body["total_events"] == 0

    def test_stats_after_chat(self, client):
        client.post("/chat", json={"user_id": "stats_user", "session_id": "s1", "message": "I'm on the Pro plan."})
        r = client.get("/stats", params={"user_id": "stats_user"})
        assert r.status_code == 200
        body = r.json()
        assert body["total_memories"] > 0
        assert body["total_events"] > 0
        assert "stored" in body["events_by_type"]


class TestGlobalStats:
    def test_global_stats_returns_counts(self, client):
        r = client.get("/stats/global")
        assert r.status_code == 200
        body = r.json()
        assert "total_memories" in body
        assert "demo_user_count" in body
        assert body["demo_user_count"] > 0
