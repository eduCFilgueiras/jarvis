from .calculator_tool import CalculatorTool
from .contracts import ToolHandler, ToolRisk, ToolSpec
from .datetime_tool import DateTimeTool
from .files_tool import FilesTool
from .notes_tool import NotesTool
from .todo_tool import TodoTool

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(
        self,
        name: str,
        handler: ToolHandler,
        description: str = "",
        risk: ToolRisk = ToolRisk.LOW,
    ) -> None:
        self._tools[name] = ToolSpec(name, description, handler, risk)

    def get(self, name: str) -> ToolHandler | None:
        spec = self._tools.get(name)
        return spec.handler if spec is not None else None

    def spec(self, name: str) -> ToolSpec | None:
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
    registry.register("calculator", calculator_tool.execute, "Calcula expressoes matematicas.")
    registry.register("datetime", datetime_tool.execute, "Consulta data e hora.")
    registry.register("files", files_tool.execute, "Lista e le arquivos locais.", ToolRisk.MEDIUM)
    registry.register("notes", notes_tool.execute, "Cria, lista e remove notas.", ToolRisk.MEDIUM)
    registry.register("todo", todo_tool.execute, "Cria, lista e conclui tarefas.", ToolRisk.MEDIUM)
    return registry
