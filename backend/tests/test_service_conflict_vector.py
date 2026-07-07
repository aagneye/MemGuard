"""Tests for the upgraded Stage 1 conflict detector.

The vector path is tested with a monkeypatched embed_text that returns
controlled vectors so we can test threshold behaviour without a live LLM.
"""
import pytest

from app.service_conflict import SIMILARITY_THRESHOLD, _keyword_conflict, _vector_conflict
from app.store import MemoryRecord


def _make_record(text: str) -> MemoryRecord:
    from datetime import datetime, timezone
    return MemoryRecord(
        id="test",
        user_id="u1",
        fact_text=text,
        trust_tier="high",
        source="user_stated",
        created_at=datetime.now(timezone.utc),
        last_confirmed_at=datetime.now(timezone.utc),
    )


class TestKeywordConflict:
    def test_plan_conflict(self):
        assert _keyword_conflict("I'm on the Pro plan", "I'm on the Enterprise plan") is True

    def test_plan_no_conflict_same(self):
        assert _keyword_conflict("I'm on the Pro plan", "I'm on the Pro plan") is False

    def test_timezone_conflict(self):
        assert _keyword_conflict("My timezone is IST", "My timezone is UTC") is True

    def test_unrelated_returns_false(self):
        assert _keyword_conflict("I like cats", "I prefer morning meetings") is False


class TestVectorConflict:
    def test_high_similarity_above_threshold_is_conflict(self, monkeypatch):
        monkeypatch.setattr("app.service_conflict.embed_text", lambda _: [1.0, 0.0])

        def mock_cosine(a, b):
            return SIMILARITY_THRESHOLD + 0.01

        monkeypatch.setattr("app.service_conflict.cosine_similarity", mock_cosine)
        assert _vector_conflict("Pro plan", "Enterprise plan") is True

    def test_low_similarity_below_threshold_is_not_conflict(self, monkeypatch):
        monkeypatch.setattr("app.service_conflict.embed_text", lambda _: [1.0, 0.0])

        def mock_cosine(a, b):
            return SIMILARITY_THRESHOLD - 0.1

        monkeypatch.setattr("app.service_conflict.cosine_similarity", mock_cosine)
        assert _vector_conflict("Pro plan", "I like cats") is False
