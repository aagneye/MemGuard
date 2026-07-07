from fastapi import FastAPI

from .config import settings
from .routes_chat import router as chat_router
from .routes_events import router as events_router
from .routes_health import router as health_router
from .routes_memories import router as memories_router
from .routes_sessions import router as sessions_router

app = FastAPI(title=settings.app_name, version="0.2.0")
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(memories_router)
app.include_router(events_router)
app.include_router(sessions_router)
