import json, tempfile, os
from scripts.telemetry_tools import write_run_header, sha1_query

def test_header_and_query_hash():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "telemetry.jsonl")
        run_id = write_run_header(p, regions=["US","EU"], queries_source="tests")
        assert len(run_id) > 10
        first = json.loads(open(p,"r",encoding="utf-8").read().splitlines()[0])
        assert first["type"] == "run_header"
        assert first["run_id"] == run_id
        h = sha1_query("  Zapier   automation ")
        assert len(h) == 40
