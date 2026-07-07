"""Tests for LLM conflict adjudication module."""
import pytest

from app.llm_adjudicate import _parse_relation, adjudicate_conflict


class TestParseRelation:
    def test_clean_json(self):
        assert _parse_relation('{"relation": "conflict"}') == "conflict"

    def test_embedded_in_prose(self):
        raw = 'Based on the comparison, {"relation": "duplicate"} is the result.'
        assert _parse_relation(raw) == "duplicate"

    def test_unknown_returns_unrelated(self):
        assert _parse_relation("I cannot determine.") == "unrelated"

    def test_invalid_value_is_returned_as_is(self):
        result = _parse_relation('{"relation": "agree"}')
        assert result == "agree"


class TestAdjudicateConflict:
    def test_returns_unrelated_when_no_client(self, monkeypatch):
        monkeypatch.setattr("app.llm_adjudicate._client", lambda: None)
        result = adjudicate_conflict("I'm on the Pro plan", "I'm on the Enterprise plan")
        assert result == "unrelated"
