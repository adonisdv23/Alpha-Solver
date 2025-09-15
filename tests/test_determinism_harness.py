import json
import hashlib
import pytest
from service.observability.replay import ReplayHarness


@pytest.mark.determinism
def test_replay_harness_is_deterministic(tmp_path):
    events = [
        {"name": "a", "payload": 1},
        {"name": "b", "payload": {"x": 2}},
        {"name": "c", "payload": "z"},
    ]
    log_path = tmp_path / "events.jsonl"
    with open(log_path, "w", encoding="utf-8") as fh:
        for ev in events:
            fh.write(json.dumps(ev) + "\n")

    harness = ReplayHarness(str(log_path))
    baseline = list(harness.iter_events())
    baseline_hash = hashlib.sha256(json.dumps(baseline, sort_keys=True).encode()).hexdigest()

    for _ in range(10):
        run = list(harness.iter_events())
        run_hash = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
        assert run_hash == baseline_hash
