"""Tests for the MCP tool server endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.mcp_server import mcp_app


@pytest.fixture
def mcp_client():
    with TestClient(mcp_app) as c:
        yield c


class TestMcpToolDiscovery:
    def test_list_tools_returns_two_tools(self, mcp_client):
        r = mcp_client.get("/tools")
        assert r.status_code == 200
        tools = r.json()["tools"]
        names = {t["name"] for t in tools}
        assert "search_memory" in names
        assert "write_memory" in names


class TestMcpSearchMemory:
    def test_returns_empty_for_unknown_user(self, mcp_client):
        r = mcp_client.post("/tools/search_memory", json={"user_id": "nobody", "query": "plan"})
        assert r.status_code == 200
        assert r.json() == []


class TestMcpWriteMemory:
    def test_write_and_search_roundtrip(self, mcp_client):
        r = mcp_client.post(
            "/tools/write_memory",
            json={"user_id": "mcp_test_user", "fact": "I am on the Pro plan", "source": "tool_inferred"},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["event_type"] in ("stored", "conflict_detected", "flagged_poisoning")

        r2 = mcp_client.post(
            "/tools/search_memory",
            json={"user_id": "mcp_test_user", "query": "Pro plan", "top_k": 3},
        )
        assert r2.status_code == 200
        results = r2.json()
        assert any("Pro" in result["fact_text"] for result in results)
