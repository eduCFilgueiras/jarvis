from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DevTaskPlan:
    task: str
    project_root: str
    files: tuple[str, ...]
    steps: tuple[str, ...]
    authorization_required: bool = True

    def render(self) -> str:
        files = ", ".join(self.files) if self.files else "nenhum arquivo identificado"
        steps = " ".join(f"{index}. {step}" for index, step in enumerate(self.steps, 1))
        return (
            f'[DEV] Tarefa: "{self.task}". '
            f"Contexto: {self.project_root}. Arquivos: {files}. "
            f"Plano: {steps} "
            "Autorizacao necessaria antes de qualquer escrita."
        )


class DevPlanner:
    def __init__(self, project_root: Path = Path("."), max_files: int = 12) -> None:
        self._project_root = project_root.resolve()
        self._max_files = max_files

    def create_plan(self, task: str) -> DevTaskPlan:
        files = tuple(
            str(path.relative_to(self._project_root))
            for path in sorted(self._project_root.rglob("*"))
            if path.is_file()
            and not any(
                part.startswith(".") or part == "__pycache__"
                for part in path.relative_to(self._project_root).parts
            )
        )[: self._max_files]
        return DevTaskPlan(
            task=task,
            project_root=str(self._project_root),
            files=files,
            steps=(
                "entender o pedido e as restricoes",
                "inspecionar os arquivos relevantes",
                "propor alteracoes pequenas e testaveis",
                "validar com testes e verificacoes",
                "aguardar autorizacao para executar escrita",
            ),
        )
