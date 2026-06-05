# Fail-Closed Review

## Requirement

Local LLM mode must stop with a bounded local failure outcome for unsafe config, local transport failure, timeout, malformed response, empty output, prompt echo, and system echo. It must not make a hosted-provider call or present failed/echoed output as successful behavior.

## Findings

Fail-closed behavior is present for:

- default-off / missing explicit opt-in;
- provider-mode mismatch;
- missing model;
- non-exact model name with leading/trailing whitespace;
- missing, non-number, non-finite, zero, or negative timeout;
- forbidden provider keys;
- non-local endpoint;
- malformed endpoint;
- unsupported scheme;
- userinfo-bearing URL;
- invalid port;
- connection failure;
- timeout;
- generic backend error;
- malformed response;
- empty output;
- prompt echo;
- system echo;
- endpoint redirects.

`run_local_llm_provider_adapter()` normalizes injected backend exceptions into `LocalLLMAdapterResult(status="failed_closed")` with a stable reason label and `failure_label="failed_closed_result"`. Successful fake/injected outputs are classified as `status="non_evidence"`, not behavior evidence.

## Hosted fallback

No hosted-provider fallback branch was identified in the reviewed local LLM runtime path. Local failures are returned as local `failed_closed` outcomes.

## Decision impact

Fail-closed review found no blocker for bounded manual smoke. The future smoke lane must preserve local failure visibility and must not add fallback unless a later spec explicitly authorizes it.
