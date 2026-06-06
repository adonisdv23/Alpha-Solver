# Final Decision

## Selected final decision

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_FAIL_REQUIRES_FIX`

## Why this decision was selected

The source artifact is present, complete, and interpretable. It records exit status `0`, five results, command provenance, script provenance, repo head, script checksum, loopback endpoint summary, model `qwen2.5:3b`, timeout `60`, `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.

However, the prompt results do not satisfy all expected smoke modes or outcomes:

- Prompt 1 expected `direct` but observed `clarify`.
- Prompt 2 expected `clarify` but observed `block`.
- Prompt 3 expected `answer_with_assumptions` but observed `block`.
- Prompt 4 expected `block` and observed `block`.
- Prompt 5 retained bounded `answer` and `final_answer`, but model-produced `considerations` and `assumptions` included forbidden readiness, validation, benchmark, provider-orchestration, `/v1/solve`, dashboard, production, and related evidence-promotion language.

## Decisions not selected

- `the narrow pass decision` was not selected because not all expected prompt modes or boundary outcomes passed.
- `the blocked-or-incomplete decision` was not selected because required artifacts and provenance are present and support interpretation.

## Decision boundary

This decision is only a final decision for one preserved manual local orchestration smoke artifact. It is not local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.
