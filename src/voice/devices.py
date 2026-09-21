from collections.abc import Awaitable, Callable
import asyncio
import io
import wave
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


class MacAudioInput:
    def __init__(self, sample_rate: int = 16_000, channels: int = 1, seconds: int = 5) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.seconds = seconds

    async def capture(self) -> bytes:
        return await self._capture()

    async def _capture(self) -> bytes:
        try:
            import sounddevice as sd
        except ImportError as error:
            raise RuntimeError("Instale sounddevice para capturar audio no macOS.") from error
        recording = await asyncio.to_thread(
            sd.rec,
            int(self.seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
        )
        await asyncio.to_thread(sd.wait)
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(self.channels)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(recording.tobytes())
        return buffer.getvalue()


class MacAudioOutput:
    def __init__(self, sample_rate: int = 16_000, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    async def play(self, audio: bytes) -> None:
        try:
            import numpy as np
            import sounddevice as sd
        except ImportError as error:
            raise RuntimeError("Instale sounddevice e numpy para reproduzir audio no macOS.") from error
        sample_rate = self.sample_rate
        channels = self.channels
        samples_data = audio
        if audio[:4] == b"RIFF":
            with wave.open(io.BytesIO(audio), "rb") as wav:
                sample_rate = wav.getframerate()
                channels = wav.getnchannels()
                samples_data = wav.readframes(wav.getnframes())
        samples = np.frombuffer(samples_data, dtype="int16")
        await asyncio.to_thread(
            sd.play, samples, sample_rate
        )
        await asyncio.to_thread(sd.wait)


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
