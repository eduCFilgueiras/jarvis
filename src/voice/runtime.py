from collections.abc import Awaitable, Callable
import unicodedata
import io
import wave
from array import array

from .devices import AudioInput, AudioOutput
from .pipeline import VoiceResult
from .session import VoiceSession


class VoiceRuntime:
    def __init__(
        self,
        audio_input: AudioInput,
        audio_output: AudioOutput,
        process_message: Callable[[str], Awaitable[str]],
        stop_phrases: tuple[str, ...] = ("sair", "parar", "para", "pare", "encerra", "encerrar"),
    ) -> None:
        self._input = audio_input
        self._output = audio_output
        self._stop_phrases = {_normalize_phrase(item) for item in stop_phrases}
        self._session = VoiceSession(
            speech_to_text=self._transcribe,
            text_to_speech=self._synthesize,
            process_message=process_message,
        )

    async def run_once(self) -> VoiceResult:
        audio = await self._input.capture()
        transcribe = getattr(self._session._speech_to_text, "transcribe", self._session._speech_to_text)
        synthesize = getattr(self._session._text_to_speech, "synthesize", self._session._text_to_speech)
        if _is_silent_wav(audio):
            return VoiceResult("", "", b"")
        transcript = await transcribe(audio)
        if _normalize_phrase(transcript) in self._stop_phrases:
            response = "Entendido, parando por aqui."
            output = await synthesize(response)
            result = VoiceResult(transcript, response, output)
        else:
            result = await self._session.handle_transcript(transcript, synthesize=synthesize)
        await self._output.play(result.audio)
        return result

    async def _transcribe(self, audio: bytes) -> str:
        from .providers import OpenAISpeechToText

        return await OpenAISpeechToText().transcribe(audio)

    async def _synthesize(self, text: str) -> bytes:
        from .providers import OpenAITextToSpeech

        return await OpenAITextToSpeech().synthesize(text)


def _normalize_phrase(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.replace("jarvis", "").strip(" ,.!?")
    return " ".join(normalized.split())


def _is_silent_wav(audio: bytes, threshold: int = 250) -> bool:
    if audio[:4] != b"RIFF":
        return False
    try:
        with wave.open(io.BytesIO(audio), "rb") as wav:
            samples = array("h", wav.readframes(wav.getnframes()))
    except (wave.Error, EOFError):
        return False
    return not samples or max(abs(sample) for sample in samples) < threshold
