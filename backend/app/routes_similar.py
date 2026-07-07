"""Find memories similar to a given memory by vector embedding.

GET /memories/{id}/similar?top_k=5

Uses text-embedding-v3 to find the nearest neighbours of a memory's fact text
in the user's memory store. Falls back to keyword search when LLM is unavailable.
"""
from fastapi import APIRouter, HTTPException, Query

from .llm_embed import cosine_similarity, embed_text
from .schemas import MemoryItem
from .service_decay import days_remaining
from .state import memory_repo

router = APIRouter(tags=["memories"])


@router.get("/memories/{memory_id}/similar", response_model=list[MemoryItem])
def get_similar_memories(
    memory_id: str,
    top_k: int = Query(5, ge=1, le=20),
) -> list[MemoryItem]:
    """Return memories most semantically similar to the given memory."""
    source_record = memory_repo.get(memory_id)
    if not source_record:
        raise HTTPException(status_code=404, detail="Memory not found")

    all_memories = memory_repo.active_for_user(source_record.user_id)
    candidates = [m for m in all_memories if m.id != memory_id]
    if not candidates:
        return []

    source_embedding = embed_text(source_record.fact_text)
    is_zero = all(v == 0.0 for v in source_embedding)

    if is_zero:
        query_lower = source_record.fact_text.lower()
        scored = [
            (m, sum(word in m.fact_text.lower() for word in query_lower.split()))
            for m in candidates
        ]
    else:
        scored = [
            (m, cosine_similarity(source_embedding, embed_text(m.fact_text)))
            for m in candidates
        ]

    scored.sort(key=lambda x: x[1], reverse=True)

    return [
        MemoryItem(
            id=m.id,
            user_id=m.user_id,
            fact_text=m.fact_text,
            trust_tier=m.trust_tier,
            source=m.source,
            status=m.status,
            ttl_days=m.ttl_days,
            superseded_by=m.superseded_by,
            conflicts_with=m.conflicts_with,
            created_at=m.created_at.isoformat(),
            days_remaining=days_remaining(m.last_confirmed_at, m.ttl_days),
        )
        for m, _ in scored[:top_k]
    ]
