"""Simple in-memory rate limiter middleware.

Limits requests per IP per minute using a sliding window. Protects the
public demo endpoint from being hammered during the judging period.
Configurable via env vars; defaults are generous for a demo (60 req/min).
"""
import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int | None = None, window_seconds: int = 60) -> None:
        super().__init__(app)
        self.max_requests = max_requests or getattr(settings, "rate_limit_rpm", 60)
        self.window_seconds = window_seconds
        self._windows: dict[str, deque[float]] = defaultdict(deque)

    def _get_client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in ("/health", "/docs", "/openapi.json"):
            return await call_next(request)

        ip = self._get_client_ip(request)
        now = time.monotonic()
        window = self._windows[ip]

        while window and now - window[0] > self.window_seconds:
            window.popleft()

        if len(window) >= self.max_requests:
            return JSONResponse(
                {"detail": "Too many requests — please slow down."},
                status_code=429,
                headers={"Retry-After": str(self.window_seconds)},
            )

        window.append(now)
        return await call_next(request)
