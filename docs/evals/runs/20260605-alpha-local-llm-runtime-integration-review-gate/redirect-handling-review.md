# Redirect Handling Review

## Requirement

HTTP redirects must not be followed and must fail closed.

## Findings

- The local urllib transport uses a custom redirect handler that returns `None` for all redirect requests.
- Redirect status codes `301`, `302`, `303`, `307`, and `308` are identified as redirect outcomes.
- `urllib_ollama_json_transport()` maps redirect `HTTPError` outcomes in those status codes to `LocalLLMProviderAdapterError("endpoint_redirect_non_evidence")`.
- The adapter runner converts that error into a `failed_closed` local result and preserves `behavior_evidence=false`.
- Redirect handling contains no hosted-provider fallback and no redirected target execution authorization.

## Test evidence reviewed

Focused runtime integration tests cover redirect fail-closed behavior for `301`, `302`, `303`, `307`, and `308` using fake opener/handler behavior rather than a real HTTP endpoint.

## Decision impact

Redirect handling review found no blocker for bounded manual smoke. The future smoke lane must not override the no-redirect behavior.
