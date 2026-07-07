"""Debug endpoint: explain why a fact would receive a given trust tier.

Useful during the demo to show the governance logic on screen.
GET /trust/explain?message=...&source=user_stated
"""
from fastapi import APIRouter, Query

from .domain_types import SourceType
from .service_trust import score_trust

router = APIRouter(tags=["governance"])


@router.get("/trust/explain")
def explain_trust(
    message: str = Query(..., description="The fact or message to score"),
    source: str = Query("user_stated", description="user_stated | tool_inferred | document_extracted"),
    confidence: float = Query(1.0, ge=0.0, le=1.0),
) -> dict:
    """Explain the trust tier that would be assigned to a given message."""
    valid_sources: set[SourceType] = {"user_stated", "tool_inferred", "document_extracted"}
    src: SourceType = source if source in valid_sources else "user_stated"  # type: ignore[assignment]
    trust_tier, ttl_days = score_trust(src, confidence)
    return {
        "input_message": message,
        "source": src,
        "confidence": confidence,
        "assigned_trust_tier": trust_tier,
        "ttl_days": ttl_days,
        "explanation": {
            "user_stated": "Direct user claims get HIGH trust — the user is asserting a fact about themselves.",
            "tool_inferred": "Tool or system inferences get MEDIUM trust — the system observed a pattern but did not confirm it.",
            "document_extracted": "Document-extracted claims get LOW trust — external documents can be poisoned.",
        }.get(src, "Unknown source"),
    }
