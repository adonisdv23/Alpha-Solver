# Source Evidence Reviewed

## Reviewed sources

- Repo-level `AGENTS.md` instructions for narrow scope, spec-first behavior changes, source-of-truth hierarchy, and validation expectations.
- Existing docs-only Self Operator planning packet patterns under `docs/evals/runs/alpha-solver-post-level-7-self-operator-*`.
- `scripts/check_local_llm_packet_consistency.py` packet consistency expectations for selected-next state, blocker fallback, and boundary files.
- `docs/local_llm_solver_orchestration_guardrails/checker-inventory.md` guardrail inventory context for local LLM orchestration packets.

## Evidence boundary

This review is limited to repository documentation and checker behavior. It does not review, execute, or validate a Self Operator implementation.

## Drafting implication

All prompt text is conditional future-use drafting only. A future Codex lane must re-inspect current specs, source files, tests, and authorization state before making any code change.
