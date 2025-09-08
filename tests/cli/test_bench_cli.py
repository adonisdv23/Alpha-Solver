import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def test_bench_cli(tmp_path) -> None:
    root = ROOT
    out_dir = root / "bench_out"
    if out_dir.exists():
        for p in out_dir.iterdir():
            p.unlink()
    cmd = [sys.executable, "-m", "alpha.cli", "bench", "--quick"]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    subprocess.check_call(cmd, cwd=tmp_path, env=env)
    assert (out_dir / "bench.csv").exists()
    assert (out_dir / "bench.json").exists()
