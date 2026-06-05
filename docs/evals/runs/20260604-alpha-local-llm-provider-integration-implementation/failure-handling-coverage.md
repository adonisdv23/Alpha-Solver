# Failure-Handling Coverage

Lane: `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-IMPLEMENTATION-001`

## Covered fail-closed cases

| Case | Offline coverage |
| --- | --- |
| Default-off backend | Disabled Ollama-style backend returns `failed_closed` before transport. |
| Timeout | Injected transport raises `TimeoutError`; adapter returns `ollama_timeout_non_evidence`. |
| Connection failure | Injected transport raises `OSError`; adapter returns `ollama_connection_failure_non_evidence`. |
| Backend HTTP error | Injected transport raises `HTTPError`; adapter returns `ollama_backend_error_non_evidence`. |
| Malformed response | Static malformed fixture returns `malformed_ollama_response_non_evidence`. |
| Empty output | Empty static fixture returns `empty_ollama_response_non_evidence`; existing stub empty output coverage is preserved. |
| Prompt echo | Parser and backend tests reject echoed user prompt as `prompt_echo_non_evidence`. |
| Missing contract | Existing adapter test preserves portable-contract missing-file fail-closed behavior before backend access. |
| Empty contract | Existing adapter test preserves empty portable-contract fail-closed behavior before backend access. |
| Fingerprint mismatch | Existing adapter test preserves SHA-256 mismatch fail-closed behavior before backend access. |
| Stub backend error | Existing adapter test preserves injected-backend error normalization. |
| Non-local endpoint | Backend validates local HTTP endpoints before transport when enabled. |

## No fallback behavior

Failure paths do not route to hosted providers, alternate backends, deterministic
v91 fallback, `/v1/solve`, dashboard preview, or operator-test evidence paths.
