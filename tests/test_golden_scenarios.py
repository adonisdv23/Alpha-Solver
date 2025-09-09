import json
import shutil
from pathlib import Path

import pytest

from alpha.core import runner


def _normalize(path: Path) -> dict:
    data = json.loads(path.read_text())
    data["run_id"] = "RUN_ID"
    data["created_at"] = "TS"
    return data


@pytest.mark.parametrize("query,region", [("demo query", "US")])
def test_plan_only_golden(tmp_path, query, region):
    shutil.rmtree(Path("artifacts"), ignore_errors=True)
    runner.run_cli(queries=[query], regions=[region], seed=1234, topk=1, mode="plan-only")
    plan = _normalize(Path("artifacts/last_plan.json"))
    golden = json.loads((Path("tests/golden/tiny_plan.json")).read_text())
    assert plan == golden
