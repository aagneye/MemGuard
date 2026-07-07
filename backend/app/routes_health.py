import platform
import sys

from fastapi import APIRouter

from .config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "version": "0.3.0",
        "provider": settings.llm_provider,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
    }
