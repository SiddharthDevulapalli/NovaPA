"""
Step 5: Learn RAG concepts.
Embed sentences, store in ChromaDB, query with a question, see closest matches.
"""

import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

oaiClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma = chromadb.Client()
collection = chroma.create_collection("rag_experiment")

SENTENCES = [
    "The Eiffel Tower is located in Paris, France.",
    "Python was created by Guido van Rossum in 1991.",
    "The mitochondria is the powerhouse of the cell.",
    "Machine learning models learn patterns from data.",
    "The Great Wall of China stretches over 13,000 miles.",
    "Neural networks are inspired by the human brain.",
    "Water boils at 100 degrees Celsius at sea level.",
    "FastAPI is a modern Python web framework.",
    "Siddharth is learning about RAG and vector databases.",
    "Sid says, 'What you are today is not important, it's what you become that matters.'",
]


def embed(texts: list[str]) -> list[list[float]]:
    response = oaiClient.embeddings.create(model="text-embedding-3-small", input=texts)
    return [r.embedding for r in response.data]


print("Embedding and storing sentences...")
vectors = embed(SENTENCES)
collection.add(
    ids=[str(i) for i in range(len(SENTENCES))],
    embeddings=vectors,
    documents=SENTENCES,
)
print(f"Stored {len(SENTENCES)} sentences.\n")

QUERIES = [
    "Where is the Eiffel Tower?",
    "Tell me about deep learning.",
    "What web framework should I use for Python APIs?",
    "Who is Siddharth and what is he learning?",
    "What did Sid say about becoming?"
]

for query in QUERIES:
    query_vector = embed([query])[0]
    results = collection.query(query_embeddings=[query_vector], n_results=2)
    print(f"Query: {query}")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        print(f"  [{distance:.4f}] {doc}")
    print()
