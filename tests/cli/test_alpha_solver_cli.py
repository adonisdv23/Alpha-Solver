import json
import subprocess
import sys


def test_flags_smoke():
    out = subprocess.check_output([
        sys.executable,
        "alpha_solver_cli.py",
        "demo",
        "--multi-branch",
        "--max-width",
        "2",
        "--max-nodes",
        "5",
        "--enable-progressive-router",
        "--router-escalation",
        "basic,structured,constrained",
        "--low-conf-threshold",
        "0.5",
        "--no-cot-fallback",
    ])
    env = json.loads(out)
    cfg = env["diagnostics"]["tot"]["config"]
    assert cfg["multi_branch"] == 1
    assert cfg["max_width"] == 2
    assert cfg["max_nodes"] == 5
    assert env["diagnostics"]["router"]["stage"]
    assert env["diagnostics"]["safe_out"]["enable_cot_fallback"] is False
