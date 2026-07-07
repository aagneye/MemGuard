"""Memory decay service — check-on-read TTL expiry with demo time scaling.

The DEMO_TIME_SCALE env var (default 1.0) multiplies elapsed time so that
a memory set to ttl_days=7 expires in 7/DEMO_TIME_SCALE real days.

Setting DEMO_TIME_SCALE=1440 makes 1 real minute feel like 1 day —
useful for a live demo where you want to show expiry in real time.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .config import settings


def _demo_elapsed_days(since: datetime) -> float:
    """Return elapsed days scaled by DEMO_TIME_SCALE."""
    real_elapsed = (datetime.now(tz=timezone.utc) - since).total_seconds() / 86400.0
    return real_elapsed * settings.demo_time_scale


def is_expired(last_confirmed_at: datetime, ttl_days: int | None) -> bool:
    """Return True if the memory should be expired based on TTL and time scale."""
    if ttl_days is None:
        return False
    return _demo_elapsed_days(last_confirmed_at) >= ttl_days


def days_remaining(last_confirmed_at: datetime, ttl_days: int | None) -> float | None:
    """Return approximate real-time days remaining, or None if no TTL."""
    if ttl_days is None:
        return None
    elapsed = _demo_elapsed_days(last_confirmed_at)
    remaining = ttl_days - elapsed
    return max(0.0, remaining)
