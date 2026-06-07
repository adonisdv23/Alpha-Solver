# Allowed CLI Boundary

## Future wrapper boundary

A future stable CLI wrapper, if implemented by the selected next lane, must remain:

- local-only;
- default-off;
- explicit opt-in;
- loopback endpoint only;
- finite timeout;
- `no_provider_keys_required=true`;
- `no_hosted_fallback=true`;
- no hosted fallback;
- `behavior_evidence=false`;
- no `/v1/solve` exposure;
- no dashboard exposure;
- no provider fallback;
- no evidence-model promotion.

## Allowed high-level behavior

A future wrapper may:

1. accept a user prompt from an explicit CLI argument, standard input, or a documented local file input;
2. accept explicit local runtime settings equivalent to the existing environment/config requirements, including enablement, endpoint URL, local model identifier, and finite timeout;
3. validate or delegate validation of localhost/loopback endpoint constraints to the existing local runtime config path;
4. call `alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration`;
5. print the normalized result as JSON;
6. exit non-zero for fail-closed configuration errors, invalid operator input, or malformed wrapper invocation while still preserving the result's non-evidence boundary where a result is produced;
7. include help text that clearly says the command is non-production, local-only, default-off, and not evidence promotion.

## Disallowed behavior

A future wrapper must not:

- mount or call production `/v1/solve`;
- mount or call dashboard preview or dashboard routes;
- add hosted provider fallback;
- accept hosted provider keys as local-mode requirements;
- race, route, or orchestrate across providers;
- label hosted output as local output;
- change runtime behavior in the orchestration runner or provider adapter except where the next lane explicitly authorizes wrapper wiring;
- modify the evidence model;
- claim local model quality, benchmark success, production readiness, MVP readiness, provider-orchestration evidence, Alpha superiority, billing evidence, broad runtime readiness, `/v1/solve` readiness, or dashboard readiness.
