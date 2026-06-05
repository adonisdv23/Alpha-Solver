# Fallback Policy Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Default fallback policy

Hosted-provider fallback from local LLM mode is prohibited.

## Hybrid-specific fallback requirement

Because the selected backend strategy is `hybrid`, provider selection must be explicit. Hybrid must not be implemented as silent fallback from one provider class to another.

## Local failure behavior

When local LLM mode is selected and any local failure occurs, the failure must remain local and visible. Connection failures, timeouts, malformed responses, empty outputs, prompt echoes, and system echoes must not trigger hosted-provider output.

## Future fallback authorization

If a later lane authorizes fallback, that future authorization must define:

- operator opt-in for fallback;
- exact fallback trigger conditions;
- hosted-provider key requirements for the fallback path;
- provenance labels that identify fallback output as hosted output;
- tests proving fallback is explicit and not silent.

No such fallback is authorized by this specification package.
