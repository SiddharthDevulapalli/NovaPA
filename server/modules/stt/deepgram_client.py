import logging
import httpx
from .config import DEEPGRAM_API_KEY, DEEPGRAM_URL, MODEL, LANGUAGE, REQUEST_TIMEOUT
from .fallback import transcribe as fallback_transcribe

logger = logging.getLogger(__name__)


async def transcribe(audio_bytes: bytes) -> str:
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav",
    }
    params = {
        "model": MODEL,
        "language": LANGUAGE,
        "punctuate": "true",
        "smart_format": "true",
        "no_log": "true",
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(DEEPGRAM_URL, headers=headers, params=params, content=audio_bytes)
            response.raise_for_status()
            data = response.json()

        transcript = (
            data.get("results", {})
                .get("channels", [{}])[0]
                .get("alternatives", [{}])[0]
                .get("transcript", "")
        )
        logger.info("Transcript: %s", transcript)
        return transcript

    except httpx.TimeoutException:
        logger.error("Deepgram request timed out.")
        return fallback_transcribe(audio_bytes)
    except httpx.HTTPStatusError as e:
        logger.error("Deepgram HTTP error: %s", e)
        return fallback_transcribe(audio_bytes)
    except Exception as e:
        logger.error("Deepgram unexpected error: %s", e)
        return fallback_transcribe(audio_bytes)
