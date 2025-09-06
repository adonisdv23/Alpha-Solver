import json
from pathlib import Path

from alpha.adapters import instruction_adapter
from alpha.executors import math_exec, csv_exec


def test_run_instruction_dispatch(tmp_path):
    math_res = instruction_adapter.run_instruction({
        "tool_id": math_exec.TOOL_ID,
        "action": "eval",
        "args": {"expr": "1+1"},
    })
    assert math_res["result"] == 2

    src = tmp_path / "input.csv"
    src.write_text("a\n1\n2\n", encoding="utf-8")
    csv_res = instruction_adapter.run_instruction({
        "tool_id": csv_exec.TOOL_ID,
        "action": "row_count",
        "args": {"path": str(src)},
    })
    assert csv_res["rows"] == 2


def test_trace_file_written(tmp_path):
    trace = Path("artifacts/exec/instructions.jsonl")
    if trace.exists():
        trace.unlink()
    instruction_adapter.run_instruction({
        "tool_id": math_exec.TOOL_ID,
        "action": "eval",
        "args": {"expr": "3+3"},
    })
    assert trace.exists()
    lines = trace.read_text(encoding="utf-8").strip().splitlines()
    assert lines and json.loads(lines[-1])["tool_id"] == math_exec.TOOL_ID
