from pathlib import Path

from alpha.eval.harness import run_eval


def test_run_eval_smoke(tmp_path):
    root = Path(__file__).resolve().parents[1]
    dataset = root / "datasets" / "mvp_golden.jsonl"
    report = run_eval(str(dataset), seed=1337, scorers=["em", "f1"], limit=2)
    assert "examples" in report
    assert len(report["examples"]) > 0
    assert "metrics" in report
