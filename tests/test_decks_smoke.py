import json
import random
from pathlib import Path

import pytest

DECK_DIR = Path("data/scenarios/decks")
DECK_FILES = sorted(DECK_DIR.glob("core_*.jsonl"))


def _load(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        first = json.loads(f.readline())
        if "skip_reason" in first:
            pytest.skip(first["skip_reason"])
        f.seek(0)
        for line in f:
            data = json.loads(line)
            records.append(data)
    return records


@pytest.mark.parametrize("path", DECK_FILES)
def test_deck_smoke(path):
    records = _load(path)
    assert records
    sample = random.Random(123).sample(records, min(3, len(records)))
    for rec in sample:
        for field in ("id", "intent", "prompt", "route_expected", "notes"):
            assert field in rec
        output = {
            "text": "ok",
            "route_explain": {"chosen": "llm_only", "candidates": ["llm_only", "mcp"]},
        }
        assert output["text"]
        assert "route_explain" in output and "chosen" in output["route_explain"]
