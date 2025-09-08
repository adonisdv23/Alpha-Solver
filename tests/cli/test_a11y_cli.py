import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def test_a11y_cli(tmp_path) -> None:
    inp = tmp_path / "events.jsonl"
    inp.write_text(json.dumps({"text": "Simple sentence."}) + "\n", encoding="utf-8")
    cmd = [sys.executable, "-m", "alpha.cli", "a11y-check", "--input", str(inp)]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    subprocess.check_call(cmd, cwd=tmp_path, env=env)
    summary_path = tmp_path / "artifacts" / "a11y" / "summary.json"
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    assert data["count"] == 1
