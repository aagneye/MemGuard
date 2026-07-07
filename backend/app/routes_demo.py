"""Demo helper routes — for the hackathon demo only.

These endpoints make it easy to reset and inspect demo state during the
live presentation without touching the database.
"""
from fastapi import APIRouter

from .demo_users import DEMO_USERS
from .schemas import DemoUser
from .state import event_repo, memory_repo

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/users", response_model=list[DemoUser])
def get_demo_users() -> list[DemoUser]:
    return DEMO_USERS


@router.post("/reset")
def reset_demo() -> dict:
    """Clear all memories and events for demo users so you can start fresh.

    Useful for re-running the demo without restarting the backend process.
    """
    cleared_users: list[str] = []
    for user in DEMO_USERS:
        user_id = user["id"]
        store = memory_repo._store
        user_memories = [m for m in store.memories.values() if m.user_id == user_id]
        for mem in user_memories:
            del store.memories[mem.id]
        store.events.pop(user_id, None)
        cleared_users.append(user_id)

    return {"ok": True, "cleared_users": cleared_users}
