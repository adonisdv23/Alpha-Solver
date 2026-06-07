# Safety invariant preservation

This decision preserves all hard invariants for the Prompt 3 contract.

## Preserved invariants

- High-risk findings continue to block `answer_with_assumptions`.
- Boundary fail-closed behavior remains unchanged.
- Failed-closed non-exposure remains unchanged.
- Diagnostics remain enum-only.
- No `/v1/solve` exposure is authorized.
- No dashboard exposure is authorized.
- No provider fallback is authorized.
- No hosted provider behavior change is authorized.
- No local model quality statement is made.
- No readiness, benchmark, MVP, production, superiority, billing, broad runtime readiness, or evidence-model claim is made.

## Prompt 3-specific preservation

When `missing_information_too_broad` fires for Prompt 3, the acceptable outcome remains `clarify`, with Pass 2 not called and model fields not exposed.
