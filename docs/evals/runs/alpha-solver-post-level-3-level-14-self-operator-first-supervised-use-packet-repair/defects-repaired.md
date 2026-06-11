# Defects repaired

Both defects lived in the merged
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet/execution-command-plan.md`.
Both were repaired and verified before any execution step ran.

## Defect 1: remote-fetch precondition in a local-only plan

- Defective text (step 1 of the plan): `git fetch origin main`
- Problem: the command can contact the remote, violating the plan's own
  boundary ("No step has network access requirements; every step is
  local-only") and the lane's local-only / no-network execution boundary.
- Risk class (runbook severity taxonomy): P1-class non-execution-safety
  risk had it been run; in fact it was never run — the defect was caught
  and repaired pre-run, so no boundary was violated.
- Repair: removed from the executable plan; replaced with local-only
  precondition checks (`git status --short` must be empty;
  `git rev-parse --verify HEAD` records the exact commit;
  `python scripts/check_self_operator_release_gate.py --repo-root .` with
  `--output "$ROOT/checks/release-gate-check.json"` must exit 0). The plan
  now states that merge/currency verification happens before the run begins,
  never via a network command inside the run, and `abort-conditions.md`
  pre-run condition 8 makes any remaining network-contacting command a hard
  stop.

## Defect 2: quoted heredoc relying on `Path("$ROOT")`

- Defective text (step 2 of the plan): `python - <<'PY'` with
  `root = Path("$ROOT")  # substituted with the literal output root`
- Problem: with a quoted heredoc delimiter, the shell performs no expansion
  inside the heredoc, so Python would receive the literal four characters
  `$ROOT` and resolve them to a `$ROOT` directory under the current working
  directory — an in-repo write and a wrong artifact root. The plan's comment
  ("substituted with the literal output root") relied on a manual edit step
  the plan never defined.
- Risk class (runbook severity taxonomy): P1/P2-class artifact-path safety
  risk had it been run (writes would have landed inside the repository
  checkout, itself an in-run abort condition); never run — caught and
  repaired pre-run.
- Repair: the output root is now passed through the shell environment
  before Python starts (`ROOT="$ROOT" python - <<'PY'`), and Python reads it
  via `os.environ["ROOT"]`. The repaired plan states explicitly that
  `$ROOT` is resolved by the shell environment before Python reads it
  through `os.environ["ROOT"]`. The quoted heredoc is retained only because
  it is paired with this environment-variable handoff; the block requires no
  shell expansion inside the heredoc and no longer contains `Path("$ROOT")`.
  A quoted heredoc that relies on `Path("$ROOT")` remains unsafe and is now
  a pre-run hard stop (`abort-conditions.md` condition 8).

## Repair scope

Only three files of the merged first-use packet were edited:
`execution-command-plan.md` (both repairs plus a dated repair record),
`abort-conditions.md` (pre-run hard-stop condition 8 for network access and
unresolved `$ROOT` expansion), and `checks-plan.md` (repair re-run record).
No other prior evidence was edited.
