import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path


class MemoryCategory(StrEnum):
    PREFERENCE = "preference"
    FACT = "fact"
    PROJECT = "project"


@dataclass(frozen=True)
class MemoryItem:
    category: MemoryCategory
    content: str


class PersistentMemory:
    def __init__(self, path: Path = Path("data/memory.json")) -> None:
        self._path = path
        self._items: list[MemoryItem] = self._load()

    def add(self, category: MemoryCategory, content: str) -> MemoryItem:
        item = MemoryItem(category, content.strip())
        if not item.content:
            raise ValueError("Memoria nao pode ser vazia.")
        self._items.append(item)
        self._save()
        return item

    def all(self, category: MemoryCategory | None = None) -> list[MemoryItem]:
        if category is None:
            return list(self._items)
        return [item for item in self._items if item.category == category]

    def search(self, query: str) -> list[MemoryItem]:
        normalized = query.lower().strip()
        return [item for item in self._items if normalized in item.content.lower()]

    def clear(self, category: MemoryCategory | None = None) -> None:
        if category is None:
            self._items.clear()
        else:
            self._items = [item for item in self._items if item.category != category]
        self._save()

    def _load(self) -> list[MemoryItem]:
        if not self._path.exists():
            return []
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            return []
        items: list[MemoryItem] = []
        for raw in payload:
            if not isinstance(raw, dict):
                continue
            try:
                category = MemoryCategory(raw.get("category"))
            except ValueError:
                continue
            content = raw.get("content")
            if isinstance(content, str) and content.strip():
                items.append(MemoryItem(category, content))
        return items

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps([asdict(item) for item in self._items], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
