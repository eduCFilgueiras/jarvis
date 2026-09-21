import unittest

from src.voice import ContinuousVoiceLoop
from src.voice.pipeline import VoiceResult


class FakeRuntime:
    def __init__(self) -> None:
        self.transcripts = iter(["ola", "parar", "nao deveria executar"])

    async def run_once(self) -> VoiceResult:
        transcript = next(self.transcripts)
        return VoiceResult(transcript, f"resposta {transcript}", b"")


class ContinuousVoiceLoopTests(unittest.IsolatedAsyncioTestCase):
    async def test_stops_on_stop_phrase(self) -> None:
        results = await ContinuousVoiceLoop(FakeRuntime()).run(max_turns=10)

        self.assertEqual([result.transcript for result in results], ["ola", "parar"])

    async def test_respects_max_turns(self) -> None:
        results = await ContinuousVoiceLoop(FakeRuntime()).run(max_turns=1)

        self.assertEqual(len(results), 1)

    async def test_accepts_accented_stop_transcription(self) -> None:
        runtime = FakeRuntime()
        runtime.transcripts = iter(["Jarvis Pará"])

        results = await ContinuousVoiceLoop(runtime).run()

        self.assertEqual(len(results), 1)
