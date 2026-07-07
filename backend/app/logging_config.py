"""Structured JSON logging for MemGuard backend.

Configures Python's standard logging to output JSON so Alibaba Cloud log
collectors (SLS) can ingest structured fields without a custom parser.
"""
import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    numeric = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric)

    try:
        import json_log_formatter  # type: ignore[import-untyped]
        handler.setFormatter(json_log_formatter.JSONFormatter())
    except ImportError:
        # json_log_formatter is optional — fall back to plain text so the
        # server still starts without it.
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )

    root = logging.getLogger()
    root.setLevel(numeric)
    root.handlers.clear()
    root.addHandler(handler)


logger = logging.getLogger("memguard")
