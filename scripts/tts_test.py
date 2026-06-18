"""
Step 12 test: convert text to speech and play it through the speakers.
"""

import asyncio
import sys
import pyaudio

sys.path.insert(0, ".")
from server.modules.tts.elevenlabs_client import speak_stream

TEST_TEXT = (
    "Hello! I am your personal AI assistant. "
    "I can search the web, set reminders, and control your smart home. "
    "How can I help you today?"
)


async def fake_token_gen():
    for word in TEST_TEXT.split(" "):
        yield word + " "
        await asyncio.sleep(0.05)


async def main() -> None:
    print("Generating audio...")
    chunks = []
    async for audio_chunk in speak_stream(fake_token_gen()):
        chunks.append(audio_chunk)

    print(f"Playing {len(chunks)} chunks...")
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)
    stream.write(b"".join(chunks))
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print("Done.")


asyncio.run(main())
