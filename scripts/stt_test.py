"""
Step 11 test: record 5 seconds from mic and print the transcript.
"""

import asyncio
import io
import sys
import wave
import pyaudio

sys.path.insert(0, ".")
from server.modules.stt.deepgram_client import transcribe

RATE = 16000
CHUNK = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16
DURATION = 5


def record() -> bytes:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording for 5 seconds... speak now!")
    frames = [stream.read(CHUNK) for _ in range(int(RATE / CHUNK * DURATION))]
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print("Done recording.\n")

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
    return buf.getvalue()


async def main() -> None:
    audio_bytes = record()
    transcript = await transcribe(audio_bytes)
    print(f"Transcript: {transcript!r}")

asyncio.run(main())
