import logging
import httpx
from typing import AsyncGenerator
from .config import ELEVENLABS_API_KEY, ELEVENLABS_URL, MODEL_ID, REQUEST_TIMEOUT, TTS_STREAMING

logger = logging.getLogger(__name__)


async def speak_stream(token_gen: AsyncGenerator[str, None]) -> AsyncGenerator[bytes, None]:
    from .sentence_buffer import stream_sentences

    async for sentence in stream_sentences(token_gen):
        logger.info("TTS sentence: %s", sentence)
        async for chunk in _synthesize(sentence):
            yield chunk


async def _synthesize(text: str) -> AsyncGenerator[bytes, None]:
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            params = {"output_format": "pcm_22050"}
            if TTS_STREAMING:
                async with client.stream("POST", ELEVENLABS_URL, headers=headers, json=payload, params=params) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        if chunk:
                            yield chunk
            else:
                response = await client.post(ELEVENLABS_URL, headers=headers, json=payload, params=params)
                response.raise_for_status()
                yield response.content

    except httpx.TimeoutException:
        logger.error("ElevenLabs request timed out for text: %s", text)
    except httpx.HTTPStatusError as e:
        logger.error("ElevenLabs HTTP error: %s", e)
    except Exception as e:
        logger.error("ElevenLabs unexpected error: %s", e)
