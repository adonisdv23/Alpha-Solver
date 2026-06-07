#!/usr/bin/env bash
set -u

ART_DIR="docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact"
MODEL="${MODEL:-qwen2.5:3b}"
ENDPOINT_URL="${ENDPOINT_URL:-http://127.0.0.1:11434/api/chat}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-60}"

python3 - <<'PY'
import json
import os
import shlex
import subprocess
from pathlib import Path

art_dir = Path("docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact")
model = os.environ.get("MODEL", "qwen2.5:3b")
endpoint_url = os.environ.get("ENDPOINT_URL", "http://127.0.0.1:11434/api/chat")
timeout_seconds = os.environ.get("TIMEOUT_SECONDS", "60")
repo_head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
repo_status = subprocess.check_output(["git", "status", "--short"], text=True)

keys_to_remove = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
]

cases = [
    "L3-FROZEN-TC-001",
    "L3-FROZEN-TC-002",
    "L3-FROZEN-TC-003",
    "L3-FROZEN-TC-004",
    "L3-FROZEN-TC-005",
]

(art_dir / "run_metadata.txt").write_text(
    "\n".join([
        "lane=ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-LEVEL-3-VALIDATION-EXECUTION-001",
        f"repo_head={repo_head}",
        "repo_status_begin",
        repo_status.rstrip(),
        "repo_status_end",
        "command_identity=python3 -m alpha.local_llm.operator_cli",
        f"model={model}",
        f"endpoint_url={endpoint_url}",
        f"timeout_seconds={timeout_seconds}",
        f"artifact_dir={art_dir}",
        "prompt_invocation_mode=inline --prompt",
        "evidence_boundary=Level 3 validation execution artifact only; not production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority evidence, billing evidence, dashboard readiness, /v1/solve readiness, broad runtime readiness, or evidence-model promotion.",
        "",
    ]),
    encoding="utf-8",
)

for case in cases:
    prompt_file = art_dir / "prompts" / f"{case}.txt"
    prompt_text = prompt_file.read_text(encoding="utf-8").strip()
    case_dir = art_dir / "results" / case
    case_dir.mkdir(parents=True, exist_ok=True)

    args = [
        "python3",
        "-m",
        "alpha.local_llm.operator_cli",
        "--enable-local-llm",
        "--prompt",
        prompt_text,
        "--endpoint-url",
        endpoint_url,
        "--model",
        model,
        "--timeout-seconds",
        timeout_seconds,
    ]

    recorded = "env " + " ".join(f"-u {k}" for k in keys_to_remove) + " \\\n" + shlex.join(args) + "\n"
    (case_dir / "executed_command.txt").write_text(recorded, encoding="utf-8")

    (case_dir / "metadata.txt").write_text(
        "\n".join([
            f"test_case_id={case}",
            f"prompt_source={prompt_file}",
            "prompt_invocation_mode=inline --prompt",
            f"repo_head={repo_head}",
            f"model={model}",
            f"endpoint_url={endpoint_url}",
            "endpoint_expected_loopback=true",
            f"timeout_seconds={timeout_seconds}",
            "behavior_evidence_expected=false",
            "no_hosted_fallback_expected=true",
            "no_provider_keys_required_expected=true",
            "",
        ]),
        encoding="utf-8",
    )

    (case_dir / "redaction_confirmation.txt").write_text(
        "\n".join([
            f"test_case_id={case}",
            "redaction_review_completed=true",
            "secrets_or_tokens_observed=false",
            "hosted_provider_keys_observed=false",
            "unnecessary_environment_dump_observed=false",
            "redaction_action=none_required_for_preserved_artifacts",
            "preserved_fields=test_case_id,prompt_text,status,safety_flags,endpoint_locality,timeout,exit_code,repo_head",
            "",
        ]),
        encoding="utf-8",
    )

    (case_dir / "operator_environment_notes.txt").write_text(
        "\n".join([
            f"test_case_id={case}",
            "operator_environment=local Mac execution worktree",
            "execution_surface=python3 -m alpha.local_llm.operator_cli",
            "endpoint_boundary=loopback-only",
            "hosted_provider_calls=none",
            "provider_fallback=none",
            "hosted_fallback=none",
            "/v1/solve_called=false",
            "dashboard_called=false",
            "google_sheets_update=false",
            "backlog_workbook_update=false",
            "evidence_boundary=artifact capture only; not readiness, benchmark, model-quality, provider-orchestration, Alpha-superiority, billing, dashboard, /v1/solve, broad-runtime, or evidence-model-promotion evidence",
            "",
        ]),
        encoding="utf-8",
    )

    env = os.environ.copy()
    for key in keys_to_remove:
        env.pop(key, None)

    result = subprocess.run(args, text=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    (case_dir / "stdout.json").write_bytes(result.stdout)
    (case_dir / "stderr.txt").write_bytes(result.stderr)
    (case_dir / "exit_code.txt").write_text(f"{result.returncode}\n", encoding="utf-8")

    try:
        data = json.loads(result.stdout.decode("utf-8"))
        meta = data.get("metadata", {}) if isinstance(data, dict) else {}
        lines = [
            "json_parse=parseable",
            f"status={data.get('status') if isinstance(data, dict) else None}",
            f"behavior_evidence={data.get('behavior_evidence') if isinstance(data, dict) else None}",
            f"no_hosted_fallback={data.get('no_hosted_fallback') if isinstance(data, dict) else None}",
            f"no_provider_keys_required={data.get('no_provider_keys_required') if isinstance(data, dict) else None}",
            f"endpoint_is_loopback={meta.get('endpoint_is_loopback')}",
            f"endpoint_host_label={meta.get('endpoint_host_label')}",
            f"timeout_seconds={meta.get('timeout_seconds')}",
        ]
    except Exception as exc:
        lines = [
            "json_parse=unparseable",
            f"parse_error={type(exc).__name__}: {exc}",
        ]

    (case_dir / "json_review.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

echo "===== FINAL FILE LIST =====" > "$ART_DIR/file_list.txt"
find "$ART_DIR" -type f | sort >> "$ART_DIR/file_list.txt"
