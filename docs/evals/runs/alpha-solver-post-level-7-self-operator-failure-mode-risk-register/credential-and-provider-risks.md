# Credential and Provider Risks

## Credential risks

- Accidental exposure of API keys, tokens, private URLs, cookies, SSH material, service credentials, or environment contents.
- Committing secrets or secret-derived artifacts into docs, logs, screenshots, source artifacts, or generated files.
- Treating redaction as sufficient after a secret has already been exposed.
- Rotating, creating, deleting, or modifying credentials without a dedicated credential procedure.

## Provider risks

- Implicit provider calls through helper scripts, fallback logic, SDK defaults, dashboard previews, API routes, local model orchestration, or smoke tests.
- Hosted provider calls that create billing, data retention, privacy, or nondeterminism concerns.
- Local provider calls that are misreported as hosted-provider evidence or vice versa.
- Provider fallback that silently changes model, environment, cost, latency, or evidence class.

## Mitigations required before implementation

- Default-deny provider calls unless an explicit lane authorizes the provider, endpoint, model, data class, and budget boundary.
- Require environment and command review before commands that can call models or providers.
- Require secret scanning and redaction review before commit.
- Require no credential reads unless a human-approved credential task explicitly requires it.

## Stop conditions

- Stop if a command may call a provider or model outside approval.
- Stop if credentials, private URLs, or secret-like values appear in output or diffs.
- Stop if provider identity, billing boundary, fallback behavior, or data-retention boundary is ambiguous.

## Boundary

This packet does not call providers, inspect credentials, rotate credentials, configure models, configure fallback, or approve provider usage.
