# Provider Selection Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Required provider modes

A future implementation may define explicit provider mode values such as:

- `hosted`
- `local_llm`

The exact names may be adjusted during implementation, but the semantics must remain explicit and auditable.

## Default provider behavior

Local LLM mode must be default-off. Absence of local LLM configuration must not enable local LLM behavior.

## Explicit operator selection

A future implementation must require explicit operator opt-in before local LLM mode is used. The implementation must not use auto-discovery, implicit local endpoint probing, environment-dependent activation, or opportunistic local routing.

## Local LLM key policy

Local LLM mode must require no hosted provider keys and no local provider keys. If a path requires provider credentials, that path must not be described as local LLM mode.

## Hosted-provider separation

Hosted provider operation must remain a separate selected mode. Hosted output must not be labeled as local LLM output.

## No silent fallback

When `local_llm` is selected and local handling fails closed, the failure must remain visible as a local LLM failure. The implementation must not silently route the same request to hosted providers.
