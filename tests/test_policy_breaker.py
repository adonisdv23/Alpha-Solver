import json

from alpha.policy.engine import PolicyEngine


def test_policy_breaker_trips(tmp_path):
    audit = tmp_path / "audit.jsonl"
    engine = PolicyEngine(breaker_max_fails=2, audit_path=str(audit))
    for _ in range(2):
        dec = engine.decide(query="q", region="r", tool_id="t")
        assert dec.decision == "allow"
        engine.record_step_result(False)
    dec = engine.decide(query="q", region="r", tool_id="t")
    assert dec.decision == "block"
    lines = audit.read_text().strip().splitlines()
    rec = json.loads(lines[-1])
    assert rec["breaker"]["tripped"] is True
