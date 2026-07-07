from fastapi import APIRouter

from .llm import _client, _model_name
from .llm_extract import extract_facts_via_llm
from .schemas import ChatRequest, ChatResponse, MemoryEvent
from .service_extract import extract_candidates
from .service_session import build_chat_history
from .state import memory_repo, memory_service, session_repo

router = APIRouter(tags=["chat"])


def _chat_with_history(messages: list[dict]) -> str:
    """Send a full conversation history to the LLM and return the reply text."""
    client = _client()
    if client is None:
        return "I can help, but the LLM API key is missing. Please set QWEN_API_KEY or start Ollama."
    try:
        res = client.chat.completions.create(
            model=_model_name(),
            messages=messages,
            temperature=0.2,
        )
        return res.choices[0].message.content or "I could not generate a response."
    except Exception:
        return "I could not reach the model, but I saved your message to memory processing."


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    session_repo.append_turn(body.session_id, "user", body.message)
    active_memories = memory_repo.active_for_user(body.user_id)

    messages = build_chat_history(
        session_repo=session_repo,
        session_id=body.session_id,
        user_id=body.user_id,
        memory_facts=[m.fact_text for m in active_memories],
        new_user_message=body.message,
    )
    reply = _chat_with_history(messages)
    session_repo.append_turn(body.session_id, "assistant", reply)

    events: list[MemoryEvent] = []
    candidates = extract_facts_via_llm(body.message) or extract_candidates(body.message)
    for candidate in candidates:
        event = memory_service.process_candidate(body.user_id, candidate)
        events.append(
            MemoryEvent(
                event_type=event["event_type"],
                type=event["type"],
                fact=event["fact"],
                trust_tier=event.get("trust_tier"),
                detail=event["detail"],
            )
        )

    return ChatResponse(reply=reply, memory_events=events)
