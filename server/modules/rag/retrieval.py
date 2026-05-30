import logging
import chromadb
from .config import CHROMA_PERSIST_PATH, COLLECTION_NAME, RETRIEVAL_TOP_K
from .embedder import embed

logger = logging.getLogger(__name__)


def _get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    return client.get_or_create_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = RETRIEVAL_TOP_K) -> list[str]:
    try:
        vectors = embed([query])
        if not vectors:
            return []

        collection = _get_collection()
        results = collection.query(query_embeddings=[vectors[0]], n_results=k)
        return results["documents"][0]
    except Exception as e:
        logger.error("Retrieval failed: %s", e)
        return []
