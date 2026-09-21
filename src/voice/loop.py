from .pipeline import VoiceResult
from .runtime import VoiceRuntime, _normalize_phrase


class ContinuousVoiceLoop:
    def __init__(
        self,
        runtime: VoiceRuntime,
        stop_phrases: tuple[str, ...] = ("sair", "parar", "para", "pare", "encerrar"),
    ) -> None:
        self._runtime = runtime
        self._stop_phrases = {_normalize_phrase(item) for item in stop_phrases}

    async def run(self, max_turns: int = 10) -> list[VoiceResult]:
        results: list[VoiceResult] = []
        for _ in range(max_turns):
            result = await self._runtime.run_once()
            results.append(result)
            if _normalize_phrase(result.transcript) in self._stop_phrases:
                break
        return results
