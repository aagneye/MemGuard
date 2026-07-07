from .store import MemoryRecord


def has_conflict(existing: MemoryRecord, new_fact: str) -> bool:
    existing_lower = existing.fact_text.lower()
    new_lower = new_fact.lower()

    plan_keys = ("plan", "pro", "enterprise")
    if any(k in existing_lower for k in plan_keys) and any(k in new_lower for k in plan_keys):
        return existing_lower != new_lower

    tz_keys = ("timezone", "ist", "utc", "pst")
    if any(k in existing_lower for k in tz_keys) and any(k in new_lower for k in tz_keys):
        return existing_lower != new_lower

    return False
