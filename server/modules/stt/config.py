import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"
MODEL = "nova-2"
LANGUAGE = "en"
REQUEST_TIMEOUT = 15
