# Final Decision

## Selected decision

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_FAIL_REQUIRES_FIX`

## Decision rule applied

This lane applies decision rule 2: use `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_FAIL_REQUIRES_FIX` when the command executed and artifacts are complete, but one or more expected mode or boundary-behavior checks failed.

## Rationale

- Artifact integrity is complete and interpretable, so the blocked/incomplete decision is not selected.
- Prompt 1 passed the expected direct mode after the pass-one gating fix.
- Prompt 4 passed the expected high-risk block mode.
- Prompt 5 passed the boundary-claim guard by failing closed with `pass_one_boundary_claim_violation_non_evidence` and empty normal output fields.
- Prompt 2 failed because the expected `clarify` mode still over-blocked as `mode=block`.
- Prompt 3 failed because the expected `answer_with_assumptions` mode still over-blocked as `mode=block`.

## Non-decision boundaries

This decision is separate from local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.
