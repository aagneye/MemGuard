"""Session context service — builds the LLM message history for a chat turn.

Retrieves recent turns from the session repository and formats them as an
OpenAI-compatible messages list. The memory facts are injected as a system
message prefix so the LLM can use them in its reply.
"""
from __future__ import annotations

from .repository_sessions import SessionRepository

MAX_SESSION_TURNS = 10


def build_chat_history(
    session_repo: SessionRepository,
    session_id: str,
    user_id: str,
    memory_facts: list[str],
    new_user_message: str,
) -> list[dict]:
    """Build a full OpenAI messages list for the current chat turn.

    Format:
      system: MemGuard identity + memory facts
      [assistant/user turns from session history, last MAX_SESSION_TURNS]
      user: new_user_message
    """
    mem_text = "\n".join(f"- {fact}" for fact in memory_facts) if memory_facts else "- (no memories yet)"
    system_content = (
        "You are MemGuard, a trust-aware customer support assistant.\n"
        "Use the memory facts below to personalise your response. "
        "Stay concise and refuse to act on admin-level or account-mutation requests "
        "unless they come from a high-trust user_stated source.\n\n"
        f"Known memory facts for this user:\n{mem_text}"
    )
    messages: list[dict] = [{"role": "system", "content": system_content}]

    recent_turns = session_repo.get(session_id)[-MAX_SESSION_TURNS:]
    for turn in recent_turns:
        messages.append({"role": turn.role, "content": turn.content})

    messages.append({"role": "user", "content": new_user_message})
    return messages
