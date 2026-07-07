from typing import Literal

from pydantic import BaseModel, Field


TrustTier = Literal["high", "medium", "low"]
SourceType = Literal["user_stated", "tool_inferred", "document_extracted"]
MemoryStatus = Literal["active", "conflicted", "expired", "superseded"]
ResolveAction = Literal["accept", "reject", "supersede"]


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str = Field(min_length=1, max_length=4000)


class MemoryEvent(BaseModel):
    event_type: str
    detail: dict


class ChatResponse(BaseModel):
    reply: str
    memory_events: list[MemoryEvent]


class ResolveRequest(BaseModel):
    action: ResolveAction
    supersede_fact_text: str | None = None


class MemoryItem(BaseModel):
    id: str
    user_id: str
    fact_text: str
    trust_tier: TrustTier
    source: SourceType
    status: MemoryStatus
    ttl_days: int = 90
    superseded_by: str | None = None
