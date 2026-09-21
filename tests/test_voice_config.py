import unittest
from unittest.mock import patch

from src.voice import VoiceConfig


class VoiceConfigTests(unittest.TestCase):
    def test_reads_voice_provider_configuration(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "JARVIS_VOICE_ENABLED": "true",
                "JARVIS_STT_PROVIDER": "mock-stt",
                "JARVIS_TTS_PROVIDER": "mock-tts",
            },
            clear=True,
        ):
            config = VoiceConfig()

        self.assertTrue(config.enabled)
        self.assertEqual(config.speech_to_text, "mock-stt")
        self.assertEqual(config.text_to_speech, "mock-tts")
