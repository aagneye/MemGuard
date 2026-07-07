"""Application startup tasks and shutdown cleanup.

Registered via FastAPI's lifespan context manager in main.py.
Logs configuration summary on startup so the ECS deployment logs
immediately show which LLM provider is active.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .config import settings
from .logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info(
        "MemGuard starting",
        extra={
            "version": "0.3.0",
            "provider": settings.llm_provider,
            "chat_model": settings.qwen_chat_model if settings.llm_provider == "qwen" else settings.ollama_model,
            "rate_limit_rpm": settings.rate_limit_rpm,
            "demo_time_scale": settings.demo_time_scale,
        },
    )
    yield
    logger.info("MemGuard shutting down")
