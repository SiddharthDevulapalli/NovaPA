import logging
import numpy as np
from typing import Callable
from openwakeword.model import Model
from .config import WAKE_WORD_THRESHOLD, PRETRAINED_MODEL, AUDIO_CHUNK
from .audio_stream import open_stream, close_stream

logger = logging.getLogger(__name__)


def on_wake(callback: Callable[[], None]) -> None:
    model = Model(wakeword_models=[PRETRAINED_MODEL], inference_framework="onnx")
    pa, stream = open_stream()
    logger.info("Listening for wake word '%s'...", PRETRAINED_MODEL)

    try:
        while True:
            audio = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
            frame = np.frombuffer(audio, dtype=np.int16)
            prediction = model.predict(frame)
            score = prediction.get(PRETRAINED_MODEL, 0)
            if score >= WAKE_WORD_THRESHOLD:
                logger.info("Wake word detected (score=%.2f)", score)
                close_stream(pa, stream)
                callback()
                pa, stream = open_stream()
    except KeyboardInterrupt:
        logger.info("Wake word detector stopped.")
    finally:
        close_stream(pa, stream)
