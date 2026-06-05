# Canonical Spec Compliance

Canonical spec reviewed: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

Index reviewed: `.specs/INDEX.md` includes `LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.

## Compliance matrix

| Spec requirement | Review result | Evidence summary |
| --- | --- | --- |
| Local LLM mode optional and default-off | Pass | Runtime config raises `local_llm_disabled_non_evidence` unless `ALPHA_LOCAL_LLM_ENABLED` is truthy. `.env.example` keeps local LLM settings commented and defaults `MODEL_PROVIDER=local`. |
| Explicit operator opt-in required | Pass | `scripts/check_env.py` requires `MODEL_PROVIDER=local_llm`, `ALPHA_LOCAL_LLM_ENABLED=true`, endpoint, model, and timeout before local LLM config passes. |
| Localhost / loopback endpoints only | Pass | Endpoint validation requires `http`, rejects userinfo, and accepts only `localhost` or loopback IP hosts. |
| No provider keys for local LLM mode | Pass | Config construction and environment checks reject hosted provider key variables in local LLM mode. |
| Finite timeout required | Pass | Timeout parsing rejects missing, non-number, non-finite, zero, and negative values. |
| Hosted output must not be labeled local | Pass | Runtime metadata uses explicit `provider_mode=local_llm`, `backend_class=ollama-local-http-runtime`, `local_backend`, and local model metadata; no hosted call branch exists in this path. |
| `behavior_evidence=false` preserved | Pass | Adapter result default, request metadata, runtime metadata, failure metadata, and tests preserve false. |
| Non-local, malformed, ambiguous, unsupported-scheme, missing-host, userinfo endpoints rejected | Pass | Endpoint tests and validator cover these fail-closed cases. |
| Connection failure, timeout, malformed response, empty output, prompt echo, system echo fail closed | Pass | Adapter catches injected backend failures and normalizes them to `failed_closed`; parser and echo guards reject malformed/empty/echo output. |
| No silent hosted fallback | Pass | Failure normalization returns local `failed_closed` outcomes and tests assert no hosted fallback behavior. |
| Distinguishable local provenance | Pass | Runtime metadata includes local backend/model/loopback/timeout/no-fallback/non-evidence labels. |
| `/v1/solve` and dashboard preview remain blocked | Pass | Runtime helper states it is intentionally not wired to these surfaces; `.env.example` preserves the same boundary. |

## Conclusion

The reviewed implementation satisfies the canonical contract sufficiently to authorize the next bounded manual runtime smoke lane. This conclusion is limited to source/config/test/runbook review and focused offline test execution; it is not runtime smoke evidence.
