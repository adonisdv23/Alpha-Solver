import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fixtures.datasets import load_jsonl

DATA_PATH = Path(__file__).resolve().parents[1] / "data/datasets/replay/replay_small.jsonl"


def process(item, seed: int = 1234) -> int:
    rnd = random.Random(seed + item["id"])
    return rnd.randint(0, 1000)


def test_replay_stability():
    items = load_jsonl(DATA_PATH, ["id", "input", "result"])
    outputs1 = [process(item) for item in items]
    outputs2 = [process(item) for item in items]
    expected = [item["result"] for item in items]
    assert outputs1 == outputs2 == expected
    assert len(items) >= 10
