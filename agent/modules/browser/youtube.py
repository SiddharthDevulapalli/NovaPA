import logging
import urllib.parse
import httpx
from .config import YOUTUBE_API_KEY, YOUTUBE_SEARCH_URL, YOUTUBE_WATCH_URL, YOUTUBE_FALLBACK_URL, REQUEST_TIMEOUT
from .opener import open_url

logger = logging.getLogger(__name__)


def play_youtube(query: str) -> str:
    video_url = _find_video(query) if YOUTUBE_API_KEY else _fallback_url(query)
    open_url(video_url)
    return f"Playing YouTube: {query}"


def _find_video(query: str) -> str:
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY,
    }
    try:
        response = httpx.get(YOUTUBE_SEARCH_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        items = response.json().get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            return f"{YOUTUBE_WATCH_URL}{video_id}"
    except Exception as e:
        logger.warning("YouTube API failed, using fallback: %s", e)
    return _fallback_url(query)


def _fallback_url(query: str) -> str:
    return f"{YOUTUBE_FALLBACK_URL}{urllib.parse.quote_plus(query)}"
