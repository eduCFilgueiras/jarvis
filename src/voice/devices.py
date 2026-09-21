from collections.abc import Awaitable, Callable
from typing import Protocol


class AudioInput(Protocol):
    async def capture(self) -> bytes: ...


class AudioOutput(Protocol):
    async def play(self, audio: bytes) -> None: ...


class MockAudioInput:
    def __init__(self, audio: bytes = b"") -> None:
        self.audio = audio

    async def capture(self) -> bytes:
        return self.audio


class MockAudioOutput:
    def __init__(self) -> None:
        self.played: list[bytes] = []

    async def play(self, audio: bytes) -> None:
        self.played.append(audio)


async def run_audio_turn(
    audio_input: AudioInput,
    audio_output: AudioOutput,
    process_audio: Callable[[bytes], Awaitable[bytes]],
) -> bytes:
    audio = await audio_input.capture()
    result = process_audio(audio)
    output = await result
    await audio_output.play(output)
    return output
