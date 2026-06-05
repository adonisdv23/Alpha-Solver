# Scaffold Preservation Checklist

Use this checklist when reviewing this scaffold or a future lane that consumes it.

- [ ] Changes remain docs-only under `docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-packet-scaffold/`.
- [ ] Runtime smoke is not executed in this lane.
- [ ] Runtime implementation is described as absent unless a future implementation PR creates it.
- [ ] Future implementation PR merge is required before smoke.
- [ ] Future review gate authorization is required before smoke.
- [ ] Localhost or loopback-only endpoint is required.
- [ ] Exact local model name is required.
- [ ] Finite timeout is required.
- [ ] Hosted provider fallback is forbidden.
- [ ] Provider keys are not required for local mode.
- [ ] Raw artifact preservation is required.
- [ ] Sanitized import after execution is required.
- [ ] No smoke result is imported in this scaffold.
- [ ] `behavior_evidence=false` is preserved unless a later lane explicitly changes the evidence model.
- [ ] Exactly one selected next lane is recorded.
- [ ] Evidence-boundary language remains narrow.
