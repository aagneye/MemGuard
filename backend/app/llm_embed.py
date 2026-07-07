"""Qwen embedding call for vector-based memory retrieval.

Uses the fixed model 'text-embedding-v3' (DashScope) as specified in the
architecture doc. Falls back to a zero-vector when the client is unavailable
so the service degrades gracefully without crashing.

The vector dimension for text-embedding-v3 is 1024 by default.
This module is a thin adapter that wraps the OpenAI-compatible embeddings API
exposed by DashScope.
"""
from __future__ import annotations

import math

EMBEDDING_DIM = 1024
_EMBEDDING_MODEL = "text-embedding-v3"


def _zero_vector(dim: int = EMBEDDING_DIM) -> list[float]:
    return [0.0] * dim


def embed_text(text: str) -> list[float]:
    """Return a 1024-dim embedding for text using Qwen text-embedding-v3.

    Returns a zero vector (graceful degradation) when the LLM client is
    unavailable, so callers can proceed with keyword-only matching.
    """
    from .llm import _client  # local import to avoid circular

    client = _client()
    if client is None:
        return _zero_vector()

    try:
        res = client.embeddings.create(model=_EMBEDDING_MODEL, input=text)
        return res.data[0].embedding
    except Exception:
        return _zero_vector()


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
