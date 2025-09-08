from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Compute the repository root without resolving symlinks
ROOT = Path(__file__).parent.parent


def _run(code: str) -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    cmd = [sys.executable, "-c", code]
    return subprocess.check_output(cmd, env=env, text=True)


def test_quality_gate_cli_imports_alpha() -> None:
    out = _run("import alpha.core.config as c; print(c.__name__)")
    assert out.strip() == "alpha.core.config"
