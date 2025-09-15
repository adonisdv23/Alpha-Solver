import os
import random

from service.replay.player import Player
from service.replay.recorder import Recorder


def pipeline(payload, seed):
    rnd = random.Random(seed)
    score = rnd.random()
    gate = "open" if score > 0.5 else "closed"
    output = f"{payload['query']}::{score:.3f}"
    route_explain = {
        "scores": {"score": score},
        "gate_decisions": {"gate": gate},
        "plan_winner": "A" if score > 0.3 else "B",
        "budget_verdict": "ok",
    }
    return output, route_explain


def test_replay_stability_across_scenarios():
    os.environ["REPLAY_CI"] = "1"
    recorder = Recorder()
    player = Player()

    scenarios = [
        ("s1", {"query": "hello 123"}, 1),
        ("s2", {"query": "world 456"}, 2),
        ("s3", {"query": "foo"}, 3),
    ]

    for name, payload, seed in scenarios:
        record = recorder.record(name, payload, seed=seed, run_func=pipeline)
        # ensure redaction removed digits
        assert not any(ch.isdigit() for ch in record["payload"]["query"])
        for _ in range(10):
            result = player.replay(record, pipeline)
            assert result["hash"] == record["hash"]
            assert result["route_explain"] == record["route_explain"]
