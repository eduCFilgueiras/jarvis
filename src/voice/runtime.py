from collections.abc import Awaitable, Callable

from .devices import AudioInput, AudioOutput
from .pipeline import VoiceResult
from .session import VoiceSession


class VoiceRuntime:
    def __init__(
        self,
        audio_input: AudioInput,
        audio_output: AudioOutput,
        process_message: Callable[[str], Awaitable[str]],
    ) -> None:
        self._input = audio_input
        self._output = audio_output
        self._session = VoiceSession(
            speech_to_text=self._transcribe,
            text_to_speech=self._synthesize,
            process_message=process_message,
        )

    async def run_once(self) -> VoiceResult:
        audio = await self._input.capture()
        result = await self._session.handle_audio(audio)
        await self._output.play(result.audio)
        return result

    async def _transcribe(self, audio: bytes) -> str:
        from .providers import OpenAISpeechToText

        return await OpenAISpeechToText().transcribe(audio)

    async def _synthesize(self, text: str) -> bytes:
        from .providers import OpenAITextToSpeech

        return await OpenAITextToSpeech().synthesize(text)
