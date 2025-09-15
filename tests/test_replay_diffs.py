import os
import random

import pytest

from service.replay.player import Player, ReplayMismatch
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


def test_diff_on_seed_change():
    recorder = Recorder()
    player = Player()
    record = recorder.record("base", {"query": "hello"}, seed=1, run_func=pipeline)
    bad = dict(record)
    bad["seed"] = 2
    with pytest.raises(ReplayMismatch) as exc:
        player.replay(bad, pipeline)
    msg = exc.value.args[0]
    assert "scores" in msg
    assert "hash" in msg


def test_snapshot_change_affects_hash(tmp_path):
    os.environ["TOOL_REGISTRY_SHA"] = "A"
    recorder = Recorder()
    player = Player()
    record = recorder.record("snap", {"query": "world"}, seed=1, run_func=pipeline)

    os.environ["TOOL_REGISTRY_SHA"] = "B"
    with pytest.raises(ReplayMismatch) as exc:
        player.replay(record, pipeline)
    assert "tool_registry_sha" in exc.value.args[0]

    os.environ["TOOL_REGISTRY_SHA"] = "A"
    result = player.replay(record, pipeline)
    assert result["hash"] == record["hash"]
