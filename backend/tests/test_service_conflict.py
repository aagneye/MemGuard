from app.service_conflict import has_conflict
from app.store import MemoryRecord


def _memory(fact_text: str) -> MemoryRecord:
    return MemoryRecord(
        id="m1",
        user_id="u1",
        fact_text=fact_text,
        trust_tier="high",
        source="user_stated",
    )


def test_plan_conflict_detected() -> None:
    assert has_conflict(_memory("I am on Pro plan"), "I am on Enterprise plan")


def test_plan_duplicate_not_conflict() -> None:
    assert not has_conflict(_memory("I am on Pro plan"), "I am on Pro plan")
