import glob
import json
import collections
import subprocess
import sys

subprocess.run([
    sys.executable,
    "scripts/telemetry_leaderboard.py",
    "--paths",
    "telemetry/.jsonl",
    "--topk",
    "5",
    "--format",
    "md",
    "--out",
    "artifacts/leaderboard.md",
], check=True)

counts = collections.defaultdict(int)
for p in glob.glob("artifacts/shortlists//*.json"):
    try:
        with open(p, "r", encoding="utf-8") as fh:
            j = json.load(fh)
        counts[j.get("region", "?")] += 1
    except Exception:
        pass
print("Snapshot counts by region:")
for k in sorted(counts):
    print(f" {k}: {counts[k]}")
