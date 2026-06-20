import io
import wave
import logging
import numpy as np
import pyaudio
from .config import SILENCE_THRESHOLD, SILENCE_DURATION_MS, MAX_DURATION_S, MIN_RECORDING_S, SAMPLE_RATE, CHUNK

logger = logging.getLogger(__name__)


def record_utterance(min_recording_s: float = MIN_RECORDING_S) -> bytes:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0
    max_chunks = int(SAMPLE_RATE / CHUNK * MAX_DURATION_S)
    silence_chunks_needed = int((SILENCE_DURATION_MS / 1000) / (CHUNK / SAMPLE_RATE))
    min_chunks = int(SAMPLE_RATE / CHUNK * min_recording_s)

    logger.info("Recording utterance...")
    for i in range(max_chunks):
        audio = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(audio)
        if i < min_chunks:
            continue
        rms = np.sqrt(np.mean(np.frombuffer(audio, dtype=np.int16).astype(np.float32) ** 2))
        if rms < SILENCE_THRESHOLD:
            silent_chunks += 1
            if silent_chunks >= silence_chunks_needed:
                logger.info("Silence detected, stopping recording.")
                break
        else:
            silent_chunks = 0

    stream.stop_stream()
    stream.close()
    pa.terminate()

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))
    return buf.getvalue()
