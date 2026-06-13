# Deferral Register

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Conservative status; verified against
> committed packets. Nothing here is a readiness or resolution claim.
> "Blocks tiny smoke" = does this block the next narrow synthetic OpenAI token
> smoke? "Blocks public exposure" = does this block public/runtime/provider
> exposure, `/v1/solve`, or dashboards?

## DEF-001 — Self Operator execution evidence

- **Status:** **Substantially advanced within local-only scope** (not fully
  retired; does not prove provider/runtime readiness).
- **Supporting evidence:** PRs #497, #499, #500, #501 — offline Self Operator
  suite passes, release-gate CLI exits 0, operator approval captured and the
  local safety gate exercised; PR #501 verdict `APPROVAL_ACCEPTED_LOCAL_FLOW_CAPTURED`.
- **Missing evidence:** end-to-end operator-supervised run against a
  representative candidate task with recorded decisions on a **provider/runtime**
  path (inherently out of local-only scope).
- **What would close it:** operator-supervised end-to-end run with recorded
  decisions on the intended runtime path, plus durable artifacts.
- **Blocks tiny smoke:** No.
- **Blocks public exposure:** Yes (local-only evidence is insufficient for
  runtime/provider exposure).

## DEF-002 — Product security/privacy review

- **Status:** **Open.**
- **Supporting evidence:** PR #503 boundary packet enumerates what must be
  reviewed; substantial security machinery already exists (auth, audit, tenancy,
  validation, redaction, classification — see
  [`DEF_002_SECURITY_PRIVACY_INPUTS.md`](DEF_002_SECURITY_PRIVACY_INPUTS.md)).
- **Missing evidence:** a completed threat-model / gap-closure review covering
  CORS default, secrets-at-rest, provider telemetry paths, data-sharing,
  logging/redaction, dependency/supply-chain, dashboard/`/v1/solve` exposure.
- **What would close it:** an operator-scoped security/privacy assessment
  (frame as **assessment + gap closure of existing machinery**, not
  build-from-scratch) with recorded findings and dispositions.
- **Blocks tiny smoke:** No (a narrow synthetic smoke with redaction does not
  require DEF-002 closure).
- **Blocks public exposure:** Yes.

## DEF-003 — Prior Fable delta-audit custody / replacement

- **Status:** **Open (custody/provenance).**
- **Supporting evidence:** PR #503 boundary packet documents acceptable closure
  paths; the audit full text is **not** committed to the repo.
- **Missing evidence:** committed audit text with provenance, or an accepted
  replacement custody path.
- **What would close it:** commit the audit text (with redactions + provenance),
  or operator-approve a documented replacement.
- **Blocks tiny smoke:** No.
- **Blocks public exposure:** No directly (it is a custody/provenance gap), but
  it must not be cited as resolved security/quality evidence.

## DEF-004 — Audit custody / provenance (general)

- **Status:** **Open (custody/provenance)** unless repo evidence shows otherwise.
- **Supporting evidence:** evidence-discipline pattern across packets; no
  committed artifact closes general audit custody.
- **Missing evidence:** a committed, provenance-bearing custody record.
- **What would close it:** operator-supplied custody artifact committed with
  provenance.
- **Blocks tiny smoke:** No.
- **Blocks public exposure:** No directly; do not cite as resolved.

## Newly surfaced review inputs (issue-derived; not yet formal DEFs)

These come from audit verification (see [`ISSUE_REGISTER.md`](ISSUE_REGISTER.md))
and are recorded as inputs to future DEF-002 / hardening review. None blocks the
tiny smoke; none is resolved here.

| Ref | Topic | Blocks smoke | Blocks public exposure | Routed to |
|-----|-------|--------------|------------------------|-----------|
| ISS-003 | CORS default `*` + credentials | No | Yes | DEF-002 |
| ISS-004 | Plaintext file secrets backend | No | Yes (if dashboard/secrets exposed) | DEF-002 |
| ISS-005 | Provider telemetry (default allowlist-safe; opt-in paths unverified) | No | Review before public | DEF-002 |
| ISS-009 | Sanitizer lacks Unicode normalization | No | Yes (redaction-evasion risk) | DEF-002 |
| ISS-001 | Spec contamination (MCP-002 / NEW-010) | No | No | Spec reconciliation lane |

## Summary

- **None of DEF-001…DEF-004 is resolved.** DEF-001 is advanced (local-only).
- **No deferral blocks the next tiny synthetic smoke**, which is gated only on
  OpenAI project/billing clarification (PR #509).
- **DEF-002 (and the local-only limit of DEF-001) block public/runtime/provider
  exposure.**
