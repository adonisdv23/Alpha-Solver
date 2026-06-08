# Self Operator Prep Inventory

## Docs-only Self Operator packets Level 8 should review

These packets are Self Operator preparation references. They help Level 8 understand proposed boundaries, but they do not prove runtime implementation or readiness.

| Packet | Key files Level 8 should review | Inventory use |
| --- | --- | --- |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-mvp-scope-matrix/` | `README.md`, `in-scope-mvp.md`, `out-of-scope-mvp.md`, `operator-only-boundary.md`, `blocked-until-later.md`, `dependency-notes.md`, `non-actions.md` | Understand narrow MVP scope, explicit exclusions, operator-only decisions, and pending dependencies. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-implementation-file-map/` | `README.md`, `likely-runtime-files.md`, `likely-test-files.md`, `likely-doc-files.md`, `forbidden-files.md`, `implementation-scope-rules.md`, `open-questions.md`, `non-actions.md` | Identify files a future authorized lane may inspect, while preserving that this packet does not grant modification authority. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-task-job-schema/` | `task-schema.md`, `job-schema.md`, `run-id-and-trace-fields.md`, `operator-confirmation-fields.md`, `stop-reason-fields.md`, `artifact-reference-fields.md`, `non-actions.md` | Review candidate task/job vocabulary for future operator-only records. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-lifecycle-state-machine/` | `lifecycle-overview.md`, `state-list.md`, `transition-rules.md`, `approval-gates.md`, `stop-and-blocked-states.md`, `audit-requirements.md`, `non-actions.md` | Review candidate lifecycle and stop-state semantics. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-human-approval-controls/` | `approval-principles.md`, `actions-requiring-approval.md`, `forbidden-without-approval.md`, `confirmation-wording.md`, `approval-record-schema.md`, `stop-conditions.md`, `non-actions.md` | Review human approval requirements and forbidden unauthorised actions. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-local-run-harness-design/` | `harness-overview.md`, `local-only-execution-boundary.md`, `preflight-requirements.md`, `forbidden-external-actions.md`, `stop-state-handling.md`, `artifact-capture-requirements.md`, `non-actions.md` | Review local-only harness expectations and external-action prohibitions. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-artifact-persistence-schema/` | `run-metadata-schema.md`, `prompt-preservation.md`, `output-preservation.md`, `confirmation-records.md`, `stop-reason-records.md`, `artifact-inventory.md`, `redaction-rules.md`, `non-actions.md` | Review candidate artifact preservation and redaction expectations. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-failure-mode-risk-register/` | `risk-register.md`, `misuse-cases.md`, `credential-and-provider-risks.md`, `unsafe-action-risks.md`, `evidence-promotion-risks.md`, `branch-pollution-risks.md`, `mitigations-and-stop-conditions.md`, `non-actions.md` | Review known risks and stop-condition candidates. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-operator-runbook-draft/` | `operator-flow.md`, `preflight-checklist.md`, `approval-checklist.md`, `monitoring-checklist.md`, `stop-and-recovery.md`, `artifact-review.md`, `archive-and-closeout.md`, `non-actions.md` | Review future human operator process after a separately authorized implementation exists. |
| `docs/evals/runs/alpha-solver-post-level-7-self-operator-acceptance-test-plan/` | `static-test-plan.md`, `local-smoke-test-plan.md`, `approval-gate-tests.md`, `stop-condition-tests.md`, `artifact-preservation-tests.md`, `blocked-action-tests.md`, `acceptance-criteria.md`, `non-actions.md` | Review future validation criteria without treating them as executed tests. |

## Prep-inventory boundary

These packets are supporting Self Operator prep references, not accepted runtime evidence. Level 8 may cite them to identify what to inspect and what remains blocked, but not to claim Self Operator is implemented, executable, safe, accepted, or ready.
