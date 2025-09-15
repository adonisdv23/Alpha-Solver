import random
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fixtures.datasets import load_jsonl

ROOT = Path(__file__).resolve().parents[1] / "data/datasets"


def test_scenarios_smoke():
    pii = load_jsonl(ROOT / "pii/labels_email_phone.jsonl", ["id", "text", "label"])[0]
    routing = load_jsonl(ROOT / "routing/scenarios_routing.jsonl", ["id", "query", "label"])[0]
    replay = load_jsonl(ROOT / "replay/replay_small.jsonl", ["id", "input", "result"])[0]

    assert re.search(r"example.com", pii["text"]) or re.search(r"555-010", pii["text"])
    router_label = "mcp" if "database" in routing["query"].lower() or "tool" in routing["query"].lower() else "llm_only"
    assert router_label == routing["label"]
    rnd = random.Random(1234 + replay["id"])
    assert rnd.randint(0, 1000) == replay["result"]
