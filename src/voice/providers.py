from collections.abc import Awaitable, Callable
import os


class MockSpeechToText:
    async def transcribe(self, audio: bytes) -> str:
        return audio.decode("utf-8")


class MockTextToSpeech:
    async def synthesize(self, text: str) -> bytes:
        return text.encode("utf-8")


class OpenAISpeechToText:
    def __init__(self, model: str = "gpt-4o-mini-transcribe") -> None:
        self._model = model

    async def transcribe(self, audio: bytes) -> str:
        if not os.environ.get("OPENAI_API_KEY"):
            return "OpenAI nao esta configurado para transcricao."
        try:
            from openai import AsyncOpenAI
        except ImportError:
            return "SDK da OpenAI nao esta instalado para transcricao."
        client = AsyncOpenAI()
        response = await client.audio.transcriptions.create(
            model=self._model,
            file=("audio.wav", audio),
        )
        return response.text


class OpenAITextToSpeech:
    def __init__(self, model: str = "gpt-4o-mini-tts", voice: str = "alloy") -> None:
        self._model = model
        self._voice = voice

    async def synthesize(self, text: str) -> bytes:
        if not os.environ.get("OPENAI_API_KEY"):
            return b"OpenAI nao esta configurado para sintese."
        try:
            from openai import AsyncOpenAI
        except ImportError:
            return b"SDK da OpenAI nao esta instalado para sintese."
        client = AsyncOpenAI()
        response = await client.audio.speech.create(
            model=self._model,
            voice=self._voice,
            input=text,
            response_format="wav",
        )
        return response.read()


SpeechToText = Callable[[bytes], Awaitable[str]]
TextToSpeech = Callable[[str], Awaitable[bytes]]
