import logging
from typing import TypedDict

import httpx

from .config import BRAVE_API_KEY, BRAVE_SEARCH_URL, SEARCH_RESULT_COUNT, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class SearchResult(TypedDict):
    title: str
    url: str
    snippet: str


async def search(query: str) -> list[SearchResult]:
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    params = {"q": query, "count": SEARCH_RESULT_COUNT}

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(BRAVE_SEARCH_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        logger.warning("Brave search timed out for query: %s", query)
        return []
    except httpx.HTTPStatusError as e:
        logger.error("Brave search HTTP error: %s", e)
        return []
    except Exception as e:
        logger.error("Brave search unexpected error: %s", e)
        return []

    results = []
    for item in data.get("web", {}).get("results", []):
        results.append(SearchResult(
            title=item.get("title", ""),
            url=item.get("url", ""),
            snippet=item.get("description", ""),
        ))
    return results
