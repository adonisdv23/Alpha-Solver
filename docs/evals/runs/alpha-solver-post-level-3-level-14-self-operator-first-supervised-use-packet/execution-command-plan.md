# Execution command plan

The exact commands the execution lane will run, in order, from the
repository root of a clean checkout of `main`. **Nothing below was run by
this packet lane.** `$ROOT` is the output root from `output-root.md`.

## 1. Preconditions (read-only)

```bash
git fetch origin main
git status --short          # must be empty
python scripts/check_self_operator_release_gate.py --repo-root . \
  --output "$ROOT/checks/release-gate-check.json"   # must exit 0
```

## 2. Gate-and-record pipeline (wrapper classifies; it executes nothing)

With `inputs/approval-record.json` and `inputs/proposed-task.json` drafted
below `$ROOT` per `operator-confirmation-required.md`, where the proposed
task's `proposed_commands` contain only the literal command text
`python scripts/check_local_llm_packet_consistency.py`:

```bash
python - <<'PY'
import json
from pathlib import Path
from alpha.self_operator.dry_run import run_local_dry_run_wrapper

root = Path("$ROOT")  # substituted with the literal output root
task = json.loads((root / "inputs/proposed-task.json").read_text())
approval = json.loads((root / "inputs/approval-record.json").read_text())
result = run_local_dry_run_wrapper(task, approval, output_root=root)
print(result)
PY
```

Expected: `dry-run-result.json` and `execution-gate-result.json` below
`$ROOT`, gate status `allowed_for_local_dry_run_wrapper`, and no
`stop-state.json`. Any other outcome is a stop per `stop-state-rules.md`.

## 3. Supervised consistency review (deterministic, read-only)

```bash
python scripts/check_local_llm_packet_consistency.py \
  | tee "$ROOT/checks/consistency-check.stdout.txt"   # must exit 0
```

## 4. Post-run verification (read-only)

```bash
git status --short          # must still be empty: the run wrote nothing in-repo
```

Record every command, exit code, and UTC timestamp in
`$ROOT/checks/commands-run.txt`, and the supervision log in
`$ROOT/notes/operator-log.md`.

## Boundaries of this plan

- The wrapper call in step 2 classifies the proposed command text; the only
  command ever executed by a human-typed shell invocation is the
  deterministic read-only checker in steps 1 and 3.
- No step has network access requirements; every step is local-only.
- No step writes inside the repository; repository evidence is imported
  later, redacted, by the execution lane through lane review.
- If any step deviates from this plan, the run aborts per
  `abort-conditions.md`; the plan is not adjusted mid-run.
