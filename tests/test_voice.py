import unittest

from src.voice import MockSpeechToText, MockTextToSpeech, VoicePipeline, VoiceSession, VoiceState


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

    async def test_voice_session_returns_to_idle_after_response(self) -> None:
        async def process(message: str) -> str:
            return f"resposta: {message}"

        session = VoiceSession(MockSpeechToText(), MockTextToSpeech(), process)

        result = await session.handle_audio(b"ola")

        self.assertEqual(result.response, "resposta: ola")
        self.assertEqual(session.state, VoiceState.IDLE)

    async def test_interrupt_marks_speaking_session(self) -> None:
        async def process(message: str) -> str:
            return message

        session = VoiceSession(MockSpeechToText(), MockTextToSpeech(), process)
        session._state = VoiceState.SPEAKING

        session.interrupt()

        self.assertEqual(session.state, VoiceState.INTERRUPTED)
