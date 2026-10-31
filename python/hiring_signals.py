"""Compare hiring activity across companies (open roles, growth, top departments).

Usage:
    export APIFY_TOKEN=...
    python hiring_signals.py stripe airbnb lever:spotify lever:palantir
"""
import os
import sys

from apify_client import ApifyClient

companies = sys.argv[1:] or ["stripe", "airbnb", "lever:spotify", "lever:palantir"]
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("caspiandata/ats-jobs-hiring-signals").call(
    run_input={"companies": companies, "outputJobs": False, "emitSignals": True}
)

rows = [i for i in client.dataset(run["defaultDatasetId"]).iterate_items() if i["type"] == "company-signal"]
rows.sort(key=lambda r: r["postedLast30Days"], reverse=True)
print(f"{'Company':<14}{'Open roles':>11}{'Posted 30d':>12}{'Remote %':>10}  Top department")
for r in rows:
    top = r["topDepartments"][0]["name"] if r["topDepartments"] else "-"
    print(f"{r['company']:<14}{r['openRoles']:>11}{r['postedLast30Days']:>12}{round(r['remoteShare'] * 100):>9}%  {top}")
