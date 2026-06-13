# ALPHA-SOLVER-DEF-002-SECURITY-PRIVACY-REVIEW-PACKET-001

Verdict: `DEF_002_REVIEW_CAPTURED_OPEN_GAPS`

This is a **docs-only** product-level security/privacy review lane for DEF-002. It
assesses Alpha Solver's security and privacy posture using **committed repository
evidence only** and records a formal DEF-002 review packet.

This lane inspected code and docs **read-only**. It did not modify runtime,
product, provider, or model code; it did not modify tests or CI. It did not call
providers, use tokens, access secrets, print environment variables, deploy, or
expose `/v1/solve`.

## What this packet decides

- It **captures** a structured security/privacy review across the 14 required
  focus areas (see `security-privacy-scope.md`).
- It records concrete, file-and-line-cited evidence for each area.
- It enumerates open hardening gaps in `risk-register.md`.
- It records candidate operator-acceptable residual risks in
  `accepted-residual-risks.md` (proposed, not accepted here).
- It explicitly **does not** mark DEF-002 closed.

## Verdict rationale (summary)

Reviewable, committed code evidence is present for every required focus area, so
the review is not blocked by missing evidence. However, several open hardening
gaps remain that require remediation rather than mere operator acceptance:

- secrets-at-rest are stored in **plaintext** by the dashboard `FileSecretsBackend`;
- CORS default is wildcard origin (`*`) combined with `allow_credentials=True`;
- default API auth key (`dev-secret`) and default dashboard password
  (`alpha-dashboard`) ship as insecure development defaults;
- two divergent `data_classification.yaml` registries disagree on rules;
- dependencies have no lockfile / hash pinning and the repo vendors several
  third-party libraries.

Because open gaps remain, the verdict is `DEF_002_REVIEW_CAPTURED_OPEN_GAPS` and
the selected next lane drives gap closure. See `def-002-verdict.md`.

## Selected next lane

`ALPHA-SOLVER-DEF-002-GAP-CLOSURE-PLAN-001` (open gaps remain). See
`selected-next-lane.md`.

## Files in this packet

| File | Purpose |
| --- | --- |
| `repo-state-verification.md` | Branch, HEAD, and read-only verification context |
| `security-privacy-scope.md` | The 14 required focus areas and review scope |
| `data-flow-review.md` | Request/data-flow and local-vs-provider execution boundary |
| `credential-handling-review.md` | Secrets-at-rest, FileSecretsBackend, auth keys, JWT |
| `logging-redaction-review.md` | Logging, redaction, telemetry prompt-content risk |
| `provider-data-sharing-review.md` | Provider/API data-sharing boundaries |
| `dashboard-v1-solve-exposure-review.md` | Dashboard exposure and `/v1/solve` exposure |
| `dependency-supply-chain-review.md` | Dependency and supply-chain surface |
| `risk-register.md` | Open gaps / findings register |
| `accepted-residual-risks.md` | Proposed residual risks for operator acceptance |
| `def-002-verdict.md` | Formal verdict and closure-gating rationale |
| `forbidden-claims.md` | Claims this packet must not be used to assert |
| `non-actions.md` | Actions explicitly not taken (hard boundaries) |
| `selected-next-lane.md` | The selected downstream lane |

## Boundaries

This packet does not claim DEF-002 resolved, security/privacy completion, runtime
readiness, production readiness, or `/v1/solve`/dashboard readiness. See
`forbidden-claims.md`.
