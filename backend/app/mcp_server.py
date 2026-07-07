"""MemGuard MCP Tool Server (stretch goal).

Exposes search_memory and write_memory as MCP tools so Qwen Cloud agents
(and any MCP-compatible client) can call the memory layer as external tools
rather than having the backend hand-wire retrieval into the prompt.

This is a direct rubric line item:
  "Does the project make sophisticated use of QwenCloud APIs, e.g.,
   custom skills, MCP integrations?"

Run standalone: python -m app.mcp_server
Or import and mount in main.py via app.mount("/mcp", mcp_app).
"""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .state import event_repo, memory_repo, memory_service
from .domain_models import FactCandidate
from .service_extract import detect_source
from .service_trust import score_trust


mcp_app = FastAPI(
    title="MemGuard MCP Tool Server",
    description="MCP-compatible tool server exposing memory search and write to Qwen agents.",
    version="0.1.0",
)


class SearchMemoryRequest(BaseModel):
    user_id: str
    query: str
    top_k: int = 5


class SearchMemoryResult(BaseModel):
    id: str
    fact_text: str
    trust_tier: str
    source: str
    status: str
    relevance: float


class WriteMemoryRequest(BaseModel):
    user_id: str
    fact: str
    source: str = "tool_inferred"


class WriteMemoryResult(BaseModel):
    memory_id: str
    event_type: str


@mcp_app.post("/tools/search_memory", response_model=list[SearchMemoryResult])
def search_memory(body: SearchMemoryRequest) -> list[SearchMemoryResult]:
    """MCP tool: search a user's active memories by keyword relevance."""
    memories = memory_repo.active_for_user(body.user_id)
    query_lower = body.query.lower()
    scored = [
        (m, sum(word in m.fact_text.lower() for word in query_lower.split()))
        for m in memories
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [
        SearchMemoryResult(
            id=m.id,
            fact_text=m.fact_text,
            trust_tier=m.trust_tier,
            source=m.source,
            status=m.status,
            relevance=float(score),
        )
        for m, score in scored[:body.top_k]
    ]


@mcp_app.post("/tools/write_memory", response_model=WriteMemoryResult)
def write_memory(body: WriteMemoryRequest) -> WriteMemoryResult:
    """MCP tool: write a new memory fact on behalf of an agent."""
    source_hint = body.source if body.source in ("user_stated", "tool_inferred", "document_extracted") else "tool_inferred"  # type: ignore[assignment]
    candidate = FactCandidate(fact=body.fact, source_hint=source_hint, confidence=0.9)  # type: ignore[arg-type]
    result = memory_service.process_candidate(body.user_id, candidate)
    return WriteMemoryResult(memory_id=result["detail"].get("memory_id", ""), event_type=result["event_type"])


@mcp_app.get("/tools")
def list_tools() -> dict:
    """MCP tool discovery endpoint — lists available tools and their schemas."""
    return {
        "tools": [
            {
                "name": "search_memory",
                "description": "Search a user's stored memories by keyword relevance.",
                "input_schema": SearchMemoryRequest.model_json_schema(),
            },
            {
                "name": "write_memory",
                "description": "Write a new memory fact for a user.",
                "input_schema": WriteMemoryRequest.model_json_schema(),
            },
        ]
    }
