from dataclasses import dataclass, field
import os


@dataclass
class VoiceConfig:
    enabled: bool = field(
        default_factory=lambda: os.environ.get("JARVIS_VOICE_ENABLED", "false").lower() == "true"
    )
    speech_to_text: str = field(
        default_factory=lambda: os.environ.get("JARVIS_STT_PROVIDER", "mock")
    )
    text_to_speech: str = field(
        default_factory=lambda: os.environ.get("JARVIS_TTS_PROVIDER", "mock")
    )
    language: str = field(default_factory=lambda: os.environ.get("JARVIS_VOICE_LANGUAGE", "pt-BR"))
