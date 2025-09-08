import json

from alpha.policy.governance import GovernanceEngine


def test_budget_breaker_and_logging(tmp_path) -> None:
    path = tmp_path / "audit.jsonl"
    eng = GovernanceEngine(max_steps=1, breaker_max_fails=1, audit_path=str(path))
    # first step allowed
    dec1 = eng.decide(query="q", region="r", tool_id="t")
    assert dec1.decision == "allow"
    eng.record_step_result(False)  # failure triggers breaker
    # second step should be blocked
    dec2 = eng.decide()
    assert dec2.decision == "block"
    lines = path.read_text(encoding="utf-8").splitlines()
    assert all(json.loads(line)["event_type"] == "policy_audit" for line in lines)


def test_dry_run_warns(tmp_path) -> None:
    path = tmp_path / "audit.jsonl"
    eng = GovernanceEngine(max_steps=1, dry_run=True, audit_path=str(path))
    eng.decide()
    eng.record_step_result(True)
    dec = eng.decide()
    assert dec.decision == "warn"
    rec = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
    assert rec["decision"] == "warn"
