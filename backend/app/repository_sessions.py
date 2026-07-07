from collections import defaultdict


class SessionRepository:
    def __init__(self) -> None:
        self.turns: dict[str, list[dict]] = defaultdict(list)

    def append_turn(self, session_id: str, role: str, content: str) -> None:
        self.turns[session_id].append({"role": role, "content": content})

    def get_turns(self, session_id: str, limit: int = 12) -> list[dict]:
        return self.turns[session_id][-limit:]

    def clear(self, session_id: str) -> None:
        self.turns.pop(session_id, None)
