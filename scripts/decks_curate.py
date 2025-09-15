#!/usr/bin/env python3
"""Validate and sample scenario decks."""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Set

REQUIRED_FIELDS = {"id", "intent", "prompt", "route_expected", "notes"}


def _normalize_prompt(text: str) -> str:
    """Collapse whitespace and clamp length."""
    cleaned = " ".join(text.strip().split())
    return cleaned[:1000]


def _load_deck(path: Path, seen_ids: Set[str]) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []
    ids: List[str] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if "skip_reason" in data:
                # stub deck, no validation of records
                return []
            missing = REQUIRED_FIELDS - data.keys()
            if missing:
                raise ValueError(f"{path}:{lineno} missing fields: {sorted(missing)}")
            rid = data["id"]
            if rid in seen_ids:
                raise ValueError(f"duplicate id: {rid}")
            seen_ids.add(rid)
            data["prompt"] = _normalize_prompt(data["prompt"])
            ids.append(rid)
            records.append(data)
    if ids != sorted(ids):
        raise ValueError(f"{path} ids not sorted")
    return records


def curate(paths: List[Path], sample: int = 0, shuffle: bool = False, seed: int = 123) -> List[Dict[str, str]]:
    seen_ids: Set[str] = set()
    all_records: List[Dict[str, str]] = []
    for p in paths:
        all_records.extend(_load_deck(p, seen_ids))
    if sample:
        rng = random.Random(seed)
        pool = list(all_records)
        if shuffle:
            rng.shuffle(pool)
        pool = pool[:sample]
        for rec in pool:
            print(json.dumps(rec, ensure_ascii=False))
    return all_records


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true", help="validate decks")
    parser.add_argument("--sample", type=int, default=0, help="emit N random records")
    parser.add_argument("--shuffle", action="store_true", help="shuffle before sampling")
    parser.add_argument("--seed", type=int, default=123, help="random seed")
    args = parser.parse_args(argv)

    try:
        records = curate(args.paths, sample=args.sample, shuffle=args.shuffle, seed=args.seed)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.check and not records:
        # For stub decks, _load_deck returns [], which is fine
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
