# Security/privacy review scope

## Objective

Assess Alpha Solver's product-level security and privacy posture using committed
repository evidence, and produce a formal DEF-002 review packet. This lane may
inspect code and docs read-only and must not modify runtime/provider behavior.

## In scope (14 required focus areas)

1. **CORS defaults** — `data-flow-review.md`, `dashboard-v1-solve-exposure-review.md`.
2. **Secrets-at-rest and FileSecretsBackend** — `credential-handling-review.md`.
3. **Credential handling** — `credential-handling-review.md`.
4. **Provider / API data-sharing boundaries** — `provider-data-sharing-review.md`.
5. **Logging and redaction** — `logging-redaction-review.md`.
6. **Provider telemetry prompt-content risk** — `logging-redaction-review.md`,
   `provider-data-sharing-review.md`.
7. **Dashboard exposure** — `dashboard-v1-solve-exposure-review.md`.
8. **`/v1/solve` exposure** — `dashboard-v1-solve-exposure-review.md`.
9. **Auth, JWT, API keys, tenancy, audit, evidence APIs** —
   `credential-handling-review.md`, `dashboard-v1-solve-exposure-review.md`.
10. **`data_classification.yaml` and related registries** — `data-flow-review.md`.
11. **Dependency / supply-chain surface** — `dependency-supply-chain-review.md`.
12. **Local vs provider execution boundaries** — `data-flow-review.md`,
    `provider-data-sharing-review.md`.
13. **Residual risks** — `risk-register.md`, `accepted-residual-risks.md`.
14. **Claim boundaries** — `forbidden-claims.md`, `def-002-verdict.md`.

## Out of scope (hard boundaries)

This lane does not, and this packet does not authorize anyone to:

- call providers or use tokens;
- access or read secrets;
- print or dump environment variables;
- deploy;
- expose `/v1/solve`;
- modify runtime / product / provider / model code;
- modify tests or CI.

## Method

For each focus area the reviewer:

1. located the authoritative committed source file(s);
2. read the relevant implementation read-only;
3. recorded observed controls and observed gaps with `file:line` citations;
4. assigned each gap a severity and a disposition (gap-closure vs. proposed
   residual-risk acceptance) in `risk-register.md`.

## Posture summary

Alpha Solver is **offline-first**. The default model provider is `local`
(`.env.example`), and remote/provider execution is gated behind explicit
environment opt-in. Several defensive controls are well-built (allowlist-based
provider telemetry and SAFE-OUT, deterministic secret redaction for Self
Operator artifacts, fail-closed dashboard mounting, tamper-evident audit hash
chain). The open gaps concentrate in insecure defaults (CORS, dev auth key,
dashboard password), plaintext secrets-at-rest, registry inconsistency, and the
dependency/supply-chain surface.
