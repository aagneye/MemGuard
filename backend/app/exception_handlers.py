"""Standardized error response handlers for MemGuard API.

Returns consistent JSON error objects with a `detail` and `error_code`
field so the frontend can display human-readable messages.
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "The requested resource was not found.",
                "error_code": "NOT_FOUND",
                "path": str(request.url.path),
            },
        )

    @app.exception_handler(422)
    async def validation_error_handler(request: Request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Request validation failed — check your request body.",
                "error_code": "VALIDATION_ERROR",
                "errors": getattr(exc, "errors", lambda: [])() if hasattr(exc, "errors") else [],
            },
        )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc) -> JSONResponse:
        from .logging_config import logger
        logger.exception("Unhandled server error", extra={"path": str(request.url.path)})
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An internal error occurred. Please try again.",
                "error_code": "INTERNAL_ERROR",
            },
        )
