from .domain_models import FactCandidate
from .repository_events import EventRepository
from .repository_memories import MemoryRepository
from .service_conflict import has_conflict
from .service_poison import is_sensitive_claim
from .service_trust import score_trust


class MemoryService:
    def __init__(self, memories: MemoryRepository, events: EventRepository) -> None:
        self.memories = memories
        self.events = events

    def process_candidate(self, user_id: str, candidate: FactCandidate) -> dict:
        active_memories = self.memories.active_for_user(user_id)
        trust_tier, ttl_days = score_trust(candidate.source_hint, candidate.confidence)
        existing_conflict = next((m for m in active_memories if has_conflict(m, candidate.fact)), None)

        if candidate.source_hint == "document_extracted" and is_sensitive_claim(candidate.fact):
            flagged = self.memories.create(
                user_id=user_id,
                fact_text=candidate.fact,
                trust_tier="low",
                source=candidate.source_hint,
                status="conflicted",
                ttl_days=ttl_days,
            )
            detail = {"memory_id": flagged.id, "reason": "possible_poisoning", "fact": candidate.fact}
            self.events.add(user_id, "flagged_poisoning", detail)
            return {"event_type": "flagged_poisoning", "detail": detail}

        if existing_conflict:
            incoming = self.memories.create(
                user_id=user_id,
                fact_text=candidate.fact,
                trust_tier=trust_tier,
                source=candidate.source_hint,
                status="conflicted",
                ttl_days=ttl_days,
            )
            self.memories.mark_conflicted([existing_conflict, incoming])
            detail = {"existing_id": existing_conflict.id, "incoming_id": incoming.id, "fact": candidate.fact}
            self.events.add(user_id, "conflict_detected", detail)
            return {"event_type": "conflict_detected", "detail": detail}

        saved = self.memories.create(
            user_id=user_id,
            fact_text=candidate.fact,
            trust_tier=trust_tier,
            source=candidate.source_hint,
            status="active",
            ttl_days=ttl_days,
        )
        detail = {"memory_id": saved.id, "trust_tier": trust_tier, "source": candidate.source_hint}
        self.events.add(user_id, "stored", detail)
        return {"event_type": "stored", "detail": detail}
