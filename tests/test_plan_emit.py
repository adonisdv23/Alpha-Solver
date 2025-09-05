import json
from pathlib import Path

import jsonschema

from alpha.core import loader, orchestrator
from alpha.core.paths import write_json_atomic


def test_plan_emit(tmp_path):
    loader.load_all('registries')
    shortlist = [{"id": "demo_tool", "prompt": "hi"}]
    plan = orchestrator.build_plan("hello", "US", 1, shortlist, None)
    plan.artifacts["plan_path"] = str(tmp_path / "plan.json")
    plan.artifacts["shortlist_snapshot"] = str(tmp_path / "shortlist.json")
    write_json_atomic(plan.artifacts["plan_path"], plan.to_dict())
    schema = json.loads(Path('schemas/plan.schema.json').read_text())
    jsonschema.validate(plan.to_dict(), schema)
    assert Path(plan.artifacts["plan_path"]).is_file()
