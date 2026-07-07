"""Tests for service_session build_chat_history."""
import pytest

from app.service_session import MAX_SESSION_TURNS, build_chat_history
from app.repository_sessions import SessionRepository
from app.store import InMemoryStore


@pytest.fixture
def session_repo():
    return SessionRepository(InMemoryStore())


class TestBuildChatHistory:
    def test_includes_system_message_first(self, session_repo):
        messages = build_chat_history(session_repo, "s1", "u1", [], "Hello")
        assert messages[0]["role"] == "system"

    def test_system_includes_memory_facts(self, session_repo):
        messages = build_chat_history(session_repo, "s1", "u1", ["I'm on the Pro plan"], "Hello")
        system_content = messages[0]["content"]
        assert "Pro plan" in system_content

    def test_new_user_message_is_last(self, session_repo):
        messages = build_chat_history(session_repo, "s1", "u1", [], "What is my plan?")
        assert messages[-1]["role"] == "user"
        assert messages[-1]["content"] == "What is my plan?"

    def test_session_history_included(self, session_repo):
        session_repo.append_turn("s2", "user", "I told you my plan")
        session_repo.append_turn("s2", "assistant", "Yes, you are on Pro.")
        messages = build_chat_history(session_repo, "s2", "u1", [], "New message")
        roles = [m["role"] for m in messages]
        assert "assistant" in roles

    def test_truncates_to_max_turns(self, session_repo):
        for i in range(MAX_SESSION_TURNS + 5):
            session_repo.append_turn("s3", "user", f"Message {i}")
            session_repo.append_turn("s3", "assistant", f"Reply {i}")
        messages = build_chat_history(session_repo, "s3", "u1", [], "Final")
        history_messages = [m for m in messages if m["role"] != "system"]
        assert len(history_messages) <= MAX_SESSION_TURNS + 1
