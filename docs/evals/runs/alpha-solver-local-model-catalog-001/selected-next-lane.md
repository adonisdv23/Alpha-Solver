# Selected Next Lane

Selected next lane: `ALPHA-SOLVER-LOCAL-MULTI-MODEL-SMOKE-HARNESS-001`

## Purpose

Build a local-only, default-off, multi-model smoke harness that can iterate over operator-specified Ollama model names through the existing loopback-only adapter path.

## Recommended scope

- Accept an explicit list of local model names.
- Require `ALPHA_LOCAL_LLM_ENABLED=true` or an equivalent operator-only flag.
- Reuse loopback endpoint validation and finite timeout validation.
- Use no hosted-provider keys and no hosted fallback.
- Run a tiny fixed prompt set with serial execution first.
- Store normalized non-promotional artifacts with model identifiers, statuses, reasons, and boundary labels.
- Preserve `behavior_evidence=False` unless a later approved evidence lane defines stronger criteria.

## Out of scope for next lane

- Production routing.
- Dashboard or `/v1/solve` exposure.
- Paid-provider calls.
- Benchmark claims.
- Model superiority claims.
