# Checks run

Requested checks for this docs-only packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan`
- Confirm changed files are only under `docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan/`.

Results are recorded in the PR summary/final response after execution. These checks validate documentation packet consistency only and do not start implementation.

Additional required search check:

- `rg "READY_FOR_FIRST_CODE_STATIC_TEST_SCAFFOLD_PLANNING_ONLY|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-10-SELF-OPERATOR-STATIC-TEST-SCAFFOLD-IMPLEMENTATION-001|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-9-SELF-OPERATOR-MVP-IMPLEMENTATION-PLAN-FIX-001|does not implement Self Operator|no provider calls|no external API calls|no credentials|no browser automation|no deployment|no billing|no evidence promotion" docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-mvp-implementation-plan`
