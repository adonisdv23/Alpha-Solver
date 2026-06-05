# Residual Risk Register

| Risk | Status | Mitigation for next lane |
| --- | --- | --- |
| Runtime smoke has not yet been executed. | Open by design | Execute only in `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001` after recording endpoint, model, timeout, opt-in, and artifact paths. |
| Local model availability is unknown. | Open by design | Future operator must confirm the selected local model is already available before smoke and must not download during evidence capture unless separately authorized. |
| Local model quality is unknown. | Out of scope | Do not make quality claims; smoke may record only bounded runtime invocation outcome. |
| Real local endpoint behavior is unknown. | Open by design | Future smoke must preserve raw and sanitized artifacts and classify pass/fail/blocked narrowly. |
| Full-suite failures remain outside local LLM scope. | Open but unrelated | Track or repair in separate lanes; do not treat them as local LLM blockers unless new evidence connects them. |
| Runbook placeholders require concrete smoke values. | Controlled | Next lane must fill exact implementation-specific endpoint/model/timeout/command values before execution. |
| `/v1/solve` and dashboard preview remain unsupported for local LLM runtime. | Preserved | Do not expose these surfaces unless a later spec explicitly authorizes them. |
| Hosted fallback remains prohibited. | Preserved | Any future fallback requires a separate spec defining explicit operator opt-in, trigger conditions, credentials, provenance, and tests. |

## Review conclusion

No residual risk blocks a bounded manual smoke execution lane, provided the next lane remains within the authorization limits and stops on missing prerequisites.
