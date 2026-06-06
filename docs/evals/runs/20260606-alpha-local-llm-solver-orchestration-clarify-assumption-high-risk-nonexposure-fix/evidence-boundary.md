# Evidence Boundary

This PR is a narrow implementation fix plus focused fake-transport tests for clarify gating, answer-with-assumptions gating, and high-risk non-exposure.

It is not:

- manual smoke execution;
- runtime smoke evidence;
- local model quality evidence;
- hosted provider evidence;
- `/v1/solve` readiness;
- dashboard readiness;
- MVP validation;
- production readiness;
- benchmark evidence;
- provider orchestration evidence;
- Alpha superiority evidence;
- evidence-model promotion;
- broad runtime readiness evidence;
- billing evidence.

Local-only invariants remain preserved: default-off local LLM mode, explicit local opt-in, loopback endpoint enforcement, no provider keys required, finite timeout, no hosted fallback, `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.
