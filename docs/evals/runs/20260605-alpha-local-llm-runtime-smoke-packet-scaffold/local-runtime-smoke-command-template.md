# Local Runtime Smoke Command Template

Do not run this command in the scaffold lane. Runtime smoke is not executed here.

## Template

```bash
# Placeholder only. Replace only after a reviewed implementation PR is merged.
ALPHA_LOCAL_RUNTIME_ENDPOINT="http://127.0.0.1:<port>" \
ALPHA_LOCAL_RUNTIME_MODEL="<exact-local-model-name>" \
ALPHA_LOCAL_RUNTIME_TIMEOUT_SECONDS="<finite-timeout-seconds>" \
ALPHA_LOCAL_RUNTIME_NO_HOSTED_FALLBACK="1" \
python <future-reviewed-runtime-smoke-entrypoint> \
  --endpoint "$ALPHA_LOCAL_RUNTIME_ENDPOINT" \
  --model "$ALPHA_LOCAL_RUNTIME_MODEL" \
  --timeout-seconds "$ALPHA_LOCAL_RUNTIME_TIMEOUT_SECONDS" \
  --no-hosted-fallback \
  --local-only
```

## Required Constraints

- Endpoint must be localhost or loopback only.
- Model name must be exact and local.
- Timeout must be finite.
- Hosted provider fallback must be unavailable or disabled.
- Provider keys must not be required for local mode.
- The smoke command must fail closed if the implementation is missing.

## Forbidden in This Scaffold

- Do not call a local model.
- Do not call a hosted provider.
- Do not make network calls.
- Do not import smoke results.
