from __future__ import annotations

from openai import OpenAI

from .config import settings


def _client() -> OpenAI | None:
    if settings.llm_provider == "qwen":
        api_key = settings.qwen_api_key or settings.dashscope_api_key
        base_url = settings.qwen_base_url or settings.dashscope_base_url
        if not api_key:
            return None
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key="ollama", base_url=settings.ollama_base_url)


def _model_name() -> str:
    return settings.qwen_chat_model if settings.llm_provider == "qwen" else settings.ollama_model


def chat_reply(message: str, memories: list[str]) -> str:
    mem_text = "\n".join(f"- {m}" for m in memories) if memories else "- none"
    prompt = (
        "You are MemGuard, a trust-aware customer support assistant.\n"
        "Use relevant memory facts, stay concise, and refuse unsafe entitlement changes unless confirmed.\n"
        f"Known memory facts:\n{mem_text}\n"
        f"User message: {message}"
    )
    client = _client()
    if client is None:
        return "I can help, but the Qwen API key is missing. Please set DASHSCOPE_API_KEY."
    try:
        res = client.chat.completions.create(
            model=_model_name(),
            messages=[
                {"role": "system", "content": "You are concise and safety-first."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return res.choices[0].message.content or "I could not generate a response."
    except Exception:
        return "I could not reach the model, but I saved your message to memory processing."
