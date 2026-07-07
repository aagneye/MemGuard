from app.store import InMemoryStore


def test_accepting_new_memory_expires_linked_old_memory() -> None:
    store = InMemoryStore()
    old = store.add(user_id="u1", fact_text="Pro plan", trust_tier="high", source="user_stated", status="conflicted")
    new = store.add(
        user_id="u1", fact_text="Enterprise plan", trust_tier="high", source="user_stated", status="conflicted"
    )
    store.link_conflict(old.id, new.id)

    resolved = store.resolve(new.id, "accept")

    assert resolved is not None
    assert resolved.status == "active"
    assert store.get(old.id).status == "expired"


def test_keeping_old_memory_reactivates_it_and_expires_new() -> None:
    store = InMemoryStore()
    old = store.add(user_id="u1", fact_text="Pro plan", trust_tier="high", source="user_stated", status="conflicted")
    new = store.add(
        user_id="u1", fact_text="Enterprise plan", trust_tier="high", source="user_stated", status="conflicted"
    )
    store.link_conflict(old.id, new.id)

    resolved = store.resolve(new.id, "reject")

    assert resolved is not None
    assert resolved.status == "expired"
    assert store.get(old.id).status == "active"
