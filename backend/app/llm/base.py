from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, user_message: str, memory_facts: list[str]) -> str:
        raise NotImplementedError

    @abstractmethod
    async def extract_facts(self, user_message: str) -> list[dict]:
        raise NotImplementedError
