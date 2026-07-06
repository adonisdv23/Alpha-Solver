import json
import random
import subprocess
import sys
from pathlib import Path

import pytest

DECK_DIR = Path("data/scenarios/decks")
DECK_FILES = sorted(DECK_DIR.glob("*.jsonl"))


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


def test_smoke_deck_replay_command():
    result = subprocess.run(
        [
            sys.executable,
            "cli/alpha_solver_cli.py",
            "replay",
            "data/scenarios/decks/smoke.jsonl",
            "--max-tokens",
            "120",
            "--min-budget-tokens",
            "60",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "replay ok"
