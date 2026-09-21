import unittest

from src.voice import MockAudioInput, MockAudioOutput, run_audio_turn


class AudioDeviceTests(unittest.IsolatedAsyncioTestCase):
    async def test_mock_audio_turn_captures_processes_and_plays(self) -> None:
        audio_input = MockAudioInput(b"input")
        audio_output = MockAudioOutput()

        async def process(audio: bytes) -> bytes:
            return audio.upper()

        result = await run_audio_turn(audio_input, audio_output, process)

        self.assertEqual(result, b"INPUT")
        self.assertEqual(audio_output.played, [b"INPUT"])
