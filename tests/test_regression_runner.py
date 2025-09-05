from alpha.core.regression import run_regression


def test_regression_runner(tmp_path):
    summary = run_regression("tests/regression", tmp_path / "summary.json")
    assert summary["total"] == 10
    assert summary["failed"] == 0
