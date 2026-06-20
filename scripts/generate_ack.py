"""
One-time script: generates a short acknowledgment sound via ElevenLabs
and saves it as raw PCM to audio_files/ack.pcm.
Run once: python scripts/generate_ack.py
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, ".")

from agent.modules.vad.config import ACK_TEXT

API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
OUTPUT_PATH = "audio_files/ack.pcm"


def generate() -> None:
    response = httpx.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        params={"output_format": "pcm_22050"},
        json={
            "text": ACK_TEXT,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        },
    )
    response.raise_for_status()
    with open(OUTPUT_PATH, "wb") as f:
        f.write(response.content)
    print(f"Saved ack sound ({len(response.content)} bytes) to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
