import asyncio
import logging
import sys
import pyaudio

sys.path.insert(0, ".")

from agent.modules.wake_word.detector import on_wake
from agent.modules.vad.recorder import record_utterance
from server.modules.stt.deepgram_client import transcribe
from server.modules.agent.core import run
from server.modules.agent.history import ConversationHistory
from server.modules.tts.elevenlabs_client import speak_stream

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

history = ConversationHistory()


def _play(audio_bytes: bytes) -> None:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)
    stream.write(audio_bytes)
    stream.stop_stream()
    stream.close()
    pa.terminate()


async def _agent_tokens(message: str):
    async for token in run(message, history):
        yield token


async def handle_utterance() -> None:
    logger.info("Recording utterance...")
    audio = record_utterance()

    logger.info("Transcribing...")
    transcript = await transcribe(audio)

    if not transcript.strip():
        logger.info("Empty transcript — ignoring.")
        return

    print(f"\nYou: {transcript}")

    logger.info("Generating response...")
    chunks = []
    async for chunk in speak_stream(_agent_tokens(transcript)):
        chunks.append(chunk)

    _play(b"".join(chunks))


def on_wake_callback() -> None:
    asyncio.run(handle_utterance())


if __name__ == "__main__":
    print("Personal AI Assistant ready.")
    print("Say 'hey jarvis' to activate. Press Ctrl+C to quit.\n")
    on_wake(on_wake_callback)
