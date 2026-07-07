from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes_auth import router as auth_router
from .routes_chat import router as chat_router
from .routes_demo import router as demo_router
from .routes_events import router as events_router
from .routes_health import router as health_router
from .routes_memories import router as memories_router
from .routes_session_new import router as session_new_router
from .routes_sessions import router as sessions_router
from .routes_teams import router as teams_router

app = FastAPI(title=settings.app_name, version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[item.strip() for item in settings.cors_origins.split(",") if item.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(demo_router)
app.include_router(chat_router)
app.include_router(memories_router)
app.include_router(events_router)
app.include_router(sessions_router)
app.include_router(session_new_router)
app.include_router(teams_router)
