from alpha.eval.harness import run_eval


def test_run_eval_smoke(tmp_path):
    report = run_eval("datasets/mvp_golden.jsonl", seed=1337, scorers=["em", "f1"], limit=2)
    assert "examples" in report
    assert len(report["examples"]) > 0
    assert "metrics" in report
