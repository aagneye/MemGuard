"""Memory search endpoint — keyword + vector hybrid search.

GET /memories/search?user_id=...&q=...&top_k=5

Uses the same embedding model as the conflict detector (text-embedding-v3).
Falls back to keyword matching when the LLM is unavailable.
"""
from fastapi import APIRouter, Query

from .llm_embed import cosine_similarity, embed_text
from .schemas import MemoryItem
from .service_decay import days_remaining
from .state import memory_repo

router = APIRouter(tags=["memories"])


@router.get("/memories/search", response_model=list[MemoryItem])
def search_memories(
    user_id: str = Query(...),
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
) -> list[MemoryItem]:
    """Search a user's active memories by semantic similarity to a query."""
    memories = memory_repo.active_for_user(user_id)
    if not memories:
        return []

    query_embedding = embed_text(q)
    is_zero_vector = all(v == 0.0 for v in query_embedding)

    if is_zero_vector:
        q_lower = q.lower()
        scored = [
            (m, sum(word in m.fact_text.lower() for word in q_lower.split()))
            for m in memories
        ]
    else:
        scored = [
            (m, cosine_similarity(query_embedding, embed_text(m.fact_text)))
            for m in memories
        ]

    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_k]

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
        for m, _ in top
    ]
