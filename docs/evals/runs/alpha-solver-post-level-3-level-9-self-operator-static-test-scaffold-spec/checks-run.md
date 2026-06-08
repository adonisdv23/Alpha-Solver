# Checks run

Requested checks for this docs-only packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-static-test-scaffold-spec`
- Confirm changed files are only under `docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-static-test-scaffold-spec/`.

Results are recorded in the PR summary/final response after execution. These checks validate documentation packet consistency only and do not start implementation.

Additional required search check:

- `rg "SELF_OPERATOR_PROVIDER_CALL_BLOCKED|SELF_OPERATOR_FALLBACK_BLOCKED|SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED|SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED|NO_FURTHER_LEVEL_9_SELF_OPERATOR_STATIC_TEST_SCAFFOLD_SPEC_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-9-SELF-OPERATOR-STATIC-TEST-SCAFFOLD-SPEC-FIX-001" docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-static-test-scaffold-spec`
