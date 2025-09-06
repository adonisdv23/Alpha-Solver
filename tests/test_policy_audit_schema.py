import json
import re

from alpha.policy.engine import PolicyEngine


def test_policy_audit_schema(tmp_path):
    audit = tmp_path / "audit.jsonl"
    engine = PolicyEngine(audit_path=str(audit))
    engine.decide(query="q", region="r", tool_id="t")
    lines = audit.read_text().strip().splitlines()
    assert len(lines) >= 2
    header = json.loads(lines[0])
    assert header["run_id"]
    assert header["now_utc"].endswith("Z")
    rec = json.loads(lines[1])
    for field in [
        "run_id",
        "step_index",
        "query",
        "region",
        "tool_id",
        "decision",
        "reason",
        "budget",
        "breaker",
        "data_class",
        "timestamp",
    ]:
        assert field in rec
    assert re.match(r"\d{4}-\d{2}-\d{2}T.*Z", rec["timestamp"])
