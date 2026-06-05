# Backend Strategy Decision

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Decision

Exactly one backend strategy is selected for the future implementation lane:

- Selected: `hybrid`
- Not selected: `hosted-only`
- Not selected: `local-only`

## Meaning of hybrid in this specification

Hybrid means the product may expose separately configured hosted and local backend modes, but the provider for a request or run must be selected explicitly by operator configuration. Hybrid does not mean automatic fallback, opportunistic routing, provider racing, hidden orchestration, or substituting hosted output for a local LLM failure.

## Why hosted-only is not selected

Hosted-only would end local runtime integration planning. That would be simpler operationally, but it would not satisfy the selected planning direction to preserve local LLM as an optional backend path.

## Why local-only is not selected

Local-only would require local model setup for the affected LLM-backed path and would make local machine configuration too central. This conflicts with the requirement to preserve local LLM as optional and not make it the required MVP path.

## Why hybrid is selected

Hybrid is the smallest path that preserves existing hosted operation as a distinct option while allowing a future implementation lane to add default-off local LLM mode. The implementation must keep provider selection explicit and observable.

## Fallback rule attached to this decision

Because hybrid is selected, the future implementation must require explicit provider selection and must prohibit silent fallback. If fallback is ever separately authorized by a later lane, the fallback must be explicit, operator-approved, request-visible, and labeled in provenance as hosted-provider fallback rather than local LLM output.
