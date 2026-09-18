from dataclasses import dataclass
from pathlib import Path

PROJECT_VERSION = "0.1.0"


@dataclass
class JarvisConfig:
    assistant_name: str = "Jarvis"
    version: str = PROJECT_VERSION
    language: str = "pt-BR"
    debug: bool = True
    timezone: str = "local"
    history_limit: int = 5
    history_path: Path = Path("data/history.json")
    export_path: Path = Path("data/session.md")
