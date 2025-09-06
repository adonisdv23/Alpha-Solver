"""Local CSV operations."""
import csv
import time
from pathlib import Path
from typing import Dict, Any

TOOL_ID = "local.csv.ops"

_ARTIFACT_DIR = Path("artifacts/exec/csv")


def _timestamp() -> str:
    return time.strftime("%Y%m%d%H%M%S", time.gmtime())


def row_count(path: str) -> Dict[str, Any]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        count = sum(1 for _ in reader)
    return {"ok": True, "rows": count}


def filter_rows(path: str, col: str, value: str, out_name: str) -> Dict[str, Any]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = [row for row in reader if row.get(col) == value]
        fieldnames = reader.fieldnames if reader.fieldnames else []

    _ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _ARTIFACT_DIR / f"{_timestamp()}_{Path(out_name).name}"
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return {"ok": True, "rows": len(rows), "out": str(out_path)}
