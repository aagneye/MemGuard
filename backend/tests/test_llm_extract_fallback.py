"""Tests for LLM extraction module with fallback behavior.

When the LLM client is unavailable (no API key), extract_facts_via_llm
must return None cleanly so the caller can switch to heuristic extraction.
"""
import pytest

from app.llm_extract import _parse_json_candidates, _validate_source, extract_facts_via_llm


class TestParseJsonCandidates:
    def test_clean_array(self):
        raw = '[{"fact": "On Pro plan", "source_hint": "user_stated", "confidence": 0.9}]'
        result = _parse_json_candidates(raw)
        assert len(result) == 1
        assert result[0]["fact"] == "On Pro plan"

    def test_array_embedded_in_prose(self):
        raw = 'Here are the facts: [{"fact": "IST timezone", "source_hint": "user_stated", "confidence": 1.0}] done.'
        result = _parse_json_candidates(raw)
        assert len(result) == 1

    def test_empty_array_string(self):
        assert _parse_json_candidates("[]") == []

    def test_no_array_returns_empty(self):
        assert _parse_json_candidates("No facts here.") == []


class TestValidateSource:
    def test_valid_sources(self):
        for src in ("user_stated", "tool_inferred", "document_extracted"):
            assert _validate_source(src) == src

    def test_invalid_source_defaults_to_user_stated(self):
        assert _validate_source("unknown_source") == "user_stated"


class TestExtractFactsViaLlm:
    def test_returns_none_when_no_client(self, monkeypatch):
        monkeypatch.setattr("app.llm_extract._client", lambda: None)
        assert extract_facts_via_llm("any message") is None
