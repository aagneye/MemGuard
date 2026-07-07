"""Simple in-process LRU cache for text embeddings.

Avoids re-embedding the same fact text on every conflict check call.
The cache is bounded by MAX_CACHE_SIZE entries (LRU eviction) to prevent
unbounded memory growth in long-running processes.

This is important because the two-stage conflict detector calls embed_text()
on every active memory for each new fact — without caching, a user with
100 memories would make 100 embedding API calls per message.
"""
from __future__ import annotations

from functools import lru_cache

MAX_CACHE_SIZE = 512


@lru_cache(maxsize=MAX_CACHE_SIZE)
def cached_embed(text: str) -> tuple[float, ...]:
    """Cache-aware wrapper around embed_text that returns a hashable tuple."""
    from .llm_embed import embed_text
    return tuple(embed_text(text))


def cached_cosine_similarity(text_a: str, text_b: str) -> float:
    """Cosine similarity between two texts using cached embeddings."""
    from .llm_embed import cosine_similarity
    vec_a = list(cached_embed(text_a))
    vec_b = list(cached_embed(text_b))
    return cosine_similarity(vec_a, vec_b)


def clear_cache() -> None:
    """Clear the embedding cache — useful in tests and after bulk memory changes."""
    cached_embed.cache_clear()
