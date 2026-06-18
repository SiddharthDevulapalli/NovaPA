import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
MODEL_ID = "eleven_turbo_v2_5"
REQUEST_TIMEOUT = 30

TTS_STREAMING = os.getenv("TTS_STREAMING", "false").lower() == "true"
_base = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
ELEVENLABS_URL = f"{_base}/stream" if TTS_STREAMING else _base
