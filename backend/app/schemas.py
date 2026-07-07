from pydantic import BaseModel, Field

from .domain_types import MemoryStatus, ResolveAction, SourceType, TrustTier


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str = Field(min_length=1, max_length=4000)


class MemoryEvent(BaseModel):
    event_type: str
    type: str
    fact: str
    trust_tier: TrustTier | None = None
    detail: dict


class SessionTurn(BaseModel):
    role: str
    content: str


class NewSessionRequest(BaseModel):
    user_id: str


class NewSessionResponse(BaseModel):
    session_id: str


class DemoUser(BaseModel):
    id: str
    label: str


class UserProfile(BaseModel):
    id: str
    email: str
    name: str
    picture: str | None = None


class GoogleAuthRequest(BaseModel):
    credential: str = Field(min_length=10)


class AuthResponse(BaseModel):
    token: str
    user: UserProfile


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
    conflicts_with: str | None = None
    created_at: str


class TeamCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    owner_user_id: str


class TeamInviteRequest(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    invited_by: str


class TeamMemberAddRequest(BaseModel):
    user_id: str


class TeamInviteOut(BaseModel):
    id: str
    email: str
    invited_by: str
    status: str
    created_at: str


class TeamOut(BaseModel):
    id: str
    name: str
    owner_user_id: str
    members: list[str]
    invites: list[TeamInviteOut]
