"""Demo state debug endpoint — shows full in-memory state for debugging.

GET /demo/state

Returns all memories, events, and session counts per demo user.
Useful during the demo recording to show the "before/after" of demo beats.
Not exposed in production builds (DEMO_MODE must be enabled).
"""
from fastapi import APIRouter, HTTPException

from .config import settings
from .demo_users import DEMO_USERS
from .state import event_repo, memory_repo

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/state")
def get_demo_state() -> dict:
    """Return summary of all demo user memories and event counts."""
    result = {}
    for user in DEMO_USERS:
        user_id = user["id"]
        memories = memory_repo.all_for_user(user_id)
        events = event_repo.recent(user_id, limit=50)
        result[user_id] = {
            "label": user["label"],
            "memory_count": len(memories),
            "memories_by_status": {
                "active": sum(1 for m in memories if m.status == "active"),
                "conflicted": sum(1 for m in memories if m.status == "conflicted"),
                "expired": sum(1 for m in memories if m.status == "expired"),
                "superseded": sum(1 for m in memories if m.status == "superseded"),
            },
            "event_count": len(events),
            "recent_event_types": [e["event_type"] for e in events[-5:]],
        }
    return {"users": result, "provider": settings.llm_provider}
