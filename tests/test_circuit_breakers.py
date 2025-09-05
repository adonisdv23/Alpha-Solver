from pathlib import Path
from alpha.core import runner


def test_circuit_breaker_trips(tmp_path):
    plan = {
        "steps": [
            {"tool_id": "a"},
            {"tool_id": "b"},
        ],
        "breaker": {"trip_count": 1},
    }
    trace = runner.run(plan)
    assert len(trace) == 1  # second step blocked
    assert Path(plan["audit_log"]).exists()
