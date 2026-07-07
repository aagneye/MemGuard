"""Aggregate statistics endpoint.

GET /stats?user_id=... — per-user stats
GET /stats/global — global system-wide stats

Useful for the demo to show memory growth over the 5 beats,
and for judges who want to see the governance logic numerically.
"""
from fastapi import APIRouter, Query

from .demo_users import DEMO_USERS
from .state import event_repo, memory_repo

router = APIRouter(tags=["stats"])


@router.get("/stats")
def get_user_stats(user_id: str = Query(...)) -> dict:
    """Return aggregate memory and event statistics for a user."""
    memories = memory_repo.all_for_user(user_id)
    events = event_repo.recent(user_id, limit=1000)

    tier_counts = {"high": 0, "medium": 0, "low": 0}
    status_counts = {"active": 0, "conflicted": 0, "expired": 0, "superseded": 0}
    source_counts = {"user_stated": 0, "tool_inferred": 0, "document_extracted": 0}

    for m in memories:
        tier_counts[m.trust_tier] = tier_counts.get(m.trust_tier, 0) + 1
        status_counts[m.status] = status_counts.get(m.status, 0) + 1
        source_counts[m.source] = source_counts.get(m.source, 0) + 1

    event_type_counts: dict[str, int] = {}
    for e in events:
        et = e.get("event_type", "unknown")
        event_type_counts[et] = event_type_counts.get(et, 0) + 1

    return {
        "user_id": user_id,
        "total_memories": len(memories),
        "by_trust_tier": tier_counts,
        "by_status": status_counts,
        "by_source": source_counts,
        "total_events": len(events),
        "events_by_type": event_type_counts,
    }


@router.get("/stats/global")
def get_global_stats() -> dict:
    """Return system-wide aggregate stats across all demo users."""
    total_memories = 0
    total_events = 0
    users_with_memories: list[str] = []

    for user in DEMO_USERS:
        user_id = user["id"]
        memories = memory_repo.all_for_user(user_id)
        events = event_repo.recent(user_id, limit=1000)
        total_memories += len(memories)
        total_events += len(events)
        if memories:
            users_with_memories.append(user_id)

    return {
        "total_memories": total_memories,
        "total_events": total_events,
        "active_demo_users": len(users_with_memories),
        "demo_user_count": len(DEMO_USERS),
    }
