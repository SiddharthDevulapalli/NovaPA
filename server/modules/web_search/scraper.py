import logging
import httpx
from .config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


async def fetch_page(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text
    except httpx.TimeoutException:
        logger.warning("Page fetch timed out: %s", url)
        return ""
    except httpx.HTTPStatusError as e:
        logger.error("Page fetch HTTP error %s: %s", e.response.status_code, url)
        return ""
    except Exception as e:
        logger.error("Page fetch unexpected error: %s", e)
        return ""
