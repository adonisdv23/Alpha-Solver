# Security / privacy inputs

Full inputs doc: [`docs/DEF_002_SECURITY_PRIVACY_INPUTS.md`](../../../DEF_002_SECURITY_PRIVACY_INPUTS.md).

Recorded for the future **DEF-002** review (not resolved here):

- **CORS** default `*` + credentials (ISS-003) — CONFIRMED.
- **Secrets at rest**: plaintext `FileSecretsBackend` (ISS-004) — CONFIRMED.
- **Provider telemetry**: allowlist-based, no payload inspection (ISS-005) —
  default-safe; verify opt-in paths.
- **Data sharing**: operator verification pending (PR #504).
- **Credential handling**: no SDK, httpx plumbing, `.env` gitignored, secrets
  not committed — CONFIRMED no committed real secrets.
- **Logging/redaction**: regex redaction without Unicode normalization (ISS-009)
  — CONFIRMED gap.
- **Dashboard exposure** / **`/v1/solve` exposure**: out of scope; not exposed.
- **Dependency/supply-chain**: small pinned dep set; review during DEF-002.
- **Existing machinery**: auth/audit/tenancy/validation/classification present →
  DEF-002 = assess + close gaps, not build-from-scratch.

**DEF-002 remains open.** No security/privacy completion claim is made.
