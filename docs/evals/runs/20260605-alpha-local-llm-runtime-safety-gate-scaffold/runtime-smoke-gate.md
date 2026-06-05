# Runtime Smoke Gate

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Smoke-before-readiness rule

Runtime smoke is required before any local LLM runtime-readiness claim. A future implementation cannot claim runtime readiness based on this scaffold.

## Minimum future smoke expectations

A future runtime smoke lane must preserve raw artifacts and must check, at minimum, that:

- local LLM mode was explicitly configured;
- the endpoint was localhost or loopback only;
- no hosted provider fallback occurred;
- no provider keys were required for local LLM mode;
- finite timeout behavior was exercised or verified;
- malformed, empty, prompt-echo, and system-echo response handling was evaluated according to the authorized smoke plan;
- `behavior_evidence=false` remained preserved unless a later lane explicitly changed the evidence model.

## No smoke in this lane

This lane does not run a model, does not call Ollama, does not call hosted providers, does not make network calls, and does not create runtime evidence.
