from .domain_types import SourceType, TrustTier

SOURCE_RULES: dict[SourceType, tuple[TrustTier, int]] = {
    "user_stated": ("high", 180),
    "tool_inferred": ("medium", 60),
    "document_extracted": ("low", 14),
}


def score_trust(source: SourceType, confidence: float = 1.0) -> tuple[TrustTier, int]:
    trust_tier, ttl_days = SOURCE_RULES[source]
    if confidence < 0.5 and trust_tier == "high":
        return "medium", ttl_days
    if confidence < 0.5 and trust_tier == "medium":
        return "low", ttl_days
    return trust_tier, ttl_days
