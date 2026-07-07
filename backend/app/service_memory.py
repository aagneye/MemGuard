from .domain_models import FactCandidate
from .llm_adjudicate import adjudicate_conflict
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
        # Stage 1: heuristic keyword similarity scan (fast)
        candidate_conflicts = [m for m in active_memories if has_conflict(m, candidate.fact)]
        # Stage 2: LLM adjudication on each candidate (precise)
        existing_conflict = None
        for mem in candidate_conflicts:
            relation = adjudicate_conflict(mem.fact_text, candidate.fact)
            if relation == "conflict":
                existing_conflict = mem
                break
            if relation == "duplicate":
                # Duplicate — touch last_confirmed_at instead of inserting
                break
        # Fall back to heuristic result if LLM returned unrelated for all
        if existing_conflict is None and candidate_conflicts:
            # LLM said "unrelated" for everything but heuristic fired — trust heuristic
            existing_conflict = candidate_conflicts[0]

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
            return {
                "event_type": "flagged_poisoning",
                "type": "flagged",
                "fact": candidate.fact,
                "trust_tier": "low",
                "detail": detail,
            }

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
            self.memories.link_conflict(existing_conflict.id, incoming.id)
            detail = {"existing_id": existing_conflict.id, "incoming_id": incoming.id, "fact": candidate.fact}
            self.events.add(user_id, "conflict_detected", detail)
            return {
                "event_type": "conflict_detected",
                "type": "conflict",
                "fact": candidate.fact,
                "trust_tier": trust_tier,
                "detail": detail,
            }

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
        return {
            "event_type": "stored",
            "type": "stored",
            "fact": candidate.fact,
            "trust_tier": trust_tier,
            "detail": detail,
        }
