import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fixtures.datasets import load_jsonl

DATA_PATH = Path(__file__).resolve().parents[1] / "data/datasets/routing/scenarios_routing.jsonl"


def simple_router(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["database", "tool", "fetch", "lookup"]):
        return "mcp"
    return "llm_only"


def test_routing_accuracy():
    items = load_jsonl(DATA_PATH, ["id", "query", "label"])
    total = 0
    correct = 0
    for item in items:
        label = item["label"]
        if label not in {"llm_only", "mcp"}:
            continue
        pred = simple_router(item["query"])
        if pred == label:
            correct += 1
        total += 1
    assert total >= 30
    assert correct / total >= 0.9
