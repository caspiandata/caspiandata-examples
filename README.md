# Caspian Data — examples

Small, copy-paste examples for the **Caspian Data** Actors on [Apify Store](https://apify.com/caspiandata). Each example runs in a few seconds and costs a fraction of a cent.

| Actor | What it does | Examples |
|---|---|---|
| [Document to Markdown](https://apify.com/caspiandata/doc-to-markdown) | PDF, DOCX and HTML → clean Markdown, automatic OCR for scans, RAG-ready chunks | [Python](python/pdf_to_markdown_rag.py) · [JavaScript](javascript/pdf-to-markdown.mjs) |
| [Company Jobs Tracker](https://apify.com/caspiandata/ats-jobs-hiring-signals) | Jobs from any company on Greenhouse or Lever, new-jobs-only mode, hiring signals | [New jobs alert](python/track_new_jobs.py) · [Hiring signals](python/hiring_signals.py) |

## Setup

1. Create a free Apify account and copy your API token from **Settings → API & Integrations**.
2. Export it:

```bash
export APIFY_TOKEN=your_token_here
```

3. Install the client:

```bash
pip install apify-client      # Python
npm install apify-client      # JavaScript
```

## PDF → Markdown chunks for RAG (Python)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("caspiandata/doc-to-markdown").call(run_input={
    "urls": ["https://arxiv.org/pdf/1706.03762"],
    "pageRange": "1-5",
    "chunkSize": 1200,
})
for doc in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(doc["title"], len(doc["chunks"]), "chunks")
```

Each chunk has `heading`, `text` and `chars`, so you can embed `text` and keep `heading` as metadata.

## Daily "new jobs" alert (Python)

Run [`track_new_jobs.py`](python/track_new_jobs.py) once a day (cron, GitHub Actions or an Apify schedule). The first run returns all open roles; later runs return only postings that are new since the previous run.

## License

MIT
