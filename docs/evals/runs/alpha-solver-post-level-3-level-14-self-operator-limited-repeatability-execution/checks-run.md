# Checks run

- `git status --short`
- `git rev-parse --verify HEAD`
- `python scripts/check_self_operator_release_gate.py --repo-root . --output "$ROOT/checks/release-gate-check.json"`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet`
- `rg -n "git fetch|Path\(\"\$ROOT\"\)" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet/execution-command-plan.md`
- `ROOT="$ROOT" python - <<'PY' ... run_local_dry_run_wrapper ... PY`
- `python scripts/check_local_llm_packet_consistency.py`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet`
- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-execution`
- Focused consistency-output verification `rg` command.
- Forbidden-claim and unsafe-pattern scan `rg` command.

## Final scan classification

All forbidden-claim and unsafe-pattern scan hits were reviewed and classified as `allowed_boundary_reference`. No hit was classified as `forbidden_claim` or `unsafe_executable_plan_pattern`.
