import json

from alpha.policy.engine import PolicyEngine


def test_policy_data_class(tmp_path):
    policy_path = tmp_path / "data_policy.json"
    policy_path.write_text(
        json.dumps(
            {
                "deny": {"families": ["denyfam"], "tags": ["pii"]},
                "allow": {"families": [], "tags": []},
            }
        )
    )
    audit = tmp_path / "audit.jsonl"
    engine = PolicyEngine(data_policy_path=str(policy_path), audit_path=str(audit))
    dec = engine.decide(
        query="q",
        region="r",
        tool_id="t",
        family="denyfam",
        tags=["pii"],
    )
    assert dec.decision == "block"
    rec = json.loads(audit.read_text().strip().splitlines()[-1])
    assert rec["data_class"]["status"] == "deny"
