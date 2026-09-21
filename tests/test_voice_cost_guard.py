import unittest
import wave
from io import BytesIO
from array import array

from src.voice.runtime import _is_silent_wav


class VoiceCostGuardTests(unittest.TestCase):
    def test_detects_silent_wav(self) -> None:
        buffer = BytesIO()
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(array("h", [0] * 160).tobytes())

        self.assertTrue(_is_silent_wav(buffer.getvalue()))
