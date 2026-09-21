from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from src.security import PermissionPolicy, PermissionRequest
from src.tools import FilesTool

from .dev_planner import DevTaskPlan


@dataclass(frozen=True)
class ExecutionPreview:
    task: str
    operations: tuple[str, ...]
    dry_run: bool = True

    def render(self) -> str:
        operations = " ".join(
            f"{index}. {operation}" for index, operation in enumerate(self.operations, 1)
        )
        return (
            f'[DEV] Execucao simulada para "{self.task}": {operations} '
            "Nenhum arquivo ou comando foi alterado."
        )


class AllowedOperation(StrEnum):
    INSPECT = "inspect"
    TEST = "test"
    REPORT = "report"


class DevExecutionGuard:
    """Validates safe DEV operations; it never invokes a shell command."""

    def __init__(self, project_root: Path = Path(".")) -> None:
        self._project_root = project_root.resolve()

    def validate(self, operation: AllowedOperation, path: Path | None = None) -> bool:
        if operation not in set(AllowedOperation):
            return False
        if path is None:
            return True
        resolved = (self._project_root / path).resolve()
        return resolved == self._project_root or self._project_root in resolved.parents

    def execute(self, operation: AllowedOperation, path: Path | None = None) -> str:
        if not self.validate(operation, path):
            return "Operacao bloqueada pela politica de execucao DEV."
        return f"Operacao {operation.value} validada; execucao externa desabilitada."

    async def write_file(
        self,
        path: Path,
        content: str,
        permissions: PermissionPolicy,
    ) -> str:
        if not self.validate(AllowedOperation.INSPECT, path):
            return "Operacao bloqueada pela politica de execucao DEV."
        request = PermissionRequest("dev", "write", str(path))
        decision = permissions.check(request)
        if not decision.allowed:
            return f"Permissao pendente: {decision.reason}"
        return await FilesTool(self._project_root).execute(
            f"escrever arquivo {path}: {content}"
        )


class DevExecutor:
    """Prepares an execution preview without performing side effects."""

    def prepare(self, plan: DevTaskPlan) -> ExecutionPreview:
        return ExecutionPreview(
            task=plan.task,
            operations=(
                "revisar os arquivos identificados",
                "aplicar alteracoes somente apos nova confirmacao",
                "executar testes direcionados",
                "reportar o resultado e os arquivos modificados",
            ),
        )
