from pydantic import BaseModel, Field

from .domain_types import MemoryStatus, ResolveAction, SourceType, TrustTier


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str = Field(min_length=1, max_length=4000)


class MemoryEvent(BaseModel):
    event_type: str
    detail: dict


class SessionTurn(BaseModel):
    role: str
    content: str


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
