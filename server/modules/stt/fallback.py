import logging

logger = logging.getLogger(__name__)


def transcribe(audio_bytes: bytes) -> str:
    logger.warning("STT fallback triggered — returning empty transcript.")
    return ""
