"""Tests for GET /memories/{id}/provenance endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestProvenance:
    def test_provenance_includes_memory_fields(self, client):
        client.post("/chat", json={"user_id": "prov_user", "session_id": "s1", "message": "I'm on the Pro plan."})
        mems = client.get("/memories", params={"user_id": "prov_user"}).json()
        assert len(mems) > 0
        mem_id = mems[0]["id"]

        r = client.get(f"/memories/{mem_id}/provenance")
        assert r.status_code == 200
        body = r.json()
        assert "memory" in body
        assert body["memory"]["id"] == mem_id
        assert "events" in body
        assert isinstance(body["events"], list)

    def test_provenance_404_for_unknown(self, client):
        r = client.get("/memories/unknown-id/provenance")
        assert r.status_code == 404
