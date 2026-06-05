# Implementation Review Checklist

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

This is a scaffold only. Local LLM runtime integration is not implemented here.

Future implementation review must check:

- [ ] Local LLM runtime use is default-off unless explicitly configured.
- [ ] Local LLM mode accepts only localhost / loopback endpoints.
- [ ] Non-local and malformed endpoints fail closed before any model call.
- [ ] No provider keys are required, loaded, exposed, or used for local LLM mode.
- [ ] Routing does not silently switch to a hosted provider.
- [ ] Hosted provider fallback is absent unless separately authorized.
- [ ] Finite timeout is configured for local runtime calls.
- [ ] Connection failure fails closed.
- [ ] Timeout fails closed.
- [ ] Malformed response fails closed.
- [ ] Empty output fails closed.
- [ ] Prompt echo fails closed.
- [ ] System echo fails closed.
- [ ] `/v1/solve` is not exposed to local LLM mode until explicitly authorized.
- [ ] Dashboard preview is not exposed to local LLM mode until explicitly authorized.
- [ ] Observability distinguishes local LLM from hosted providers.
- [ ] Raw artifacts are preserved for runtime smoke.
- [ ] `behavior_evidence=false` remains preserved until a later lane explicitly changes the evidence model.
