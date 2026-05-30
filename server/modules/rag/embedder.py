import logging
from openai import OpenAI
from .config import OPENAI_API_KEY, EMBEDDING_MODEL

logger = logging.getLogger(__name__)
_oaiClient = OpenAI(api_key=OPENAI_API_KEY)


def embed(texts: list[str]) -> list[list[float]]:
    try:
        response = _oaiClient.embeddings.create(model=EMBEDDING_MODEL, input=texts)
        return [r.embedding for r in response.data]
    except Exception as e:
        logger.error("Embedding failed: %s", e)
        return []
