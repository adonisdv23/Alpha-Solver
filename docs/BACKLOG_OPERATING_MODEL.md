# Backlog Operating Model

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Defines how backlog items are grouped and
> resolved. Docs-only; no item here authorizes a provider call, runtime
> exposure, or readiness claim.

## Backlog groups

1. **Current lane** — the single controlling lane in flight.
2. **Next ready lane** — the one selected next lane (no others run in parallel as "next").
3. **Blocked by operator** — needs a human decision/attestation.
4. **Blocked by missing evidence** — needs committed evidence to proceed.
5. **Blocked by provider/token/account setup** — needs OpenAI project/billing/account readiness.
6. **Evidence packets** — completed, kept as evidence (off active queue).
7. **Deferrals** — DEF-001…DEF-004 and issue-derived review inputs.
8. **OpenAI smoke and evals** — the smoke→eval progression.
9. **Security/privacy** — DEF-002 inputs and reviews.
10. **Runtime/product** — out of scope here; tracked, not worked.
11. **Checker and guardrail hardening** — static-checker scope and gates.
12. **Value experiment** — the strategic Alpha-vs-baseline protocol.
13. **Specs/docs integrity** — contamination, staleness, duplication.
14. **Backlog candidates** — surfaced ideas not yet scheduled.
15. **Historical archive** — preserved, removed from active queue.
16. **Do not touch** — canonical sources, preserved source artifacts.

## Paste-ready backlog table

| item | group | state | next lane / owner | blocks smoke | blocks public |
|------|-------|-------|-------------------|--------------|---------------|
| PR #508 checker-scope hardening | 6 Evidence packets / 11 Checker hardening | DONE (merged) | — | No | No |
| PR #509 OpenAI smoke retry — blocked by project/billing verification | 6 Evidence packets / 5 Provider setup | BLOCKED (merged evidence) | superseded by PR #511/#512 project-billing boundary chain | Yes | n/a |
| `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` | 6 Evidence packets / 5 Provider setup | BLOCKED evidence superseded by PR #512 (`BLOCKED_PROJECT_BILLING_OPERATOR_CONFIRMATION_MISSING`) | superseded by `OPENAI-PROJECT-BILLING-BOUNDARY-ATTESTATION-RETRY-001` | Yes | No |
| `OPENAI-PROJECT-BILLING-BOUNDARY-ATTESTATION-RETRY-001` | 1 Current lane / 5 Provider setup | CONFIRMED (`OPENAI_PROJECT_BILLING_BOUNDARY_CONFIRMED`) | `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` | No | No |
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` | 2 Next ready / 8 OpenAI smoke | **NEXT (selected)** | one tiny synthetic smoke retry only | Yes | No |
| `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` | 12 Value experiment | BLOCKED (after smoke) | after a successful tiny smoke | No | — |
| DEF-002 security/privacy review | 7 Deferrals / 9 Security | OPEN | DEF-002 review lane | No | Yes |
| DEF-003 audit custody or replacement | 7 Deferrals | OPEN (custody) | DEF-003 custody lane | No | No |
| docs/current-state cleanup | 13 Specs/docs integrity | DONE (this lane) | maintain `CURRENT_STATE.md` | No | No |
| spec contamination reconciliation | 13 Specs/docs integrity | OPEN | `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001` | No | No |
| roadmap refresh | 13 Specs/docs integrity | DONE (this lane) | docs maintainer | No | No |
| test hermeticity fix | 11 Checker/guardrail hardening | OPEN | test-hermeticity fix lane (not this lane) | No | No |
| evidence ledger / lane registry | 6 Evidence packets / 13 integrity | DONE (this lane) | maintain registries | No | No |
| CORS / security review input (ISS-003) | 9 Security/privacy | OPEN (input recorded) | DEF-002 | No | Yes |
| FileSecrets / security review input (ISS-004) | 9 Security/privacy | OPEN (input recorded) | DEF-002 | No | Yes |
| provider telemetry / security review input (ISS-005) | 9 Security/privacy | OPEN (default-safe; verify opt-in) | DEF-002 | No | Review |
| hardcoded pricing review (ISS-007) | 10 Runtime/product | OPEN (input recorded) | pricing review lane | No | No |
| sanitizer Unicode normalization review (ISS-009) | 9 Security/privacy | OPEN (input recorded) | DEF-002 | No | Yes |
| alpha/service architecture map (ISS-008, ISS-012) | 10 Runtime/product | OPEN (input recorded) | architecture-map lane | No | No |

## Operating rules

- Exactly **one** "Next ready" lane at a time (`LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002`).
- Provider-call lanes remain tightly bounded: PR #512 records the redacted project/billing attestation, but it does not authorize broad provider validation, evals, benchmarks, production, public MVP, or readiness claims.
- Security inputs (group 9) are **recorded, not fixed**, in this docs lane; they
  flow to DEF-002. Runtime/product (group 10) is tracked, not worked here.
- Evidence packets (group 6) are immutable; never re-run a merged lane verbatim.
- A tiny smoke proves plumbing only and never advances the value-experiment item.
