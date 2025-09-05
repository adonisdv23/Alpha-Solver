import time

from alpha.core.benchmark import benchmark


def test_benchmark(tmp_path):
    def fn(q: str) -> None:
        time.sleep(0.01)
    summary = benchmark(fn, ["a", "b"], out_dir=tmp_path)
    assert summary["count"] == 2
    assert (tmp_path / "benchmark.json").exists()
