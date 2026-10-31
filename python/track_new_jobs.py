"""Print job postings that are new since the last run, for a watchlist of companies.

Run it daily. The Actor keeps the state, so you only see fresh postings.

Usage:
    export APIFY_TOKEN=...
    python track_new_jobs.py
"""
import os

from apify_client import ApifyClient

WATCHLIST = ["https://boards.greenhouse.io/stripe", "greenhouse:airbnb", "lever:spotify"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("caspiandata/ats-jobs-hiring-signals").call(
    run_input={
        "companies": WATCHLIST,
        "keywords": ["data", "analytics", "engineer"],
        "onlyNew": True,
        "stateKey": "my-daily-watchlist",
        "emitSignals": False,
    }
)

new_jobs = [i for i in client.dataset(run["defaultDatasetId"]).iterate_items() if i["type"] == "job"]
print(f"{len(new_jobs)} new job(s)")
for job in new_jobs:
    print(f"- {job['company']}: {job['title']} ({job['location']}) {job['url']}")
