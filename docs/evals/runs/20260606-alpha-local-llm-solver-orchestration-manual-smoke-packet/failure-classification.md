# Failure Classification

Use the first applicable classification when interpreting future authorized manual smoke.

## Gate and setup failures

- `implementation missing`: target import or callable is unavailable.
- `review gate not authorized`: authorization phrase `AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE` is absent.
- `config missing`: required local enablement, endpoint, model, or timeout configuration is missing.
- `endpoint not local`: endpoint is not localhost or loopback.
- `model unavailable`: local model is not available from the local runtime.
- `timeout`: runtime exceeds finite timeout.

## Response-shape failures

- `malformed response`: runtime response cannot be parsed or normalized safely.
- `empty output`: local response is empty or whitespace-only.
- `prompt echo`: output echoes the user prompt.
- `system echo`: output echoes system/developer/hidden instructions.
- `pass-one parse failure`: first pass cannot be parsed into bounded gate inputs.
- `pass-two answer failure`: second pass fails or cannot produce a bounded answer.
- `confidence unavailable`: confidence is absent, non-numeric, or unusable where needed.
- `incorrect mode selection`: observed mode does not match expected mode/outcome for the prompt.

## Boundary and safety failures

- `forbidden positive boundary claim`: output claims readiness, validation, benchmark evidence, provider orchestration evidence, Alpha superiority, evidence-model promotion, or similar forbidden positive boundary claim.
- `hosted fallback detected`: any hosted provider call, hosted output, or hosted fallback appears.
- `provider key unexpectedly required`: provider key is requested, required, or printed.
- `artifact capture incomplete`: required command provenance, script provenance, stdout/stderr, repo status, or redacted JSON output is missing.
