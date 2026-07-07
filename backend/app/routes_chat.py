from fastapi import APIRouter

from .llm import chat_reply
from .llm_extract import extract_facts_via_llm
from .schemas import ChatRequest, ChatResponse, MemoryEvent
from .service_extract import extract_candidates
from .state import memory_repo, memory_service, session_repo

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    session_repo.append_turn(body.session_id, "user", body.message)
    active_memories = memory_repo.active_for_user(body.user_id)
    reply = chat_reply(body.message, [m.fact_text for m in active_memories])
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
