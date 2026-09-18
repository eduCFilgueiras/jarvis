from collections.abc import Awaitable, Callable

from .calculator_tool import CalculatorTool
from .datetime_tool import DateTimeTool
from .files_tool import FilesTool
from .notes_tool import NotesTool
from .todo_tool import TodoTool

ToolHandler = Callable[[str], Awaitable[str]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        self._tools[name] = handler

    def get(self, name: str) -> ToolHandler | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return sorted(self._tools)


def create_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    calculator_tool = CalculatorTool()
    datetime_tool = DateTimeTool()
    files_tool = FilesTool()
    notes_tool = NotesTool()
    todo_tool = TodoTool()
    registry.register("calculator", calculator_tool.execute)
    registry.register("datetime", datetime_tool.execute)
    registry.register("files", files_tool.execute)
    registry.register("notes", notes_tool.execute)
    registry.register("todo", todo_tool.execute)
    return registry
