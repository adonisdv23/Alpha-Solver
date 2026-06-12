# Council audit evidence bundle

Lane ID: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-EVIDENCE-BUNDLE-001`

Purpose: prepare a frozen evidence bundle and manual prompt packet for a future Council of Reeds audit. This preparation lane does not run the Council, does not execute additional Self Operator runs, and does not claim eligibility beyond forwarding the packet to a future manual Council run lane.

Review decision dependency used: `accepted_for_council_audit_prep`.

Dependency status: PR #486 is present in local git history as merged into the current branch, and the required limited repeatability review packet selected this lane.

This is evidence for a narrow local-only operator-supervised Self Operator candidate. Do not infer production readiness, hosted readiness, runtime readiness, provider readiness, benchmark superiority, broad MVP readiness, release readiness, or autonomous readiness.

## Packet contents

- Evidence chain and manifest files for PR #480 through PR #486.
- Current state snapshot before any Council run.
- Manual Council runbook for independent GPT chats operated by a human.
- Seat matrix, seat prompts, response capture template, synthesis instructions, defect register template, severity rubric, claim boundaries, redaction rules, non-actions, checks, selected next lane, and fallback lane.

## Required evidence packets

- PR #480 first supervised-use execution / repair:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet-repair/`
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-execution/`
- PR #481 first supervised-use review:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-review/`
- PR #482 first-use review step-label correction:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-review/`
- PR #483 auditor backlog triage:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-auditor-backlog-triage/`
- PR #484 limited repeatability packet:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet/`
- PR #485 limited repeatability execution:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-execution/`
- PR #486 limited repeatability review:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-review/`

## Selected next lane

If this bundle remains clean after required preparation-lane checks only, the selected next lane is `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-MANUAL-RUN-001`. Council has not run, and this wording does not mean Council has found no defects.

If the evidence bundle is blocked before the manual Council run, select `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-EVIDENCE-BUNDLE-FIX-001`. Reserve `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-EVIDENCE-BUNDLE-FALLBACK-001` only for cases where the fix lane cannot proceed or the bundle cannot be safely repaired.

AUDIT-005 is now recorded in `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-pre-council-audit-005-decision-and-bundle-routing-fix/audit-005-decision-record.md`. F-1 remains open for the future checker-scope extension lane.
