import re
from pathlib import Path


class FilesTool:
    def __init__(self, root: Path = Path("."), max_chars: int = 4000) -> None:
        self._root = root.resolve()
        self._max_chars = max_chars

    async def execute(self, message: str) -> str:
        input_text = message.lower().strip()

        if input_text.startswith("listar arquivos"):
            target = self._extract_optional_path(message, "listar arquivos")
            return self._list_files(target)

        if input_text.startswith("ler arquivo"):
            target = self._extract_required_path(message, "ler arquivo")
            return self._read_file(target)

        if input_text.startswith("escrever arquivo"):
            target, content = self._extract_write(message)
            return self._write_file(target, content)

        raise ValueError("Comando de arquivo nao reconhecido.")

    def _extract_write(self, message: str) -> tuple[Path, str]:
        raw = re.sub(r"^\s*escrever arquivo\b", "", message, flags=re.I).strip()
        if ":" not in raw:
            raise ValueError("Use 'escrever arquivo caminho: conteudo'.")
        path_text, content = raw.split(":", 1)
        if not path_text.strip() or not content.strip():
            raise ValueError("Informe caminho e conteudo.")
        return Path(path_text.strip()), content.lstrip()

    def _write_file(self, path: Path, content: str) -> str:
        target = self._resolve_safe_path(path)
        if target.exists() and target.is_dir():
            return "O caminho informado e um diretorio."
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Arquivo escrito: {path}"

    def _extract_optional_path(self, message: str, command: str) -> Path:
        raw_path = re.sub(rf"^\s*{re.escape(command)}\b", "", message, flags=re.I)
        raw_path = raw_path.strip()
        return Path(raw_path or ".")

    def _extract_required_path(self, message: str, command: str) -> Path:
        path = self._extract_optional_path(message, command)

        if str(path) == ".":
            raise ValueError("Informe o caminho do arquivo.")

        return path

    def _resolve_safe_path(self, path: Path) -> Path:
        resolved = (self._root / path).resolve()

        if resolved != self._root and self._root not in resolved.parents:
            raise ValueError("Caminho fora da area permitida.")

        return resolved

    def _list_files(self, path: Path) -> str:
        target = self._resolve_safe_path(path)

        if not target.exists():
            return "Caminho nao encontrado."

        if not target.is_dir():
            return "O caminho informado nao e um diretorio."

        entries = sorted(item.name for item in target.iterdir())

        if not entries:
            return "Diretorio vazio."

        return "Arquivos:\n" + "\n".join(entries)

    def _read_file(self, path: Path) -> str:
        target = self._resolve_safe_path(path)

        if not target.exists():
            return "Arquivo nao encontrado."

        if not target.is_file():
            return "O caminho informado nao e um arquivo."

        content = target.read_text(encoding="utf-8")

        if len(content) > self._max_chars:
            content = content[: self._max_chars] + "\n...[truncado]"

        return f"Conteudo de {path}:\n{content}"
