#!/usr/bin/env python3
"""Utility script to print the P0+P1 bulk review artifact.

This helper loads ``artifacts/review_p0p1.json`` and prints it in a
human-readable format. It is intended for one-off inspection and does
not alter runtime behavior.
"""
import json
from pathlib import Path

def main() -> None:
    artifact_path = Path(__file__).resolve().parents[1] / "artifacts" / "review_p0p1.json"
    data = json.loads(artifact_path.read_text())
    print(json.dumps(data, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
