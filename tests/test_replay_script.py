from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_replay_script(tmp_path, monkeypatch):
    plan = {"seed": 42}
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    script = Path(__file__).resolve().parents[1] / "scripts" / "replay.py"
    subprocess.run([sys.executable, str(script), "--plan", str(plan_path)], check=True)

    out_dir = tmp_path / "artifacts" / "replay"
    runs = list(out_dir.glob("run_*"))
    assert runs
    assert (runs[0] / "replay.json").exists()
