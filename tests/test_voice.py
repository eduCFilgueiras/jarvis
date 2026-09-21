import unittest

from src.voice import MockSpeechToText, MockTextToSpeech, VoicePipeline


class VoicePipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_mock_pipeline_round_trip(self) -> None:
        async def process(message: str) -> str:
            return f"resposta: {message}"

        pipeline = VoicePipeline(
            MockSpeechToText(), MockTextToSpeech(), process
        )

        result = await pipeline.process_audio(b"ola Jarvis")

        self.assertEqual(result.transcript, "ola Jarvis")
        self.assertEqual(result.response, "resposta: ola Jarvis")
        self.assertEqual(result.audio, b"resposta: ola Jarvis")
