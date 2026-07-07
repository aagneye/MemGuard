from .domain_models import FactCandidate
from .domain_types import SourceType


def detect_source(text: str) -> SourceType:
    lowered = text.lower()
    if "forwarded email" in lowered or "document" in lowered or "attached" in lowered:
        return "document_extracted"
    if "based on usage" in lowered or "seems like" in lowered:
        return "tool_inferred"
    return "user_stated"


def extract_candidates(message: str) -> list[FactCandidate]:
    lowered = message.lower().strip()
    source_hint = detect_source(message)
    keywords = ("plan", "timezone", "ist", "always reply", "concise", "refund", "admin access")
    if any(key in lowered for key in keywords):
        return [FactCandidate(fact=message.strip(), source_hint=source_hint, confidence=1.0)]
    return []
