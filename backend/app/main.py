from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from .llm import chat_reply
from .schemas import ChatRequest, ChatResponse, MemoryEvent, MemoryItem, ResolveRequest
from .store import InMemoryStore, MemoryRecord

app = FastAPI(title="MemGuard API", version="0.1.0")
store = InMemoryStore()


def detect_source(text: str) -> str:
    lowered = text.lower()
    if "forwarded email" in lowered or "document" in lowered or "attached" in lowered:
        return "document_extracted"
    if "based on usage" in lowered or "seems like" in lowered:
        return "tool_inferred"
    return "user_stated"


def trust_for_source(source: str) -> tuple[str, int]:
    if source == "user_stated":
        return "high", 180
    if source == "tool_inferred":
        return "medium", 60
    return "low", 14


def extract_fact_candidate(message: str) -> str | None:
    lowered = message.lower()
    if "plan" in lowered:
        return message.strip()
    if "timezone" in lowered or "ist" in lowered:
        return message.strip()
    if "always reply" in lowered or "concise" in lowered:
        return message.strip()
    if "refund" in lowered or "admin access" in lowered:
        return message.strip()
    return None


def conflicts(existing: MemoryRecord, new_fact: str) -> bool:
    existing_lower = existing.fact_text.lower()
    new_lower = new_fact.lower()
    plan_keys = ("plan", "pro", "enterprise")
    if any(k in existing_lower for k in plan_keys) and any(k in new_lower for k in plan_keys):
        return existing_lower != new_lower
    tz_keys = ("timezone", "ist", "utc", "pst")
    if any(k in existing_lower for k in tz_keys) and any(k in new_lower for k in tz_keys):
        return existing_lower != new_lower
    return False


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    events: list[MemoryEvent] = []
    active_memories = store.list_active(body.user_id)
    reply = chat_reply(body.message, [m.fact_text for m in active_memories])

    candidate = extract_fact_candidate(body.message)
    if candidate:
        source = detect_source(body.message)
        trust, ttl_days = trust_for_source(source)
        existing_conflict = next((m for m in active_memories if conflicts(m, candidate)), None)

        if source == "document_extracted" and ("refund" in candidate.lower() or "admin access" in candidate.lower()):
            flagged = store.add(
                user_id=body.user_id,
                fact_text=candidate,
                trust_tier="low",
                source=source,
                status="conflicted",
                ttl_days=ttl_days,
            )
            detail = {"memory_id": flagged.id, "reason": "possible_poisoning", "fact": candidate}
            store.add_event(body.user_id, "flagged_poisoning", detail)
            events.append(MemoryEvent(event_type="flagged_poisoning", detail=detail))
        elif existing_conflict:
            incoming = store.add(
                user_id=body.user_id,
                fact_text=candidate,
                trust_tier=trust,
                source=source,
                status="conflicted",
                ttl_days=ttl_days,
            )
            store.mark_conflicted([existing_conflict, incoming])
            detail = {"existing_id": existing_conflict.id, "incoming_id": incoming.id, "fact": candidate}
            store.add_event(body.user_id, "conflict_detected", detail)
            events.append(MemoryEvent(event_type="conflict_detected", detail=detail))
        else:
            saved = store.add(
                user_id=body.user_id,
                fact_text=candidate,
                trust_tier=trust,
                source=source,
                status="active",
                ttl_days=ttl_days,
            )
            detail = {"memory_id": saved.id, "trust_tier": trust, "source": source}
            store.add_event(body.user_id, "stored", detail)
            events.append(MemoryEvent(event_type="stored", detail=detail))

    return ChatResponse(reply=reply, memory_events=events)


@app.get("/memories", response_model=list[MemoryItem])
def list_memories(user_id: str = Query(...), status: str | None = None) -> list[MemoryItem]:
    records = store.list_all(user_id)
    if status:
        records = [r for r in records if r.status == status]
    return [
        MemoryItem(
            id=r.id,
            user_id=r.user_id,
            fact_text=r.fact_text,
            trust_tier=r.trust_tier,
            source=r.source,
            status=r.status,
            ttl_days=r.ttl_days,
            superseded_by=r.superseded_by,
        )
        for r in records
    ]


@app.post("/memories/{memory_id}/resolve")
def resolve_memory(memory_id: str, body: ResolveRequest) -> dict:
    result = store.resolve(memory_id, body.action, body.supersede_fact_text)
    if result is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"ok": True, "memory_id": result.id, "status": result.status}
