# Data sharing, telemetry, redaction, and prompt-content gate

## Pass criteria

- Data classification source of truth is reconciled and referenced by public docs.
- Operator/end-user disclosure states what prompt/context data is sent to providers, when, and under which opt-in.
- Telemetry fields are enumerated, redacted, and retention-scoped.
- Prompt logging policy is explicit: raw prompts are not logged unless specifically approved and protected.
- Redaction tests cover expected deployment secret/token formats.
- Evidence payload hygiene rules prevent secrets from being submitted to artifacts.
- Audit/evidence logs identify decision events without exposing secrets or raw credentials.

## Current classification

| Item | Status | Notes |
| --- | --- | --- |
| Default local boundary | Pass now | Current docs and code preserve an offline/local default unless provider is explicitly enabled. |
| Provider data sharing disclosure | Fail now | DEF-002 RR-04 remains an operator acceptance item after must-fix closure. |
| Data classification reconciliation | Fail now | DEF-002 RR-05 remains must-fix. |
| Redaction limits | Unknown / requires implementation | RR-A1 is only a residual candidate for later operator review; not accepted here. |
| Telemetry retention/access policy | Unknown / requires implementation | Needs public-surface policy and tests/evidence. |
| Audit/evidence logging coverage | Unknown / requires implementation | Some audit paths exist, but exposure-grade coverage and retention are not proven. |

## Gate result

Data sharing and telemetry boundaries are not ready for public exposure.
