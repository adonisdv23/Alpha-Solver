# Smoke Command Template

Do not run this command in this PR.

This template is blocked until endpoint-locality hardening is merged and reviewed. All angle-bracket values are operator-supplied fields for a later explicit execution lane.

```bash
ALPHA_LOCAL_LLM_SMOKE=1 \
ALPHA_LOCAL_LLM_ENDPOINT='http://127.0.0.1:<OPERATOR_SUPPLIED_PORT>/api/chat' \
ALPHA_LOCAL_LLM_MODEL='<OPERATOR_SUPPLIED_EXACT_MODEL_NAME>' \
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS='<OPERATOR_SUPPLIED_FINITE_TIMEOUT_SECONDS>' \
python -m pytest -q '<FUTURE_DEFAULT_SKIPPED_SMOKE_TEST_PATH>' -k '<FUTURE_SMOKE_TEST_NAME>'
```

## Template constraints

- Endpoint-locality hardening must fail closed on non-loopback / non-local endpoint URLs before any transport invocation.
- Endpoint must remain localhost-only using a loopback host pattern.
- Model name must be supplied by the operator in the future execution lane.
- Timeout must be finite.
- The referenced smoke test must be skipped by default unless the explicit opt-in flag is set.
- No provider access material may be passed.
- No hosted service fallback may be enabled.
- The command is a template only and has not been executed.
