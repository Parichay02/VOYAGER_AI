from typing import Dict, List


class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, List[dict]] = {}

    def get_history(self, session_id: str) -> List[dict]:
        return self._sessions.get(session_id, [])

    def add_turn(self, session_id: str, role: str, content: str):
        self._sessions.setdefault(session_id, []).append({"role": role, "content": content})

    def clear(self, session_id: str):
        self._sessions.pop(session_id, None)


session_store = SessionStore()