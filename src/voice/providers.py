from collections.abc import Awaitable, Callable


class MockSpeechToText:
    async def transcribe(self, audio: bytes) -> str:
        return audio.decode("utf-8")


class MockTextToSpeech:
    async def synthesize(self, text: str) -> bytes:
        return text.encode("utf-8")


SpeechToText = Callable[[bytes], Awaitable[str]]
TextToSpeech = Callable[[str], Awaitable[bytes]]
