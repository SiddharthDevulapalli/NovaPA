import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", "20"))


class ConversationHistory:
    def __init__(self) -> None:
        self._messages: list[dict[str, Any]] = []

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})
        self._trim()

    def _trim(self) -> None:
        max_messages = MAX_HISTORY_TURNS * 2
        if len(self._messages) > max_messages:
            self._messages = self._messages[-max_messages:]

    def add_assistant(self, content: Any) -> None:
        self._messages.append({"role": "assistant", "content": content})

    def add_tool_result(self, tool_use_id: str, result: str) -> None:
        self._messages.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": tool_use_id, "content": result}],
        })

    def get(self) -> list[dict[str, Any]]:
        return self._messages

    def clear(self) -> None:
        self._messages = []
