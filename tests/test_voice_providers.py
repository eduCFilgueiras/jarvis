import unittest
from unittest.mock import patch

from src.voice import OpenAISpeechToText, OpenAITextToSpeech


class OptionalVoiceProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_stt_reports_missing_configuration(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            response = await OpenAISpeechToText().transcribe(b"audio")
        self.assertIn("nao esta configurado", response)

    async def test_tts_reports_missing_configuration(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            response = await OpenAITextToSpeech().synthesize("ola")
        self.assertIn(b"nao esta configurado", response)
