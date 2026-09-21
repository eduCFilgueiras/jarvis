from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from .providers import SpeechToText, TextToSpeech


@dataclass(frozen=True)
class VoiceResult:
    transcript: str
    response: str
    audio: bytes


class VoicePipeline:
    def __init__(
        self,
        speech_to_text: SpeechToText,
        text_to_speech: TextToSpeech,
        process_message: Callable[[str], Awaitable[str]],
    ) -> None:
        self._speech_to_text = speech_to_text
        self._text_to_speech = text_to_speech
        self._process_message = process_message

    async def process_audio(self, audio: bytes) -> VoiceResult:
        transcribe = getattr(self._speech_to_text, "transcribe", self._speech_to_text)
        synthesize = getattr(self._text_to_speech, "synthesize", self._text_to_speech)
        transcript = await transcribe(audio)
        response = await self._process_message(transcript)
        output = await synthesize(response)
        return VoiceResult(transcript, response, output)
