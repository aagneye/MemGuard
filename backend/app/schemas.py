from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


TrustTier = Literal["high", "medium", "low"]
MemorySource = Literal["user_stated", "tool_inferred", "document_extracted"]
MemoryStatus = Literal["active", "conflicted", "expired", "superseded"]


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str = Field(min_length=1)


class MemoryEventOut(BaseModel):
    event_type: str
    detail: dict


class ChatResponse(BaseModel):
    reply: str
    memory_events: list[MemoryEventOut]


class MemoryOut(BaseModel):
    id: str
    user_id: str
    fact_text: str
    trust_tier: TrustTier
    source: MemorySource
    status: MemoryStatus
    ttl_days: int
    created_at: datetime


class ResolveRequest(BaseModel):
    action: Literal["accept", "reject", "supersede"]
    superseded_by_fact: str | None = None
