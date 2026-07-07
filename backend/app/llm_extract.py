"""Second LLM call: structured fact extraction from a user turn.

Returns a list of FactCandidate objects. Uses a strict JSON-only system
prompt as specified in the build spec. Falls back to the heuristic extractor
(service_extract.py) if the LLM is unavailable or returns unparseable output.
"""
from __future__ import annotations

import json
import re

from .domain_models import FactCandidate
from .domain_types import SourceType


_EXTRACT_SYSTEM_PROMPT = (
    "Extract any new factual claims about the user from this message. "
    "Return ONLY a JSON array of objects: [{\"fact\": \"...\", \"source_hint\": \"user_stated|tool_inferred|document_extracted\", \"confidence\": 0.0-1.0}]. "
    "If none, return []. Do not include any other text."
)


def _parse_json_candidates(raw: str) -> list[dict]:
    """Parse JSON array from raw LLM output defensively.
    LLMs sometimes wrap the array in prose; this extracts the first [...] block."""
    raw = raw.strip()
    if raw.startswith("["):
        return json.loads(raw)
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []


def _validate_source(raw: str) -> SourceType:
    valid: set[SourceType] = {"user_stated", "tool_inferred", "document_extracted"}
    return raw if raw in valid else "user_stated"  # type: ignore[return-value]


def extract_facts_via_llm(message: str) -> list[FactCandidate] | None:
    """Call the LLM for structured fact extraction.

    Returns None when the LLM client is unavailable so the caller can fall
    back to the heuristic extractor without crashing the chat turn.
    """
    from .llm import _client, _model_name  # local import to avoid circular

    client = _client()
    if client is None:
        return None

    try:
        res = client.chat.completions.create(
            model=_model_name(),
            messages=[
                {"role": "system", "content": _EXTRACT_SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.0,
            max_tokens=512,
        )
        raw = res.choices[0].message.content or "[]"
        items = _parse_json_candidates(raw)
        return [
            FactCandidate(
                fact=str(item.get("fact", "")).strip(),
                source_hint=_validate_source(str(item.get("source_hint", "user_stated"))),
                confidence=float(item.get("confidence", 1.0)),
            )
            for item in items
            if item.get("fact")
        ]
    except Exception:
        return None
