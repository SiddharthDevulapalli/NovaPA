import asyncio
import logging
import sys
import time
import pyaudio

sys.path.insert(0, ".")

from agent.modules.wake_word.detector import on_wake
from agent.modules.vad.recorder import record_utterance
from agent.modules.vad.config import FOLLOW_UP_TIMEOUT_S, FOLLOW_UP_MIN_RECORDING_S, FOLLOW_UP_SILENCE_COUNT
from server.modules.stt.deepgram_client import transcribe
from server.modules.agent.core import run
from server.modules.agent.history import ConversationHistory
from server.modules.tts.elevenlabs_client import speak_stream

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

history = ConversationHistory()

ACK_PATH = "audio_files/ack.pcm"
try:
    with open(ACK_PATH, "rb") as f:
        _ACK_BYTES = f.read()
    logger.info("Loaded ack sound (%d bytes)", len(_ACK_BYTES))
except FileNotFoundError:
    logger.info("Ack sound not found — generating...")
    from scripts.generate_ack import generate
    generate()
    with open(ACK_PATH, "rb") as f:
        _ACK_BYTES = f.read()
    logger.info("Ack sound generated and loaded (%d bytes)", len(_ACK_BYTES))


def _play(audio_bytes: bytes, rate: int = 22050) -> None:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=rate, output=True)
    stream.write(audio_bytes)
    stream.stop_stream()
    stream.close()
    pa.terminate()


async def _agent_tokens(message: str):
    async for token in run(message, history):
        yield token


async def process_transcript(transcript: str) -> None:
    print(f"\nYou: {transcript}")
    logger.info("Generating response...")
    chunks = []
    async for chunk in speak_stream(_agent_tokens(transcript)):
        chunks.append(chunk)
    _play(b"".join(chunks))


async def handle_conversation() -> None:
    if _ACK_BYTES:
        _play(_ACK_BYTES)
        await asyncio.sleep(0.2)

    audio = record_utterance()
    transcript = await transcribe(audio)

    if not transcript.strip():
        logger.info("Empty transcript — ignoring.")
        return

    await process_transcript(transcript)

    logger.info("Entering follow-up mode for %.0fs...", FOLLOW_UP_TIMEOUT_S)
    follow_up_start = time.time()
    consecutive_empty = 0

    while time.time() - follow_up_start < FOLLOW_UP_TIMEOUT_S:
        logger.info("Listening for follow-up...")
        audio = record_utterance(min_recording_s=FOLLOW_UP_MIN_RECORDING_S)
        transcript = await transcribe(audio)

        if not transcript.strip():
            consecutive_empty += 1
            logger.info("Empty follow-up (%d/%d) — returning to wake word if limit reached.", consecutive_empty, FOLLOW_UP_SILENCE_COUNT)
            if consecutive_empty >= FOLLOW_UP_SILENCE_COUNT:
                logger.info("Follow-up silence limit reached — returning to wake word.")
                break
            continue

        consecutive_empty = 0
        await process_transcript(transcript)
        follow_up_start = time.time()


def on_wake_callback() -> None:
    asyncio.run(handle_conversation())


if __name__ == "__main__":
    print("Personal AI Assistant ready.")
    print("Say 'hey jarvis' to activate. Press Ctrl+C to quit.\n")
    on_wake(on_wake_callback)
