from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class ScenarioResult:
    name: str
    passed: bool


def run_regression(scenarios_dir: str | Path = "tests/regression", out_path: str | Path = "artifacts/regression_summary.json") -> Dict[str, int]:
    scenarios_path = Path(scenarios_dir)
    results: List[ScenarioResult] = []
    for f in sorted(scenarios_path.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        passed = data.get("input") == data.get("expected")
        results.append(ScenarioResult(name=f.stem, passed=passed))
    summary = {
        "total": len(results),
        "passed": sum(r.passed for r in results),
        "failed": sum(not r.passed for r in results),
    }
    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with out_p.open("w", encoding="utf-8") as f:
        json.dump({"results": [r.__dict__ for r in results], **summary}, f, indent=2)
    return summary


if __name__ == "__main__":  # pragma: no cover
    run_regression()
