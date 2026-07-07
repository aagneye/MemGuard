"""Batch operations on memories.

POST /memories/batch-touch — reset TTL for multiple memories at once
POST /memories/batch-expire — manually expire a list of memories

Useful for the demo to show bulk lifecycle operations and for admin tooling.
"""
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from .state import event_repo, memory_repo

router = APIRouter(tags=["memories"])


class BatchIdRequest(BaseModel):
    memory_ids: list[str]
    user_id: str


@router.post("/memories/batch-touch")
def batch_touch_memories(body: BatchIdRequest) -> dict:
    """Reset last_confirmed_at for a list of memory IDs, deferring their TTL."""
    updated = []
    now = datetime.now(tz=timezone.utc)
    for mem_id in body.memory_ids:
        record = memory_repo.get(mem_id)
        if record and record.user_id == body.user_id:
            record.last_confirmed_at = now
            updated.append(mem_id)
    event_repo.add(body.user_id, "bulk_touched", {"memory_ids": updated, "count": len(updated)})
    return {"ok": True, "updated_count": len(updated), "updated_ids": updated}


@router.post("/memories/batch-expire")
def batch_expire_memories(body: BatchIdRequest) -> dict:
    """Immediately expire a list of memories (for admin/demo use)."""
    expired = []
    for mem_id in body.memory_ids:
        record = memory_repo.get(mem_id)
        if record and record.user_id == body.user_id and record.status == "active":
            record.status = "expired"
            expired.append(mem_id)
    event_repo.add(body.user_id, "bulk_expired", {"memory_ids": expired, "count": len(expired)})
    return {"ok": True, "expired_count": len(expired), "expired_ids": expired}
