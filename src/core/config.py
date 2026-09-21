from dataclasses import dataclass, field
import os
from pathlib import Path

from src.voice import VoiceConfig

PROJECT_VERSION = "0.1.0"


@dataclass
class JarvisConfig:
    assistant_name: str = "Jarvis"
    version: str = PROJECT_VERSION
    environment: str = field(default_factory=lambda: os.environ.get("JARVIS_ENV", "local"))
    language: str = field(default_factory=lambda: os.environ.get("JARVIS_LANGUAGE", "pt-BR"))
    debug: bool = field(
        default_factory=lambda: os.environ.get("JARVIS_DEBUG", "true").lower() == "true"
    )
    timezone: str = field(default_factory=lambda: os.environ.get("JARVIS_TIMEZONE", "local"))
    history_limit: int = field(
        default_factory=lambda: int(os.environ.get("JARVIS_HISTORY_LIMIT", "5"))
    )
    history_path: Path = field(
        default_factory=lambda: Path(
            os.environ.get("JARVIS_HISTORY_PATH", "data/history.json")
        )
    )
    export_path: Path = field(
        default_factory=lambda: Path(
            os.environ.get("JARVIS_EXPORT_PATH", "data/session.md")
        )
    )
    voice: VoiceConfig = field(default_factory=VoiceConfig)
