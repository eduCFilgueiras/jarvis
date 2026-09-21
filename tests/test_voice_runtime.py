import unittest

from src.voice import MockAudioInput, MockAudioOutput, VoiceRuntime


class VoiceRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_runs_one_turn_with_mock_audio_devices(self) -> None:
        audio_output = MockAudioOutput()

        async def process(message: str) -> str:
            return f"resposta: {message}"

        runtime = VoiceRuntime(MockAudioInput(b"audio"), audio_output, process)

        # Runtime adapters are OpenAI-backed by design; replace them for this unit test.
        runtime._session._speech_to_text = lambda audio: _text(audio)
        runtime._session._text_to_speech = lambda text: _audio(text)
        result = await runtime.run_once()

        self.assertEqual(result.response, "resposta: audio")
        self.assertEqual(audio_output.played, [b"resposta: audio"])


async def _text(audio: bytes) -> str:
    return audio.decode()


async def _audio(text: str) -> bytes:
    return text.encode()
