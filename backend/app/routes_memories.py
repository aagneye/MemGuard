from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from .schemas import MemoryItem, ResolveRequest
from .service_decay import days_remaining
from .state import event_repo, memory_repo

router = APIRouter(tags=["memories"])


@router.get("/memories", response_model=list[MemoryItem])
def list_memories(user_id: str = Query(...), status: str | None = None) -> list[MemoryItem]:
    records = memory_repo.all_for_user(user_id)
    if status:
        records = [r for r in records if r.status == status]
    return [
        MemoryItem(
            id=r.id,
            user_id=r.user_id,
            fact_text=r.fact_text,
            trust_tier=r.trust_tier,
            source=r.source,
            status=r.status,
            ttl_days=r.ttl_days,
            superseded_by=r.superseded_by,
            conflicts_with=r.conflicts_with,
            created_at=r.created_at.isoformat(),
            days_remaining=days_remaining(r.last_confirmed_at, r.ttl_days),
        )
        for r in records
    ]


@router.get("/memories/{memory_id}", response_model=MemoryItem)
def get_memory(memory_id: str) -> MemoryItem:
    """Fetch a single memory by ID."""
    record = memory_repo.get(memory_id)
    if not record:
        raise HTTPException(status_code=404, detail="Memory not found")
    return MemoryItem(
        id=record.id,
        user_id=record.user_id,
        fact_text=record.fact_text,
        trust_tier=record.trust_tier,
        source=record.source,
        status=record.status,
        ttl_days=record.ttl_days,
        superseded_by=record.superseded_by,
        conflicts_with=record.conflicts_with,
        created_at=record.created_at.isoformat(),
        days_remaining=days_remaining(record.last_confirmed_at, record.ttl_days),
    )


@router.post("/memories/{memory_id}/touch")
def touch_memory(memory_id: str) -> dict:
    """Reset last_confirmed_at to now — defers TTL expiry. Useful for the decay demo beat."""
    record = memory_repo.get(memory_id)
    if not record:
        raise HTTPException(status_code=404, detail="Memory not found")
    record.last_confirmed_at = datetime.now(tz=timezone.utc)
    remaining = days_remaining(record.last_confirmed_at, record.ttl_days)
    event_repo.add(record.user_id, "touched", {"memory_id": memory_id})
    return {"ok": True, "memory_id": memory_id, "days_remaining": remaining}


@router.post("/memories/{memory_id}/resolve")
def resolve_memory(memory_id: str, body: ResolveRequest) -> dict:
    result = memory_repo.resolve(memory_id, body.action, body.supersede_fact_text)
    if result is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    event_repo.add(result.user_id, f"resolved_{body.action}", {"memory_id": result.id})
    return {"ok": True, "memory_id": result.id, "status": result.status}
