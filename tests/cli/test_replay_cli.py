import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from alpha.core.replay import ReplayHarness


def test_replay_cli(tmp_path) -> None:
    base = tmp_path / "artifacts" / "replays"
    harness = ReplayHarness(base)
    harness.record({"text": "hello"})
    sid = harness.save("sess1")

    cmd = [sys.executable, "-m", "alpha.cli", "replay", "--session", sid]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    out = subprocess.check_output(cmd, cwd=tmp_path, env=env, text=True)
    line = json.loads(out.strip().splitlines()[0])
    assert line["text"] == "hello"
