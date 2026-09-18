import json
from pathlib import Path

from .conversation_history import ConversationHistory, ConversationMessage


class HistoryStorage:
    def __init__(self, path: Path) -> None:
        self._path = path

    def save(self, history: ConversationHistory) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {"role": message.role, "content": message.content}
            for message in history.all()
        ]
        self._path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self) -> list[ConversationMessage]:
        if not self._path.exists():
            return []

        payload = json.loads(self._path.read_text(encoding="utf-8"))
        messages: list[ConversationMessage] = []

        for item in payload:
            role = item.get("role")
            content = item.get("content")

            if role in {"user", "assistant"} and isinstance(content, str):
                messages.append(ConversationMessage(role=role, content=content))

        return messages
