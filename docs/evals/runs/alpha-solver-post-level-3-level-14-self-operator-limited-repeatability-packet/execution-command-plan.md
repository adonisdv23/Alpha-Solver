# Execution command plan

This is the guarded command plan for a future repeatability execution lane. This
packet did not run the plan.

The future lane must set a fresh output root before using the commands below:

```bash
RUN_ID="self-operator-limited-repeatability-001-run-YYYYMMDDTHHMMSSZ"
ROOT="/tmp/alpha-solver-self-operator-limited-repeatability/${RUN_ID}"
mkdir -p "$ROOT/inputs" "$ROOT/checks" "$ROOT/notes"
```

## 0. Mandatory pre-execution plan verification

Before step 1, create and pass
`repeatability_plan_verification_before_execution.md` and
`$ROOT/inputs/repeatability-plan-verification.json` with these fields:

```text
plan_status: pass
git_fetch_absent_from_executable_plan: yes
root_expansion_safe: yes
unsafe_pattern_scan_status: pass
packet_consistency_status: pass
execution_allowed_after_plan_verification: yes
```

If any field differs, do not continue.

## 1. Preconditions

```bash
git status --short | tee "$ROOT/checks/git-status-before.txt"
git rev-parse --verify HEAD | tee "$ROOT/checks/head.txt"
python scripts/check_self_operator_release_gate.py --repo-root . \
  --output "$ROOT/checks/release-gate-check.json"
```

`git-status-before.txt` must show no tracked or untracked changes caused by the
future execution lane.

## 2. Draft approved inputs

Draft `inputs/approval-record.json`, `inputs/proposed-task.json`, and
`inputs/source-evidence-index.json` under the output root from the exact target,
operator confirmation, and input-artifact rules in this packet.

## 3. Gate-and-record pipeline

The wrapper classifies proposed command text. It must not execute the proposed
command text.

```bash
ROOT="$ROOT" python - <<'PY'
import json
import os
from pathlib import Path
from alpha.self_operator.dry_run import run_local_dry_run_wrapper

root = Path(os.environ["ROOT"])
task = json.loads((root / "inputs/proposed-task.json").read_text())
approval = json.loads((root / "inputs/approval-record.json").read_text())
result = run_local_dry_run_wrapper(task, approval, output_root=root)
print(result)
PY
```

The quoted heredoc is safe only because the output root is handed to Python
through the environment and Python reads `os.environ["ROOT"]`.

## 4. Supervised consistency review

```bash
python scripts/check_local_llm_packet_consistency.py \
  | tee "$ROOT/checks/consistency-check.stdout.txt"
```

## 5. Post-run local verification

```bash
git status --short | tee "$ROOT/checks/git-status-after.txt"
```

Record commands, exit codes, and UTC timestamps in
`$ROOT/checks/commands-run.txt`. Record operator observations in
`$ROOT/notes/operator-log.md`.

## Safeguards

- The executable plan contains no in-run remote update command.
- The executable plan does not use unsafe root literal handling.
- The wrapper step classifies only; it does not run the proposed command text.
- The supervised command remains the deterministic local packet consistency
  checker.
- Any deviation is terminal under `stop-state-rules.md` and
  `abort-conditions.md`.
