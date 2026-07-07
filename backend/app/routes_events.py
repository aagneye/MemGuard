from fastapi import APIRouter, Query

from .state import event_repo

router = APIRouter(tags=["events"])


@router.get("/events")
def list_events(user_id: str = Query(...), limit: int = 20) -> list[dict]:
    return event_repo.recent(user_id, limit=limit)
