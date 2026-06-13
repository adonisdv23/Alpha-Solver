# Accepted residual risks (proposed — not accepted here)

This file records residual risks that are **candidates** for operator risk
acceptance. This docs-only review lane does **not** accept them. Acceptance is the
job of a separate operator lane
(`ALPHA-SOLVER-DEF-002-OPERATOR-RISK-ACCEPTANCE-001`), and only after the
gap-closure items in `risk-register.md` are addressed or explicitly deferred by
the operator.

## Proposed residual risks

### RR-04 — Inherent provider data-sharing when a provider is enabled

- **Risk:** When a remote provider is explicitly enabled, user prompt text is
  transmitted to a third-party provider (`service/app.py:266`, `:987`, `:1002`).
- **Why it may be acceptable:** It is intrinsic to provider-backed inference,
  off by default (`MODEL_PROVIDER=local`), and gated behind explicit operator
  opt-in. Telemetry and failure paths are content-free.
- **Acceptance precondition:** an operator-facing data-sharing/retention
  disclosure (which provider, what is sent, retention) is documented before
  provider use, and end users are informed.

### RR-A1 — Pattern-based redaction coverage limits

- **Risk:** `alpha/self_operator/redaction.py` redaction is keyword/regex driven;
  secret formats outside the keyword/regex set may not be redacted.
- **Why it may be acceptable:** redaction is deterministic, offline, and covers
  the common assignment/bearer/secret-keyword cases; it is defense-in-depth on
  top of the content-free telemetry/SAFE-OUT allowlists.
- **Acceptance precondition:** operator acknowledges the coverage limitation and
  the keyword/regex set is reviewed for the deployment's secret formats.

### Operational residuals (deployment responsibilities)

- **JWT keystore management:** the RS256 public-key YAML keystore
  (`service/auth/jwt_utils.py`) must be managed and rotated securely at the
  deployment layer.
- **Evidence payload hygiene:** callers of the evidence API
  (`service/evidence/api.py`) must not place secret material into evidence
  payloads; the API does not enforce this.

## What is NOT proposed for acceptance

The following remain **gap-closure** items and are explicitly **not** offered for
residual acceptance in this packet: RR-01 (CORS), RR-02 (plaintext
secrets-at-rest), RR-03 (default credentials), RR-05 (divergent classification
registries), RR-06/RR-07/RR-08 (dependency/supply-chain). See `risk-register.md`.
