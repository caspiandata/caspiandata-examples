"""Convert PDFs to Markdown chunks ready for embeddings, using the Document to Markdown Actor.

Usage:
    export APIFY_TOKEN=...
    python pdf_to_markdown_rag.py https://arxiv.org/pdf/1706.03762 [more URLs]
"""
import json
import os
import sys

from apify_client import ApifyClient

urls = sys.argv[1:] or ["https://arxiv.org/pdf/1706.03762"]
client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("caspiandata/doc-to-markdown").call(
    run_input={
        "urls": urls,
        "ocr": "auto",          # OCR only pages that have no text layer
        "chunkSize": 1200,      # characters per chunk
        "chunkOverlap": 120,
    }
)

records = []
for doc in client.dataset(run["defaultDatasetId"]).iterate_items():
    if doc.get("error"):
        print(f"Skipped {doc['sourceUrl']}: {doc['error']}", file=sys.stderr)
        continue
    for chunk in doc["chunks"]:
        records.append(
            {
                "id": f"{doc['sourceUrl']}#{chunk['index']}",
                "text": chunk["text"],
                "metadata": {"source": doc["sourceUrl"], "title": doc.get("title"), "heading": chunk["heading"]},
            }
        )

# Records are ready for any embedding model / vector database (Pinecone, Qdrant, pgvector, ...).
with open("chunks.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"Wrote {len(records)} chunks to chunks.jsonl")
