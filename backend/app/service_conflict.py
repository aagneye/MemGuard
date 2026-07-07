"""Conflict detection — Stage 1 of the two-stage pipeline.

Stage 1 (this module): fast candidate selection using:
  a) keyword heuristic (no LLM cost, runs always)
  b) vector cosine similarity via Qwen text-embedding-v3 (when LLM available)
      A similarity score >= SIMILARITY_THRESHOLD marks a candidate.

Stage 2: see llm_adjudicate.py — the LLM decides the final relation type.
"""
from __future__ import annotations

from .store import MemoryRecord

SIMILARITY_THRESHOLD = 0.85


def _keyword_conflict(existing_text: str, new_text: str) -> bool:
    """Fast heuristic: same-domain keywords differ → candidate conflict."""
    e, n = existing_text.lower(), new_text.lower()
    for keys in (
        ("plan", "pro", "enterprise", "starter", "free"),
        ("timezone", "ist", "utc", "pst", "est", "gmt"),
        ("always reply", "response style", "concise", "verbose"),
        ("refund", "admin access"),
    ):
        in_existing = any(k in e for k in keys)
        in_new = any(k in n for k in keys)
        if in_existing and in_new and e != n:
            return True
    return False


def _vector_conflict(existing_text: str, new_text: str) -> bool:
    """Vector cosine similarity conflict check using cached Qwen embeddings.
    Returns False (not a candidate) when the embedding call is unavailable.
    """
    try:
        from .service_embed_cache import cached_cosine_similarity
        sim = cached_cosine_similarity(existing_text, new_text)
        return sim >= SIMILARITY_THRESHOLD and existing_text.lower() != new_text.lower()
    except Exception:
        return False


def has_conflict(existing: MemoryRecord, new_fact: str) -> bool:
    """Return True if the new fact is a conflict candidate for the existing memory.

    Uses keyword heuristic first. If it fires, returns immediately (cheap).
    If not, tries vector similarity (more expensive, requires LLM).
    """
    if _keyword_conflict(existing.fact_text, new_fact):
        return True
    return _vector_conflict(existing.fact_text, new_fact)
