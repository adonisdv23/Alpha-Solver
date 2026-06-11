# Checks run (repair portion)

Run on 2026-06-11 from the repo root on branch
`claude/eloquent-tesla-pmct3n` (created from `main` at `e04d4cc`, #479
merged), after the Step A repair edits and before any execution step.

```bash
git status --short
git diff --name-only
git diff --check
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet
```

Results:

- `git status --short` / `git diff --name-only`: changed files were exactly
  the three allowed first-use packet files (`execution-command-plan.md`,
  `abort-conditions.md`, `checks-plan.md`).
- `git diff --check`: no whitespace errors.
- Packet consistency check: passed (1 packet directory scanned).

Focused unsafe-pattern scan:

```bash
rg -n "git fetch|Path\(\"\$ROOT\"\)|<<'PY'" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet
```

Result: 6 hit lines; classification recorded in
`repair-verification-before-execution.md` — 1
`safe_quoted_heredoc_environment_root`, 4 `allowed_boundary_reference`, 1
`irrelevant_false_positive`, 0 `unsafe_executable_plan_pattern`.

Forbidden-claim scan cross-check: the repair edits introduce no new hit
lines for the first-use packet's recorded forbidden-claim scan pattern (the
packet total remains 32 hit lines with the same per-file distribution), so
the classification table in that packet's `checks-plan.md` remains its
final state.

The combined lane's required final checks (consistency over all three
packet directories plus the extended forbidden-claim and unsafe-pattern
scan) are recorded in the execution packet's `checks-run.md`
(`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-execution/`).
