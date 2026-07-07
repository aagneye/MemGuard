from uuid import uuid4

from fastapi import APIRouter

from .schemas import NewSessionRequest, NewSessionResponse

router = APIRouter(tags=["session"])


@router.post("/session/new", response_model=NewSessionResponse)
def new_session(body: NewSessionRequest) -> NewSessionResponse:
    """Starts a fresh session_id for an existing user_id, proving cross-session recall
    is a property of user_id, not of the conversation thread."""
    return NewSessionResponse(session_id=f"s_{uuid4().hex[:12]}")
