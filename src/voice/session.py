import asyncio
from collections.abc import Awaitable, Callable
from enum import StrEnum

from .pipeline import VoiceResult
from .providers import SpeechToText, TextToSpeech


class VoiceState(StrEnum):
    IDLE = "idle"
    LISTENING = "listening"
    SPEAKING = "speaking"
    INTERRUPTED = "interrupted"


class VoiceSession:
    def __init__(
        self,
        speech_to_text: SpeechToText,
        text_to_speech: TextToSpeech,
        process_message: Callable[[str], Awaitable[str]],
    ) -> None:
        self._speech_to_text = speech_to_text
        self._text_to_speech = text_to_speech
        self._process_message = process_message
        self._state = VoiceState.IDLE
        self._speech_task: asyncio.Task[bytes] | None = None

    @property
    def state(self) -> VoiceState:
        return self._state

    async def handle_audio(self, audio: bytes) -> VoiceResult:
        self._state = VoiceState.LISTENING
        transcribe = getattr(self._speech_to_text, "transcribe", self._speech_to_text)
        synthesize = getattr(self._text_to_speech, "synthesize", self._text_to_speech)
        transcript = await transcribe(audio)
        return await self.handle_transcript(transcript, synthesize=synthesize)

    async def handle_transcript(self, transcript: str, synthesize=None) -> VoiceResult:
        if synthesize is None:
            synthesize = getattr(self._text_to_speech, "synthesize", self._text_to_speech)
        response = await self._process_message(transcript)
        self._state = VoiceState.SPEAKING
        output = await synthesize(response)
        self._state = VoiceState.IDLE
        return VoiceResult(transcript, response, output)

    def interrupt(self) -> None:
        if self._state == VoiceState.SPEAKING:
            self._state = VoiceState.INTERRUPTED
            if self._speech_task is not None:
                self._speech_task.cancel()
            self._speech_task = None

    def reset(self) -> None:
        self._state = VoiceState.IDLE
        self._speech_task = None
