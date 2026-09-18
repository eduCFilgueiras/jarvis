import json
import re
from pathlib import Path
from typing import TypedDict


class TodoItem(TypedDict):
    text: str
    done: bool


class TodoTool:
    def __init__(self, path: Path = Path("data/todos.json")) -> None:
        self._path = path

    async def execute(self, message: str) -> str:
        input_text = message.lower().strip()

        if input_text.startswith("listar tarefas") or input_text.startswith("liste tarefas"):
            return self._list_todos()

        if input_text.startswith("limpar tarefas"):
            return self._clear_todos()

        if input_text.startswith("concluir tarefa"):
            return self._complete_todo(message)

        task = self._extract_task(message)
        return self._add_todo(task)

    def _extract_task(self, message: str) -> str:
        task = re.sub(
            r"^\s*(criar tarefa|crie uma tarefa|tarefa)\b",
            "",
            message,
            flags=re.I,
        )
        task = task.strip()

        if not task:
            raise ValueError("Nenhuma tarefa informada.")

        return task

    def _add_todo(self, task: str) -> str:
        todos = self._load_todos()
        todos.append({"text": task, "done": False})
        self._save_todos(todos)
        return f"Tarefa criada: {task}"

    def _list_todos(self) -> str:
        todos = self._load_todos()

        if not todos:
            return "Nenhuma tarefa salva."

        lines = ["Tarefas:"]

        for index, todo in enumerate(todos, start=1):
            status = "x" if todo["done"] else " "
            lines.append(f"{index}. [{status}] {todo['text']}")

        return "\n".join(lines)

    def _complete_todo(self, message: str) -> str:
        match = re.search(r"\d+", message)

        if match is None:
            raise ValueError("Informe o numero da tarefa.")

        index = int(match.group()) - 1
        todos = self._load_todos()

        if index < 0 or index >= len(todos):
            raise ValueError("Tarefa nao encontrada.")

        todos[index]["done"] = True
        self._save_todos(todos)
        return f"Tarefa concluida: {todos[index]['text']}"

    def _clear_todos(self) -> str:
        self._save_todos([])
        return "Tarefas apagadas."

    def _load_todos(self) -> list[TodoItem]:
        if not self._path.exists():
            return []

        payload = json.loads(self._path.read_text(encoding="utf-8"))

        if not isinstance(payload, list):
            return []

        todos: list[TodoItem] = []

        for item in payload:
            if (
                isinstance(item, dict)
                and isinstance(item.get("text"), str)
                and isinstance(item.get("done"), bool)
            ):
                todos.append({"text": item["text"], "done": item["done"]})

        return todos

    def _save_todos(self, todos: list[TodoItem]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(todos, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
