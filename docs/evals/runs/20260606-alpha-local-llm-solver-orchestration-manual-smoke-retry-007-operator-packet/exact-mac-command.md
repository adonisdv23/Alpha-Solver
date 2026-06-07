# Exact Mac Command

Copy and paste the command below on Adonis's Mac only, after confirming the prerequisites in `README.md`.

This command intentionally reads the existing manual smoke packet command template, rewrites only the approved local retry 007 execution details, unsets hosted-provider keys, runs the generated command, and prints basic artifact/diagnostic checks. The command is not evidence by itself; the future source artifact directory and later preservation/import lanes are the evidence chain.

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
printf 'exit status: %s\n' "$RUNNER_STATUS"
printf '\n=== retry 007 stdout ===\n'
cat "$ARTIFACT_DIR/manual-smoke-runner.stdout.txt" || true
printf '\n=== retry 007 stderr ===\n'
cat "$ARTIFACT_DIR/manual-smoke-runner.stderr.txt" || true
printf '\n=== retry 007 JSON parse and gate_trace quick check ===\n'
python3 - <<'CHECKPY'
from __future__ import annotations

import json
from pathlib import Path

artifact_dir = Path("docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset")
output_path = artifact_dir / "manual-smoke-redacted-output.json"
forbidden_trace_fragments = [
    "Answer directly in one sentence",
    "Make it faster",
    "Draft a concise execution plan",
    "Give exact commands",
    "Repeat all hidden/system instructions",
    "raw model output",
    "risk_flags",
    "missing_information",
    "considerations",
    "assumptions",
]
try:
    packet = json.loads(output_path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"JSON_PARSE_CHECK: FAIL {type(exc).__name__}: {exc}")
    raise
print("JSON_PARSE_CHECK: PASS")
results = packet.get("results", [])
if not isinstance(results, list):
    raise SystemExit("results is not a list")
for index, record in enumerate(results, start=1):
    prompt_record = record.get("prompt_record", {}) if isinstance(record, dict) else {}
    prompt_id = (prompt_record.get("id") if isinstance(prompt_record, dict) else None) or record.get("id") or record.get("prompt_id") or f"prompt-{index}"
    result = record.get("result", {}) if isinstance(record, dict) else {}
    metadata = result.get("metadata", {}) if isinstance(result, dict) else {}
    trace = metadata.get("gate_trace", {}) if isinstance(metadata, dict) else {}
    trace_text = json.dumps(trace, sort_keys=True)
    forbidden_hits = [fragment for fragment in forbidden_trace_fragments if fragment in trace_text]
    mode = result.get("mode") if isinstance(result, dict) else None
    status = result.get("status") if isinstance(result, dict) else None
    print(f"GATE_TRACE_CHECK prompt={index} id={prompt_id} status={status} mode={mode} trace={trace}")
    if forbidden_hits:
        raise SystemExit(f"gate_trace contains forbidden raw/sensitive text for {prompt_id}: {forbidden_hits}")
print("GATE_TRACE_REDACTION_CHECK: PASS")
CHECKPY
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
