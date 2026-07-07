from app.schemas import MemorySource, TrustTier

SOURCE_RULES: dict[MemorySource, tuple[TrustTier, int]] = {
    "user_stated": ("high", 180),
    "tool_inferred": ("medium", 60),
    "document_extracted": ("low", 14),
}


def score_trust(source: MemorySource, confidence: float = 1.0) -> tuple[TrustTier, int]:
    tier, ttl_days = SOURCE_RULES[source]
    if confidence < 0.5 and tier == "high":
        return "medium", ttl_days
    if confidence < 0.5 and tier == "medium":
        return "low", ttl_days
    return tier, ttl_days
