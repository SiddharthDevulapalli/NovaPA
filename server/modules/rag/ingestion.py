import logging
import PyPDF2
import chromadb
from .config import CHROMA_PERSIST_PATH, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from .embedder import embed

logger = logging.getLogger(__name__)


def _get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    return client.get_or_create_collection(COLLECTION_NAME)


def _extract_text(file_path: str) -> str:
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return " ".join(page.extract_text() or "" for page in reader.pages)


def _chunk(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c.strip()]


def ingest(file_path: str) -> str:
    try:
        text = _extract_text(file_path)
        if not text.strip():
            return "Could not extract text from PDF."

        chunks = _chunk(text)
        vectors = embed(chunks)
        if not vectors:
            return "Embedding failed."

        collection = _get_collection()
        ids = [f"{file_path}::{i}" for i in range(len(chunks))]
        collection.add(ids=ids, embeddings=vectors, documents=chunks)

        logger.info("Ingested %d chunks from %s", len(chunks), file_path)
        return f"Ingested {len(chunks)} chunks from {file_path}."
    except Exception as e:
        logger.error("Ingestion failed: %s", e)
        return f"Ingestion error: {e}"
