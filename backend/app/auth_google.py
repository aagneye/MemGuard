from __future__ import annotations

from typing import Any

from .config import settings


def verify_google_credential(credential: str) -> dict[str, Any]:
    """
    Verify a Google ID token. In local/dev, this gracefully falls back to
    a deterministic mock profile when GOOGLE_CLIENT_ID is not configured.
    """
    google_client_id = getattr(settings, "google_client_id", "")
    if not google_client_id:
        suffix = credential[-8:]
        return {
            "email": f"demo-{suffix}@example.com",
            "name": "Demo User",
            "picture": None,
            "sub": f"demo-{suffix}",
        }

    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token
    except Exception as exc:  # pragma: no cover - dependency issue
        raise RuntimeError("google-auth dependency is missing") from exc

    payload = id_token.verify_oauth2_token(credential, Request(), google_client_id)
    return {
        "email": payload.get("email", ""),
        "name": payload.get("name", "User"),
        "picture": payload.get("picture"),
        "sub": payload.get("sub", ""),
    }
