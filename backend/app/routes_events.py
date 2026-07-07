from fastapi import APIRouter, Query

from .state import event_repo

router = APIRouter(tags=["events"])


@router.get("/events")
def list_events(user_id: str = Query(...), limit: int = 20) -> list[dict]:
    raw = event_repo.recent(user_id, limit=limit)
    result = []
    for event in raw:
        detail = event.get("detail", {})
        result.append(
            {
                "event_type": event.get("event_type", ""),
                "type": event.get("type", event.get("event_type", "")),
                "fact": detail.get("fact", detail.get("fact_text", "")),
                "trust_tier": detail.get("trust_tier"),
                "detail": detail,
                "created_at": event.get("created_at", ""),
            }
        )
    return result
