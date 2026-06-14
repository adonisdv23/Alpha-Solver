# Secrets and provider-cost gate

## Secret storage/display pass criteria

- No plaintext provider tokens are stored unless an operator explicitly accepts a no-persistence or encrypted-at-rest design.
- Secret files/directories have restrictive permissions where file storage remains.
- UI/API displays only masked values.
- Audit logs never contain raw secrets.
- Migration handling for existing plaintext files is documented and tested with synthetic values.
- No code path prints environment variables or credential values.

## Provider token and billing/cost pass criteria

- Provider calls are default-off and require explicit operator opt-in.
- Per-tenant and global spend/request/token caps are enforced before calls.
- A kill switch can disable provider calls immediately.
- Billing/project boundary is attested for the intended public environment.
- Cost telemetry is redacted, auditable, and alertable.

## Current classification

| Item | Status | Notes |
| --- | --- | --- |
| Masked dashboard display/audit | Pass now for existing settings behavior | Settings service masks stored keys for display and audit entries. |
| Restrictive file modes | Pass now for current file backend behavior | Settings storage code creates private parent/file modes on POSIX. |
| RR-02 credential storage hardening | Pass now for the narrow accepted RR-02 evidence boundary | PR #521 merged `ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001`, which hardens file/directory permission behavior for the existing file-backed dashboard credential path; DEF-002 remains open. |
| Default credential hardening | Fail now | DEF-002 RR-03 remains open. |
| Provider default-off | Pass now | `/v1/solve` provider branch requires explicit OpenAI provider opt-in. |
| Public cost caps | Fail now | Public traffic cost caps, tenant quotas, alerts, and shutdown are not proven. |
| Billing boundary | Unknown / requires implementation | Prior attestation applies to a bounded smoke boundary, not public exposure. |

## Gate result

Secrets and provider-cost controls remain no-go blockers until RR-03 default credential hardening, remaining DEF-002 lanes, residual-risk decisions, and public cost-cap evidence are complete. RR-02 credential storage hardening alone does not authorize exposure.
