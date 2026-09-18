from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationMessage:
    role: str
    content: str


class ConversationHistory:
    def __init__(self) -> None:
        self._messages: list[ConversationMessage] = []

    def add_user_message(self, content: str) -> None:
        self._messages.append(ConversationMessage(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self._messages.append(ConversationMessage(role="assistant", content=content))

    def all(self) -> list[ConversationMessage]:
        return list(self._messages)

    def last(self, limit: int) -> list[ConversationMessage]:
        return self._messages[-limit:]

    def clear(self) -> None:
        self._messages.clear()

    def replace(self, messages: list[ConversationMessage]) -> None:
        self._messages = list(messages)
