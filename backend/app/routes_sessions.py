from fastapi import APIRouter, Query

from .state import session_repo

router = APIRouter(tags=["sessions"])


@router.get("/sessions/{session_id}/turns")
def list_session_turns(session_id: str, limit: int = Query(default=12, ge=1, le=100)) -> list[dict]:
    return session_repo.get_turns(session_id, limit=limit)


@router.delete("/sessions/{session_id}")
def clear_session(session_id: str) -> dict:
    session_repo.clear(session_id)
    return {"ok": True, "session_id": session_id}
