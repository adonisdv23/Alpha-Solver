from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_bench(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    script = Path(__file__).resolve().parents[1] / "scripts" / "bench.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--queries",
            "test",
            "--regions",
            "US",
            "--repeat",
            "1",
        ],
        check=True,
    )
    out_dir = tmp_path / "artifacts" / "bench"
    files = list(out_dir.glob("bench_*.csv"))
    assert files
    content = files[0].read_text(encoding="utf-8")
    assert "query,region,repeat,duration_ms,maxrss_kb" in content.splitlines()[0]
