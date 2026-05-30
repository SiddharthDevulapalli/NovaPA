"""
Step 6 test: ingest a PDF, then query it.
Usage: python scripts/rag_test.py path/to/your.pdf "your question here"
"""

import sys
sys.path.insert(0, ".")

from server.modules.rag.ingestion import ingest
from server.modules.rag.retrieval import retrieve

if len(sys.argv) < 3:
    print("Usage: python scripts/rag_test.py <pdf_path> <question>")
    sys.exit(1)

pdf_path = sys.argv[1]
question = sys.argv[2]

print(f"Ingesting {pdf_path}...")
result = ingest(pdf_path)
print(result)

print(f"\nQuerying: {question!r}")
chunks = retrieve(question)
for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---\n{chunk}")
