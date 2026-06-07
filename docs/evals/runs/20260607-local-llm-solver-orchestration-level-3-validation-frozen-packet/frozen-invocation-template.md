# Frozen Invocation Template

## Approved command surface

Future execution lanes may use only this local-only operator CLI wrapper shape:

```text
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt "<FROZEN_PROMPT_TEXT_FOR_TEST_CASE_ID>" \
  --endpoint-url "http://127.0.0.1:<loopback-port>" \
  --model "<local-model-name>" \
  --timeout-seconds "<finite-positive-seconds>"
```

## Frozen invocation requirements

- Use `python -m alpha.local_llm.operator_cli`.
- Use `--enable-local-llm`; local LLM operation remains default-off and explicit opt-in only.
- Use the inline `--prompt` value from `frozen-test-set.md` for the relevant `test_case_id`.
- Use only loopback endpoint metadata, preferably `http://127.0.0.1:<loopback-port>`.
- Use a finite positive `--timeout-seconds` value and capture the exact value.
- Use only a local model name selected by a later authorized execution lane.
- Preserve `behavior_evidence=false` unless a later evidence model explicitly changes it.
- Preserve `no_hosted_fallback=true`.
- Preserve `no_provider_keys_required=true`.
- Do not provide hosted provider keys.
- Do not call hosted providers.
- Do not use provider fallback or hosted fallback.
- Do not expose or call `/v1/solve`.
- Do not expose or call dashboards.

## Template instantiation rule

The future execution lane must record the fully expanded command before execution and capture it as an artifact. This frozen packet does not instantiate the local model name, endpoint port, or timeout value because it does not execute validation.
