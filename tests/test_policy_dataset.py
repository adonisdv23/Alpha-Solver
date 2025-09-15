import re
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from fixtures.datasets import load_jsonl

EMAIL_RE = re.compile(r"\b[\w.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
PHONE_RE = re.compile(r"\b555-010\d{3}\b")

DATA_PATH = Path(__file__).resolve().parents[1] / "data/datasets/pii/labels_email_phone.jsonl"


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text


def test_policy_dataset():
    items = load_jsonl(DATA_PATH, ["id", "text", "label"])
    assert len(items) >= 100
    counts = {"email": 0, "phone": 0}
    logs = []
    durations = []
    matches = 0
    for item in items:
        start = time.perf_counter()
        redacted = redact(item["text"])
        durations.append((time.perf_counter() - start) * 1000)
        logs.append(redacted)
        if item["label"] == "email":
            counts["email"] += 1
            if EMAIL_RE.search(item["text"]):
                matches += 1
        elif item["label"] == "phone":
            counts["phone"] += 1
            if PHONE_RE.search(item["text"]):
                matches += 1
    assert counts["email"] == counts["phone"] == 50
    assert matches / len(items) >= 0.99
    p95 = sorted(durations)[int(len(durations) * 0.95) - 1]
    assert p95 < 50
    for entry in logs:
        assert not EMAIL_RE.search(entry)
        assert not PHONE_RE.search(entry)
