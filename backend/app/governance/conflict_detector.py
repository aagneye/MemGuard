from collections.abc import Sequence

from app.db.models import Memory


def detect_simple_conflict(new_fact: str, existing_memories: Sequence[Memory]) -> Memory | None:
    """
    Base-level heuristic conflict detection for MVP:
    same topic keywords but different values (e.g., plan mentions).
    """
    new_lower = new_fact.lower()
    for memory in existing_memories:
        existing_lower = memory.fact_text.lower()
        if "plan" in new_lower and "plan" in existing_lower and new_lower != existing_lower:
            return memory
    return None
