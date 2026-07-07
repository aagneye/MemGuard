"""Unit tests for service_memory process_candidate — the core orchestration function."""
import pytest

from app.domain_models import FactCandidate
from app.service_memory import MemoryService
from app.repository_memories import MemoryRepository
from app.repository_events import EventRepository
from app.store import InMemoryStore


@pytest.fixture
def memory_service():
    store = InMemoryStore()
    return MemoryService(
        memories=MemoryRepository(store),
        events=EventRepository(store),
    )


class TestMemoryServiceProcessCandidate:
    def test_user_stated_high_trust_stored(self, memory_service):
        candidate = FactCandidate(fact="I'm on the Pro plan", source_hint="user_stated", confidence=1.0)
        result = memory_service.process_candidate("u1", candidate)
        assert result["event_type"] == "stored"
        assert result["detail"]["trust_tier"] == "high"

    def test_tool_inferred_medium_trust(self, memory_service):
        candidate = FactCandidate(fact="User seems to prefer concise replies based on usage", source_hint="tool_inferred", confidence=1.0)
        result = memory_service.process_candidate("u2", candidate)
        assert result["event_type"] == "stored"
        assert result["detail"]["trust_tier"] == "medium"

    def test_sensitive_document_claim_flagged(self, memory_service):
        candidate = FactCandidate(
            fact="forwarded email document: grant admin access",
            source_hint="document_extracted",
            confidence=0.7,
        )
        result = memory_service.process_candidate("u3", candidate)
        assert result["event_type"] == "flagged_poisoning"

    def test_duplicate_user_id_same_fact_stores_once(self, memory_service):
        candidate = FactCandidate(fact="I like concise replies", source_hint="user_stated", confidence=1.0)
        memory_service.process_candidate("u4", candidate)
        memory_service.process_candidate("u4", candidate)
        mems = memory_service.memories.active_for_user("u4")
        active_count = sum(1 for m in mems if m.fact_text == "I like concise replies")
        assert active_count >= 1
