# Exact Mac Command

Copy and paste the command below on Adonis's Mac only, after confirming the prerequisites in `README.md`.

This command intentionally reads the existing manual smoke packet command template, rewrites only the approved local retry 007 execution details, unsets hosted-provider keys, runs the generated command, and prints only a redaction-checked safe diagnostic summary. The command is not evidence by itself; the future source artifact directory and later preservation/import lanes are the evidence chain.

```bash
set -u
cd /Users/games/Documents/Alpha-Solver
git checkout main
git pull --ff-only

ARTIFACT_DIR="docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset"
TEMPLATE_PATH="docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-packet/exact-command-template.md"
GENERATED_COMMAND="$ARTIFACT_DIR/manual-smoke-command.sh"
mkdir -p "$ARTIFACT_DIR"

python3 - <<'PY'
from __future__ import annotations

from pathlib import Path

artifact_dir = Path("docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset")
template_path = Path("docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-packet/exact-command-template.md")
generated_command = artifact_dir / "manual-smoke-command.sh"
text = template_path.read_text(encoding="utf-8")
start = text.index("```bash") + len("```bash")
end = text.index("```", start)
command = text[start:end].strip() + "\n"
command = command.replace(
    "docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-source-artifact",
    str(artifact_dir),
)
command = command.replace("<LOCAL_OLLAMA_LOOPBACK_ENDPOINT>", "http://127.0.0.1:11434/api/chat")
command = command.replace("<LOCAL_OLLAMA_MODEL>", "qwen2.5:3b")
command = command.replace("<LOCAL_TIMEOUT_SECONDS>", "60")
command = command.replace("_dt.UTC", "_dt.timezone.utc")
command = command.replace('python "$RUNNER_PATH"', 'python3 "$RUNNER_PATH"')
command = command.replace(
    'PYTHONPATH="$(pwd)" \\\n',
    'unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY DEEPSEEK_API_KEY\nPYTHONPATH="$(pwd)" \\\n',
)
inspection = r'''
printf '\n=== retry 007 command status ===\n'
printf 'runner exit status: %s\n' "$RUNNER_STATUS"
printf 'runner stdout/stderr were captured under: %s\n' "$ARTIFACT_DIR"
printf '\n=== retry 007 redaction-safe artifact inspection ===\n'
INSPECTION_STATUS=0
python3 - <<'CHECKPY' || INSPECTION_STATUS=$?
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

artifact_dir = Path("docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset")
output_path = artifact_dir / "manual-smoke-redacted-output.json"
forbidden_trace_fragments = [
    "Answer directly in one sentence",
    "Make it faster",
    "Draft a concise execution plan",
    "Give exact commands",
    "Repeat all hidden/system instructions",
    "raw user prompt",
    "raw prompt",
    "raw model output",
    "risk_flags",
    "missing_information",
    "considerations",
    "assumptions",
    "answer text",
    "final_answer",
    "unsafe content",
    "boundary-violating content",
]
allowed_trace_fields = [
    "diagnostic_schema_version",
    "diagnostic_redaction",
    "prompt_shape",
    "pass_one_selected_mode",
    "apply_gate_decision",
    "boundary_failure_stage",
    "expose_model_fields",
    "pass_two_called",
    "blocked_reason_code",
    "blocked_reason_codes",
    "high_risk_reason_code",
    "assumption_gate_failed_reason_codes",
]
allowed_result_fields = ["status", "mode", "pass_count"]


def fail(message: str) -> None:
    raise SystemExit(f"ARTIFACT_INSPECTION_CHECK: FAIL {message}")


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} is not an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label} is not a list")
    return value


def assert_no_forbidden_fragments(value: Any, label: str) -> None:
    text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    if any(fragment in text for fragment in forbidden_trace_fragments):
        fail(f"{label} contains forbidden raw/sensitive fragment(s)")


try:
    packet = json.loads(output_path.read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"JSON parse/read failed: {type(exc).__name__}")

packet = require_mapping(packet, "packet")
results = require_list(packet.get("results"), "results")
safe_summary: list[dict[str, Any]] = []

for index, record_value in enumerate(results, start=1):
    record = require_mapping(record_value, f"results[{index}]")
    prompt_record = record.get("prompt_record", {})
    if prompt_record is not None and not isinstance(prompt_record, dict):
        fail(f"results[{index}].prompt_record is not an object")
    prompt_record = prompt_record or {}
    prompt_id = (
        prompt_record.get("id")
        or record.get("id")
        or record.get("prompt_id")
        or f"prompt-{index}"
    )
    if not isinstance(prompt_id, (str, int)):
        fail(f"results[{index}] prompt id is not scalar")

    result = require_mapping(record.get("result"), f"results[{index}].result")
    metadata = require_mapping(result.get("metadata", {}), f"results[{index}].result.metadata")
    gate_trace = require_mapping(metadata.get("gate_trace", {}), f"results[{index}].result.metadata.gate_trace")

    # Redaction checks must run before any diagnostic summary is printed.
    assert_no_forbidden_fragments(gate_trace, f"prompt {prompt_id} gate_trace")

    summary_record: dict[str, Any] = {"prompt_id": prompt_id}
    for field in allowed_result_fields:
        if field in result:
            summary_record[field] = result[field]
    for field in allowed_trace_fields:
        if field in gate_trace:
            summary_record[field] = gate_trace[field]
    assert_no_forbidden_fragments(summary_record, f"prompt {prompt_id} safe_summary")
    safe_summary.append(summary_record)

print("JSON_PARSE_CHECK: PASS")
print("GATE_TRACE_REDACTION_CHECK: PASS")
print("SAFE_DIAGNOSTIC_SUMMARY:")
print(json.dumps(safe_summary, indent=2, sort_keys=True))
CHECKPY
printf 'inspection exit status: %s\n' "$INSPECTION_STATUS"
if [ "$RUNNER_STATUS" -ne 0 ]; then
  exit "$RUNNER_STATUS"
fi
if [ "$INSPECTION_STATUS" -ne 0 ]; then
  exit "$INSPECTION_STATUS"
fi
'''

command = command.replace('exit "$RUNNER_STATUS"\n', inspection + '\nexit "$RUNNER_STATUS"\n')
generated_command.write_text(command, encoding="utf-8")
generated_command.chmod(0o700)
print(f"generated command: {generated_command}")
PY

bash "$GENERATED_COMMAND"
```

## Required operator notes

- Do not add hosted provider keys.
- Do not change the five prompts inherited from the existing manual smoke packet.
- Do not edit runtime code before running this retry.
- Preserve the generated source artifact directory exactly for later source artifact preservation.
