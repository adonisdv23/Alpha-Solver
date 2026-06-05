# Implementation Review Checklist

This is a scaffold only. Local LLM runtime integration is not implemented here.

A future implementation review must verify each item below before merge.

## Routing and exposure

- [ ] Local LLM runtime use is default-off unless explicitly configured.
- [ ] Routing does not silently switch to a hosted provider.
- [ ] `/v1/solve` is not exposed to local LLM mode until explicitly authorized.
- [ ] Dashboard preview is not exposed to local LLM mode until explicitly authorized.
- [ ] Local LLM mode requires no provider keys.

## Endpoint and timeout controls

- [ ] Local LLM mode accepts only localhost or loopback endpoints.
- [ ] Non-local endpoints fail closed.
- [ ] Malformed endpoints fail closed.
- [ ] Runtime calls use finite timeout values.
- [ ] Connection failures fail closed.
- [ ] Timeouts fail closed.

## Response and evidence controls

- [ ] Malformed responses fail closed.
- [ ] Empty outputs fail closed.
- [ ] Prompt echoes fail closed.
- [ ] System echoes fail closed.
- [ ] `behavior_evidence=false` remains preserved until a later lane explicitly changes the evidence model.
- [ ] Observability distinguishes local LLM from hosted providers.
- [ ] Raw artifacts are preserved for runtime smoke.

## Claim controls

- [ ] Runtime smoke was completed before any runtime-readiness claim.
- [ ] The implementation does not claim MVP validation, production readiness, benchmark evidence, provider-orchestration evidence, Alpha superiority evidence, `/v1/solve` readiness, or dashboard preview readiness unless separately authorized.
