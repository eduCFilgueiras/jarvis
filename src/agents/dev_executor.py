from dataclasses import dataclass

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
