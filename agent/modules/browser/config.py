import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v="
YOUTUBE_FALLBACK_URL = "https://www.youtube.com/results?search_query="
REQUEST_TIMEOUT = 10
