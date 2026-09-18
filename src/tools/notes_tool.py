import json
import re
from pathlib import Path


class NotesTool:
    def __init__(self, path: Path = Path("data/notes.json")) -> None:
        self._path = path

    async def execute(self, message: str) -> str:
        input_text = message.lower().strip()

        if input_text.startswith("listar notas") or input_text.startswith("liste notas"):
            return self._list_notes()

        if input_text.startswith("limpar notas"):
            return self._clear_notes()

        note = self._extract_note(message)
        return self._add_note(note)

    def _extract_note(self, message: str) -> str:
        note = re.sub(r"^\s*(anote|nota|crie uma nota)\b", "", message, flags=re.I)
        note = note.strip()

        if not note:
            raise ValueError("Nenhuma nota informada.")

        return note

    def _add_note(self, note: str) -> str:
        notes = self._load_notes()
        notes.append(note)
        self._save_notes(notes)
        return f"Nota salva: {note}"

    def _list_notes(self) -> str:
        notes = self._load_notes()

        if not notes:
            return "Nenhuma nota salva."

        lines = ["Notas salvas:"]
        lines.extend(f"{index}. {note}" for index, note in enumerate(notes, start=1))
        return "\n".join(lines)

    def _clear_notes(self) -> str:
        self._save_notes([])
        return "Notas apagadas."

    def _load_notes(self) -> list[str]:
        if not self._path.exists():
            return []

        payload = json.loads(self._path.read_text(encoding="utf-8"))

        if not isinstance(payload, list):
            return []

        return [item for item in payload if isinstance(item, str)]

    def _save_notes(self, notes: list[str]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(notes, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
