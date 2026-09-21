import unittest

from src.voice import MacAudioInput, MacAudioOutput


class MacAudioAdapterTests(unittest.TestCase):
    def test_adapters_are_configurable(self) -> None:
        self.assertEqual(MacAudioInput(8000, 2, 3).sample_rate, 8000)
        self.assertEqual(MacAudioOutput(22050, 2).channels, 2)
