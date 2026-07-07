from fastapi import APIRouter

from .demo_users import DEMO_USERS
from .schemas import DemoUser

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/users", response_model=list[DemoUser])
def list_demo_users() -> list[DemoUser]:
    return [DemoUser(**user) for user in DEMO_USERS]
