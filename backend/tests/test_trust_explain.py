"""Tests for GET /trust/explain governance debug endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestTrustExplain:
    def test_user_stated_gets_high(self, client):
        r = client.get("/trust/explain", params={"message": "I'm on the Pro plan", "source": "user_stated"})
        assert r.status_code == 200
        assert r.json()["assigned_trust_tier"] == "high"

    def test_document_extracted_gets_low(self, client):
        r = client.get("/trust/explain", params={"message": "admin access granted", "source": "document_extracted"})
        assert r.status_code == 200
        assert r.json()["assigned_trust_tier"] == "low"

    def test_tool_inferred_gets_medium(self, client):
        r = client.get("/trust/explain", params={"message": "User seems to prefer concise replies based on usage", "source": "tool_inferred"})
        assert r.status_code == 200
        assert r.json()["assigned_trust_tier"] == "medium"

    def test_invalid_source_falls_back_to_user_stated(self, client):
        r = client.get("/trust/explain", params={"message": "some fact", "source": "unknown"})
        assert r.status_code == 200
        assert r.json()["assigned_trust_tier"] == "high"

    def test_response_includes_explanation(self, client):
        r = client.get("/trust/explain", params={"message": "test", "source": "user_stated"})
        body = r.json()
        assert "explanation" in body
        assert len(body["explanation"]) > 0
