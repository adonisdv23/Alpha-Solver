# Command plan after repair

Verbatim content of `execution-command-plan.md` after the repair (the
plan the execution portion of this lane actually followed). Step 1 is
local-only; step 2 passes the output root through the shell environment
(`ROOT="$ROOT"`) and Python reads it via `os.environ["ROOT"]`.

````markdown
# Execution command plan

The exact commands the execution lane will run, in order, from the
repository root of a clean checkout of `main`. **Nothing below was run by
this packet lane.** `$ROOT` is the output root from `output-root.md`.

## 1. Preconditions (read-only, local-only)

```bash
git status --short          # must be empty
git rev-parse --verify HEAD # records the exact local commit the run uses
python scripts/check_self_operator_release_gate.py --repo-root . \
  --output "$ROOT/checks/release-gate-check.json"   # must exit 0
```

No precondition contacts the network. That this packet is merged and the
checkout is current is verified by the execution lane before the run begins
(outside the run, during lane chartering), never by a network command inside
the run; any network access during the run is a hard stop per
`abort-conditions.md`.

## 2. Gate-and-record pipeline (wrapper classifies; it executes nothing)

With `inputs/approval-record.json` and `inputs/proposed-task.json` drafted
below `$ROOT` per `operator-confirmation-required.md`, where the proposed
task's `proposed_commands` contain only the literal command text
`python scripts/check_local_llm_packet_consistency.py`:

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

`$ROOT` is resolved by the shell environment before Python reads it: the
`ROOT="$ROOT"` prefix passes the already-expanded output root into the
process environment, and Python reads it through `os.environ["ROOT"]`. The
quoted heredoc is acceptable only because of this environment-variable
handoff: the block requires no shell expansion inside the heredoc and does
not use `Path("$ROOT")`. A quoted heredoc that relies on `Path("$ROOT")`
remains unsafe and blocked (`abort-conditions.md`).

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
- No step has network access requirements and no step contacts a remote;
  every step is local-only. The former remote-fetch precondition was removed
  by the command-plan repair lane (see below) because it violated this
  boundary.
- No step writes inside the repository; repository evidence is imported
  later, redacted, by the execution lane through lane review.
- If any step deviates from this plan, the run aborts per
  `abort-conditions.md`; the plan is not adjusted mid-run.

## Repair record (2026-06-11)

This plan was repaired before any execution by lane
`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-REPAIR-AND-EXECUTION-001`:
the step 1 remote-fetch precondition was replaced with local-only checks,
and the step 2 heredoc was changed to pass the output root through the
shell environment (read in Python via `os.environ["ROOT"]`) instead of
relying on unexpanded `Path("$ROOT")` text inside a quoted heredoc. The
defect record, before/after plans, and pre-execution verification live in
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet-repair/`.
Nothing was executed against this plan before the repair was verified.
````
