from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine


def test_safe_out_collects_evidence_and_notes() -> None:
    cfg = SOConfig(low_conf_threshold=0.6, enable_cot_fallback=True, seed=1, max_cot_steps=1)
    sm = SafeOutStateMachine(cfg)
    tot = {
        "answer": "?",
        "confidence": 0.2,
        "reason": "missing_requirements",
        "evidence": ["no operator detected"],
    }
    env = sm.run(tot, "1+1")
    assert env["route"] == "cot_fallback"
    assert env["reason"] == "missing_requirements"
    assert env["evidence"] == ["no operator detected"]
    assert env["recovery_notes"]


def test_safe_out_pass_through_when_confident() -> None:
    cfg = SOConfig(low_conf_threshold=0.1, enable_cot_fallback=True, seed=1, max_cot_steps=1)
    sm = SafeOutStateMachine(cfg)
    tot = {
        "answer": "4",
        "confidence": 0.9,
        "reason": "ok",
        "evidence": ["checks pass"],
    }
    env = sm.run(tot, "2+2")
    assert env["route"] == "tot"
    assert env["reason"] == "ok"
    assert env["evidence"] == ["checks pass"]
    assert env["recovery_notes"] == ""
