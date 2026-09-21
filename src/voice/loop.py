from .pipeline import VoiceResult
from .runtime import VoiceRuntime


class ContinuousVoiceLoop:
    def __init__(
        self,
        runtime: VoiceRuntime,
        stop_phrases: tuple[str, ...] = ("sair", "parar", "encerrar"),
    ) -> None:
        self._runtime = runtime
        self._stop_phrases = stop_phrases

    async def run(self, max_turns: int = 10) -> list[VoiceResult]:
        results: list[VoiceResult] = []
        for _ in range(max_turns):
            result = await self._runtime.run_once()
            results.append(result)
            if result.transcript.lower().strip() in self._stop_phrases:
                break
        return results
