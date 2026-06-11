# Checks plan

## Checks required for this packet lane

This packet lane must run:

```bash
git status --short
git diff --name-only
git diff --check
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model|git fetch|Path\\(\"\\$ROOT\"\\)" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet
```

Every scan hit must be reviewed and classified as one of:

- `allowed_boundary_reference`;
- `forbidden_claim`;
- `irrelevant_false_positive`;
- `unsafe_executable_plan_pattern`.

If any `forbidden_claim` or `unsafe_executable_plan_pattern` remains, this lane
is blocked.

## Checks required for the future execution lane

A future repeatability execution lane must run at least:

```bash
git status --short
git rev-parse --verify HEAD
python scripts/check_self_operator_release_gate.py --repo-root . --output "$ROOT/checks/release-gate-check.json"
python scripts/check_local_llm_packet_consistency.py
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet
git status --short
```

The future lane must also run the same forbidden-claim and unsafe-pattern scan
against its own execution evidence packet before selecting any next lane.
