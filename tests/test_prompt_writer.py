from pathlib import Path
from alpha.core import runner


def test_prompt_emission(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    plan = {
        "steps": [{"tool_id": "t", "prompt": "hi", "adapter": "openai"}],
        "breaker": {"trip_count": 10},
    }
    trace = runner.run(plan, execute=False)
    path = Path(trace[0]["prompt_path"])
    assert (path / "system.txt").exists()
    assert (path / "user.txt").exists()
    assert (path / "schema.json").exists()
    assert Path(plan["audit_log"]).exists()
