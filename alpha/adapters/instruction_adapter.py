"""Instruction adapter for local executors."""
import json
from pathlib import Path
from typing import Any, Dict

from alpha.executors import math_exec, csv_exec

_TRACE_PATH = Path("artifacts/exec/instructions.jsonl")


def _log(record: Dict[str, Any]) -> None:
    _TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_TRACE_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def run_instruction(instr: Dict[str, Any]) -> Dict[str, Any]:
    tool_id = instr.get("tool_id")
    action = instr.get("action")
    args = instr.get("args", {})

    if tool_id == math_exec.TOOL_ID:
        result = math_exec.evaluate(args.get("expr", ""))
    elif tool_id == csv_exec.TOOL_ID:
        if action == "row_count":
            result = csv_exec.row_count(args.get("path", ""))
        elif action == "filter_rows":
            result = csv_exec.filter_rows(
                args.get("path", ""),
                args.get("col", ""),
                args.get("value", ""),
                args.get("out_path", "output.csv"),
            )
        else:
            result = {"ok": False, "error": "unsupported action"}
    else:
        result = {"ok": False, "error": "unsupported tool"}

    out = {"tool_id": tool_id, "action": action, **result}
    _log(out)
    return out
