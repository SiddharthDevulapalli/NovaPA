import logging
import webbrowser

logger = logging.getLogger(__name__)


def open_url(url: str) -> str:
    try:
        webbrowser.open(url)
        return f"Opened browser at: {url}"
    except Exception as e:
        logger.error("Failed to open browser: %s", e)
        return f"Failed to open browser: {e}"
