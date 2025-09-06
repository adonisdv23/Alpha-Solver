from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_seed(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("seed")
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a plan or shortlist deterministically")
    parser.add_argument("--plan", help="Path to plan JSON")
    parser.add_argument("--shortlist", help="Path to shortlist snapshot JSON")
    args = parser.parse_args()

    source = args.plan or args.shortlist
    if not source:
        parser.error("--plan or --shortlist required")
    src_path = Path(source)
    seed = load_seed(src_path)

    start = datetime.now(timezone.utc)
    run_dir = Path("artifacts") / "replay"
    ts = start.strftime("%Y%m%dT%H%M%SZ")
    out_dir = run_dir / f"run_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # This MVP does not execute the plan; it merely logs metadata.
    end = datetime.now(timezone.utc)
    header = {
        "source_path": str(src_path),
        "run_id": f"run_{ts}",
        "seed": seed,
        "started_at": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ended_at": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "ok",
    }
    (out_dir / "replay.json").write_text(
        json.dumps(header, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
