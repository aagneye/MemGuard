from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .exception_handlers import register_exception_handlers
from .logging_config import configure_logging
from .mcp_server import mcp_app
from .middleware_logging import RequestLoggingMiddleware
from .middleware_ratelimit import RateLimitMiddleware
from .routes_auth import router as auth_router
from .routes_chat import router as chat_router
from .routes_demo import router as demo_router
from .routes_demo_state import router as demo_state_router
from .routes_events import router as events_router
from .routes_health import router as health_router
from .routes_memories import router as memories_router
from .routes_memories_search import router as memories_search_router
from .routes_session_new import router as session_new_router
from .routes_sessions import router as sessions_router
from .routes_teams import router as teams_router
from .routes_provenance import router as provenance_router
from .routes_similar import router as similar_router
from .routes_stats import router as stats_router
from .routes_trust_explain import router as trust_explain_router

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.3.0",
    description=(
        "MemGuard — Trust-Aware Memory Agent. "
        "Scores every memory for trust and provenance, catches conflicting or poisoned "
        "facts before acting on them, and forgets what's gone stale."
    ),
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    contact={"name": "MemGuard", "url": "https://github.com/aagneye/MemGuard"},
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)
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
app.include_router(demo_state_router)
app.include_router(chat_router)
app.include_router(memories_router)
app.include_router(memories_search_router)
app.include_router(events_router)
app.include_router(sessions_router)
app.include_router(session_new_router)
app.include_router(teams_router)
app.include_router(trust_explain_router)
app.include_router(provenance_router)
app.include_router(stats_router)
app.include_router(similar_router)

register_exception_handlers(app)

# MCP tool server mounted at /mcp — discoverable by Qwen Cloud agents
app.mount("/mcp", mcp_app)
