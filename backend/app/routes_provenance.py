"""Memory provenance endpoint — trace how a memory was created.

GET /memories/{id}/provenance

Returns the full event history for a memory, linking it back to the
original chat turn and any conflict/resolution events.
Useful for the demo to show the "supersede not overwrite" lifecycle on screen.
"""
from fastapi import APIRouter, HTTPException, Query

from .state import event_repo, memory_repo

router = APIRouter(tags=["memories"])


@router.get("/memories/{memory_id}/provenance")
def get_memory_provenance(memory_id: str) -> dict:
    """Return the provenance trace for a single memory."""
    record = memory_repo.get(memory_id)
    if not record:
        raise HTTPException(status_code=404, detail="Memory not found")

    related_events = [
        e for e in event_repo.recent(record.user_id, limit=200)
        if e.get("detail", {}).get("memory_id") == memory_id
        or e.get("detail", {}).get("incoming_id") == memory_id
        or e.get("detail", {}).get("existing_id") == memory_id
    ]

    superseded_by_record = None
    if record.superseded_by:
        sup = memory_repo.get(record.superseded_by)
        if sup:
            superseded_by_record = {
                "id": sup.id,
                "fact_text": sup.fact_text,
                "trust_tier": sup.trust_tier,
                "status": sup.status,
            }

    conflicting_record = None
    if record.conflicts_with:
        con = memory_repo.get(record.conflicts_with)
        if con:
            conflicting_record = {
                "id": con.id,
                "fact_text": con.fact_text,
                "trust_tier": con.trust_tier,
                "status": con.status,
            }

    return {
        "memory": {
            "id": record.id,
            "fact_text": record.fact_text,
            "trust_tier": record.trust_tier,
            "source": record.source,
            "status": record.status,
            "created_at": record.created_at.isoformat(),
        },
        "superseded_by": superseded_by_record,
        "conflicts_with": conflicting_record,
        "events": related_events,
    }
