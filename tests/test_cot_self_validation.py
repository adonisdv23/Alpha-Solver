from alpha.core.runner import run_reasoning
from alpha.core.config import ValidationConfig
from alpha.reasoning.cot_self_validate import validate_answer


def test_cot_self_validation_deterministic():
    cfg = ValidationConfig(enabled=True, min_conf=0.7)
    results = [
        run_reasoning(
            "1+1",
            seed=42,
            config=cfg,
            cot_steps=["1 + 1"],
            answer="3",
            confidence=0.5,
        )
        for _ in range(3)
    ]
    assert all(r["answer"] == "2" for r in results)
    assert results[0] == results[1] == results[2]
    ok_true, _ = validate_answer(["1 + 1"], "2")
    ok_false, _ = validate_answer(["1 + 1"], "3")
    assert ok_true and not ok_false
