# Runtime Smoke Runbook

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-OPERATOR-CONFIG-RUNBOOK-001`

This runbook is a future-use template only. No runtime smoke was executed in this lane. No local model was called. No hosted provider was called. No smoke result is imported.

Canonical contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Preconditions for a future smoke lane

A future operator must confirm all of the following before execution:

1. The local LLM runtime implementation PR has merged and is reviewed against `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.
2. The exact runtime configuration fields are documented.
3. Local LLM mode is default-off and requires explicit opt-in.
4. The endpoint is localhost or loopback only.
5. The local model name is intentionally selected and available.
6. The timeout is finite.
7. No hosted provider key is required for local mode.
8. No silent hosted fallback is enabled.
9. Artifact redaction rules are understood before capture.

## Historical context only

Previous local smoke context used endpoint pattern `http://127.0.0.1:11434/api/chat`, model `gemma3:4b`, and timeout `120`.

Those values are not automatic runtime configuration. Confirm all values against the future implementation before any smoke execution.

## Future smoke sequence template

1. Record implementation commit or PR reference.
2. Record exact config fields and values after redaction review.
3. Confirm local mode remains default-off without explicit opt-in.
4. Confirm explicit opt-in activates only local mode.
5. Confirm endpoint locality before execution.
6. Confirm local model availability.
7. Execute one bounded runtime smoke command using a finite timeout.
8. Capture stdout, stderr, exit code, start timestamp, end timestamp, and sanitized metadata.
9. Confirm `behavior_evidence=false` is preserved if applicable to the implemented artifact shape.
10. Confirm no hosted provider call occurred and no hosted output was substituted.
11. Classify the outcome without making readiness, quality, superiority, benchmark, production, MVP, provider-orchestration, or billing claims.

## Future command placeholder

Do not execute this placeholder in this lane.

```bash
<TBD-alpha-runtime-command> \
  --provider <TBD-local-provider-mode> \
  --local-endpoint <TBD-localhost-or-loopback-endpoint> \
  --local-model <TBD-local-model-name> \
  --timeout-seconds <TBD-finite-timeout> \
  --explicit-local-opt-in <TBD-value> \
  <TBD-smoke-input>
```

## Acceptance scope for future smoke

A future smoke may only support a narrow claim that the implemented local runtime path was invoked under the recorded configuration and produced the recorded bounded outcome.

A future smoke must not be interpreted as local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.
