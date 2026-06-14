# Evidence boundary

## What this packet proves

- Incident classes and severity levels have been documented.
- Minimum immediate stop actions for provider spend, exposure, and leaked credentials have been documented.
- Evidence preservation and redaction rules have been documented.
- Rollback triggers, owner roles, and a rollback communication template have been documented.
- Missing items before public exposure have been identified at a runbook level.

## What this packet does not prove

- It does not replace the repo-global selected next lane; repo-global selected-next control remains in `docs/CURRENT_STATE.md` and `docs/LANE_REGISTRY.md`.
- It does not authorize public exposure, provider calls, deployments, production readiness, public readiness, security/privacy completion, or DEF-002 closeout.
- It does not prove public readiness.
- It does not prove production readiness.
- It does not prove runtime readiness.
- It does not prove provider readiness or provider billing safety.
- It does not prove dashboard readiness.
- It does not prove `/v1/solve` readiness.
- It does not prove DEF-002 closure.
- It does not prove security/privacy completion.
- It does not prove incident drills were run.
- It does not prove credential rotation, spend caps, kill switches, alerting, rollback, or abuse controls work in any deployed environment.
- It does not accept residual risk.

## Evidence preservation rules

- Preserve timelines, owner decisions, route names, deployment versions, request IDs, redacted principal/tenant identifiers, and containment actions.
- Prefer metadata and hashes over raw sensitive payloads.
- Store restricted evidence only in approved access-controlled systems, not in repository docs.
- Redact screenshots before attaching them to PRs, docs, tickets, or chat.
- Re-review redaction manually because pattern-based redaction can miss novel secret formats.

## Forbidden evidence in this packet

- Full credentials, tokens, cookies, JWTs, signing secrets, passwords, private keys, refresh tokens, raw secret files, raw prompts, raw completions, raw provider payloads, raw tenant data, unrestricted logs, or environment dumps.

## Allowed verdicts

- `INCIDENT_RESPONSE_MINIMUMS_CAPTURED`
- `INCIDENT_RESPONSE_BLOCKED_OPERATOR_DECISION_REQUIRED`
- `STOP_INCONCLUSIVE`

This packet uses `INCIDENT_RESPONSE_MINIMUMS_CAPTURED` because the docs-only minimums were captured without making readiness claims.
