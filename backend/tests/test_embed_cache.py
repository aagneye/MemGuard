"""Tests for the embedding LRU cache."""
import pytest

from app.service_embed_cache import cached_embed, clear_cache


class TestEmbedCache:
    def test_cache_returns_tuple(self, monkeypatch):
        monkeypatch.setattr("app.service_embed_cache.embed_text", lambda _: [1.0, 0.0])
        clear_cache()
        result = cached_embed("test text")
        assert isinstance(result, tuple)
        assert result == (1.0, 0.0)

    def test_cache_hit_returns_same_object(self, monkeypatch):
        call_count = {"n": 0}

        def counting_embed(text: str) -> list[float]:
            call_count["n"] += 1
            return [float(call_count["n"])]

        monkeypatch.setattr("app.service_embed_cache.embed_text", counting_embed)
        clear_cache()

        first = cached_embed("same text")
        second = cached_embed("same text")

        assert call_count["n"] == 1
        assert first == second

    def test_different_texts_call_embed_twice(self, monkeypatch):
        call_count = {"n": 0}

        def counting_embed(text: str) -> list[float]:
            call_count["n"] += 1
            return [0.0]

        monkeypatch.setattr("app.service_embed_cache.embed_text", counting_embed)
        clear_cache()

        cached_embed("text one")
        cached_embed("text two")

        assert call_count["n"] == 2

    def test_clear_cache_forces_recompute(self, monkeypatch):
        call_count = {"n": 0}

        def counting_embed(text: str) -> list[float]:
            call_count["n"] += 1
            return [0.0]

        monkeypatch.setattr("app.service_embed_cache.embed_text", counting_embed)
        clear_cache()

        cached_embed("cached text")
        clear_cache()
        cached_embed("cached text")

        assert call_count["n"] == 2
