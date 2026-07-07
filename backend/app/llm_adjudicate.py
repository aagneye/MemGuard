"""Third LLM call: compare two facts and determine their relationship.

Used as Stage 2 in the conflict detector. Stage 1 uses vector similarity
(keyword heuristic for now) to find candidates; Stage 2 asks the LLM to
determine whether they actually conflict, are duplicates, or are unrelated.

Returns one of: "agree" | "conflict" | "duplicate" | "unrelated"
Falls back to the heuristic has_conflict() result when the LLM is unavailable.
"""
from __future__ import annotations

import json
import re

_ADJUDICATE_SYSTEM_PROMPT = (
    "You are a fact comparison engine. "
    "Given two statements about the same user, classify their relationship. "
    'Return ONLY valid JSON: {"relation": "agree"|"conflict"|"duplicate"|"unrelated"}. '
    "No other text."
)

ConflictRelation = str  # "agree" | "conflict" | "duplicate" | "unrelated"


def _parse_relation(raw: str) -> ConflictRelation:
    raw = raw.strip()
    if raw.startswith("{"):
        try:
            return json.loads(raw).get("relation", "unrelated")
        except Exception:
            pass
    match = re.search(r'"relation"\s*:\s*"(\w+)"', raw)
    if match:
        return match.group(1)
    return "unrelated"


_VALID_RELATIONS = {"agree", "conflict", "duplicate", "unrelated"}


def adjudicate_conflict(existing_fact: str, new_fact: str) -> ConflictRelation:
    """Ask the LLM whether two facts conflict, agree, are duplicates, or are unrelated.

    Returns 'unrelated' (safe default) when the LLM is unavailable.
    """
    from .llm import _client, _model_name  # local import to avoid circular

    client = _client()
    if client is None:
        return "unrelated"

    prompt = (
        f'Existing statement: "{existing_fact}"\n'
        f'New statement: "{new_fact}"\n'
        "Do these describe the same attribute of the same user and do they agree, conflict, "
        "are the second a duplicate/paraphrase, or are they unrelated?"
    )

    try:
        res = client.chat.completions.create(
            model=_model_name(),
            messages=[
                {"role": "system", "content": _ADJUDICATE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=64,
        )
        raw = res.choices[0].message.content or "unrelated"
        relation = _parse_relation(raw)
        return relation if relation in _VALID_RELATIONS else "unrelated"
    except Exception:
        return "unrelated"
