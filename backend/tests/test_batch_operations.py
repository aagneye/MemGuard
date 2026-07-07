"""Tests for batch memory operations."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestBatchTouch:
    def test_batch_touch_updates_memories(self, client):
        client.post("/chat", json={"user_id": "batch_user", "session_id": "s1", "message": "I'm on Pro plan."})
        client.post("/chat", json={"user_id": "batch_user", "session_id": "s1", "message": "My timezone is IST."})
        mems = client.get("/memories", params={"user_id": "batch_user"}).json()
        ids = [m["id"] for m in mems]

        r = client.post("/memories/batch-touch", json={"memory_ids": ids, "user_id": "batch_user"})
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is True
        assert body["updated_count"] == len(ids)

    def test_batch_touch_ignores_wrong_user(self, client):
        client.post("/chat", json={"user_id": "batch_user2", "session_id": "s1", "message": "I'm on the Pro plan."})
        mems = client.get("/memories", params={"user_id": "batch_user2"}).json()
        ids = [m["id"] for m in mems]

        r = client.post("/memories/batch-touch", json={"memory_ids": ids, "user_id": "wrong_user"})
        assert r.status_code == 200
        assert r.json()["updated_count"] == 0


class TestBatchExpire:
    def test_batch_expire_changes_status(self, client):
        client.post("/chat", json={"user_id": "expire_user", "session_id": "s1", "message": "I'm on the Pro plan."})
        mems = client.get("/memories", params={"user_id": "expire_user"}).json()
        active = [m for m in mems if m["status"] == "active"]
        ids = [m["id"] for m in active]

        r = client.post("/memories/batch-expire", json={"memory_ids": ids, "user_id": "expire_user"})
        assert r.status_code == 200
        assert r.json()["expired_count"] == len(ids)

        mems_after = client.get("/memories", params={"user_id": "expire_user"}).json()
        active_after = [m for m in mems_after if m["status"] == "active"]
        assert len(active_after) == 0
