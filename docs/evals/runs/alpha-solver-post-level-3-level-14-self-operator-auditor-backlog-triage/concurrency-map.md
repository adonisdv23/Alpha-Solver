# Concurrency map

PROMPT 1 AND PROMPT 3 CAN RUN AT THE SAME TIME.

PROMPT 2 SHOULD WAIT FOR PROMPT 1 TO MERGE.

## Current lane relationship

- Prompt 3 is this auditor backlog triage lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-AUDITOR-BACKLOG-TRIAGE-001`.
- Prompt 1 may proceed concurrently because this lane is docs-only backlog capture and does not change the active limited repeatability packet.
- Prompt 2 should wait for Prompt 1 because it depends on Prompt 1's merged packet content and should not consume a stale plan.

## Item concurrency

| item_id | priority | classification | owning_lane | can_run_concurrently_with | blocked_by |
|---|---|---|---|---|---|
| `AUDIT-001` | A | `active_now` | limited repeatability packet hardening | Prompt 1 | PR #481 merged; current triage packet |
| `AUDIT-002` | A | `active_now` | limited repeatability packet hardening | Prompt 1 | PR #481 merged; current triage packet |
| `AUDIT-003` | A | `active_now` | limited repeatability packet hardening | Prompt 1 | known target file inventory |
| `AUDIT-004` | B | `active_next` | future prompt-bank hardening | Prompt 1 | none |
| `AUDIT-005` | A | `decision_recorded` | pre-Council AUDIT-005 decision and bundle routing fix lane | future F-1 checker-scope extension lane | AUDIT-005 decision recorded in `../alpha-solver-post-level-3-level-14-self-operator-pre-council-audit-005-decision-and-bundle-routing-fix/audit-005-decision-record.md`; future combined tooling/docs lanes must satisfy it |
| `AUDIT-006` | A | `active_now` | runbook prompt preflight hardening | Prompt 1 | canonical path inventory |
| `AUDIT-007` | A | `active_now` | limited repeatability packet hardening | Prompt 1 | known test-file inventory |
| `AUDIT-008` | C | `deferred` | future optional status CLI lane | Prompt 1 | operator prioritization |
| `AUDIT-009` | C | `deferred` | future optional status CLI lane | Prompt 1 | AUDIT-008; future implementation spec |
| `AUDIT-010` | B | `active_next` | future repeatability/status hardening | Prompt 1 | none |
| `AUDIT-011` | B | `active_next` | future evidence-boundary hardening | Prompt 1 | none |
| `AUDIT-012` | A | `active_now` | limited repeatability packet hardening | Prompt 1 | PR #481 merged; current triage packet |
| `AUDIT-013` | A | `active_now` | limited repeatability packet hardening | Prompt 1 | AUDIT-001 |
| `AUDIT-014` | A | `active_now` | execution-lane preflight hardening | Prompt 1 | none |
| `AUDIT-015` | A | `active_now` | execution-lane preflight hardening | Prompt 1 | none |
