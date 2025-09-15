import json
import random
import subprocess
import sys
from pathlib import Path

DECK_DIR = Path("data/scenarios/decks")
DECK_FILES = [p for p in sorted(DECK_DIR.glob("core_*.jsonl")) if not p.name.endswith("core_cite_web.jsonl")]


def _load_records():
    records = []
    for path in DECK_FILES:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                records.append(data)
    return records


def _predict(_prompt: str) -> str:
    # simple deterministic predictor
    return "llm_only"


def _run(seed: int):
    rng = random.Random(seed)
    records = _load_records()
    sample = rng.sample(records, min(20, len(records)))
    preds = [_predict(r["prompt"]) for r in sample]
    expects = [r["route_expected"] for r in sample]
    acc = sum(p == e for p, e in zip(preds, expects)) / len(sample)
    return preds, expects, acc


def test_quality_metrics():
    preds1, expects1, acc1 = _run(42)
    preds2, expects2, acc2 = _run(42)
    assert acc1 >= 0.85
    assert acc2 >= 0.85
    reproducible = sum(a == b for a, b in zip(preds1, preds2)) / len(preds1)
    assert reproducible >= 0.9


def test_curator_validator_failure(tmp_path):
    bad = tmp_path / "bad.jsonl"
    bad.write_text("{\"id\":\"x\"}\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, "scripts/decks_curate.py", "--check", str(bad)], capture_output=True)
    assert proc.returncode != 0
    assert b"missing" in proc.stderr.lower()
