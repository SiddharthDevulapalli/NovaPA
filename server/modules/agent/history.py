from typing import Any


class ConversationHistory:
    def __init__(self) -> None:
        self._messages: list[dict[str, Any]] = []

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})

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
