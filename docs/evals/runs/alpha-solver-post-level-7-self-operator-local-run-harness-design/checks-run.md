# Checks Run

Checks for this packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-local-run-harness-design`
- `rg "no provider calls|no hosted model calls|no external API calls|no fallback|no credential use|no billing|no dashboard exposure|no /v1/solve exposure|NO_FURTHER_SELF_OPERATOR_LOCAL_RUN_HARNESS_DESIGN_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-LOCAL-RUN-HARNESS-DESIGN-FIX-001" docs/evals/runs/alpha-solver-post-level-7-self-operator-local-run-harness-design`

The final command outputs are recorded in the PR summary rather than embedded here to avoid treating command logs as authoritative packet decisions.
