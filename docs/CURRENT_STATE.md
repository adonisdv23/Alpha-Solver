# Alpha Solver — Current State

> Source-of-truth navigation doc. Last verified **2026-06-15** for PR **#576** branch repair.
> Docs-only; no provider/runtime claims.

## Current verified phase

**Post-#576 posture: the Alpha-native local operator harness design note is complete, and an explicit operator decision is required before any next lane.**

The merged #569–#574 wave updated the repository from the post-#568 blocked Value Read state to a broader documentation-and-boundary posture. PR #576 then completed `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` as a docs-only Alpha-native local operator harness design note.

The current control posture is now `OPERATOR_DECISION_REQUIRED_AFTER_LOCAL_OPERATOR_HARNESS_DESIGN_NOTE_001`: no further implementation or execution lane is selected automatically. The operator must explicitly choose one future path before any new lane:

- authorize a separate local harness implementation/spec lane, or
- return to Value Read execution authorization, or
- stop and keep the design note as reference material.

This document does not choose for the operator.

These are docs, gate, helper, static/research, and blocked-attempt artifacts. They do not prove provider behavior, model quality, value, readiness, benchmark success, security/privacy completion, local Ollama validation, `/v1/solve` readiness, production/public readiness, or Alpha superiority.

## At a glance

| Field | Value |
|-------|-------|
| Latest verified PR in this wave | **#576** — Alpha-native local operator harness design note completed by this PR |
| PR branch state at verification | **#576 open / pending merge** on `adonisdv23/Alpha-Solver` |
| Closed-unmerged superseded PR | **#561** — superseded by merged PR #562 |
| Current controlling posture | Operator decision required after completed Alpha-native local operator harness design note |
| Selected next state | **`OPERATOR_DECISION_REQUIRED_AFTER_LOCAL_OPERATOR_HARNESS_DESIGN_NOTE_001`** |
| Strategic boundary | No implementation, UI, runtime, dependency, provider, local-model, Pi.dev, `/v1/solve`, dashboard/public API, Google Sheets, benchmark, Value Read, readiness, security/privacy, or superiority work is authorized until the operator chooses a future path |

## Completed post-552 / post-565 / post-568 infrastructure lanes

| PR | Lane / artifact | Evidence value |
|----|-----------------|----------------|
| #557 | `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001` | Defines the no-echo substantive generation gate after the post-552 fixes. |
| #558 | `ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001` | Adds a false-premise / hidden-constraint perturbation set for future Value Read design. |
| #559 | `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001` | Adds a narrative claim-safety linter artifact for unsupported claim detection. |
| #560 | `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001` | Defines the calibrated-confidence and non-claim output contract. |
| #562 | `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001` | Records the needs-human escalation protocol; supersedes closed-unmerged #561. |
| #563 | `ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001` | Adds higher-headroom Value Read cases for later bounded simulations/evals. |
| #564 | `ALPHA-SOLVER-PROMPT-CONTRACT-SIMULATION-METHODOLOGY-001` | Records prompt-contract simulation methodology. |
| #565 | `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001` | Records a local Ollama singlepath lab lane scaffold; no local model run is implied. |
| #566–#568 | `ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001` | Refreshes the Value Read packet and records `VALUE_READ_BLOCKED`; no Alpha/baseline outputs or scores. |
| #569 | Post-#568 current-state sync | Updates source-of-truth docs and MVP scorecard to the blocked Value Read state. |
| #570 | Founder memo refresh | Updates narrative positioning for the post-#568 blocked state. |
| #571 | `14 - V1 Solve Exposure Gate Packet` | Records `/v1/solve` exposure as `BLOCKED`; route existence is not public readiness. |
| #572 | Local Ollama singlepath operator helper | Adds an operator helper script for the local-only lane; helper existence is not a successful run. |
| #573 | Local Ollama singlepath blocked attempt | Records exact-model preflight success and failed-closed timeout/backend error; no local answer or quality evidence. |
| #574 | `18 - PI.DEV-HARNESS-FEASIBILITY` | Records `BORROW_PATTERNS_ONLY_NO_INTEGRATION` for Pi.dev harness research. |
| #576 | `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` | Completes the docs-only Alpha-native local operator harness design note; no implementation or execution authorization. |

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for the PR status ledger and [`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lifecycle classification.

## Selected next state

**`OPERATOR_DECISION_REQUIRED_AFTER_LOCAL_OPERATOR_HARNESS_DESIGN_NOTE_001`** is the current global selected next state.

This is a decision state, not an implementation lane. It means no implementation is authorized, no UI is authorized, no runtime work is authorized, no dependency work is authorized, no provider call is authorized, no local model call is authorized, no Pi.dev install/run/integration is authorized, no `/v1/solve` exposure is authorized, no dashboard or public API exposure is authorized, no Google Sheets mutation is authorized, no benchmark or Value Read execution is authorized, and no readiness, value, security/privacy, provider, local-Ollama, Pi.dev integration, or Alpha superiority claim is authorized.

The operator must explicitly choose one future path before any new lane:

1. authorize a separate local harness implementation/spec lane, or
2. return to Value Read execution authorization, or
3. stop and keep the design note as reference material.

This source-of-truth state does not choose for the operator and does not automatically authorize a successor lane.

## Open deferrals (see [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md))

- **DEF-001** — Self Operator execution evidence: substantially advanced within local-only scope; does not prove provider/runtime readiness.
- **DEF-002** — Product security/privacy review: open; `/v1/solve` exposure remains blocked by PR #571.
- **DEF-003** — Prior Fable delta-audit custody/replacement: open.
- **DEF-004** — Audit custody/provenance: open unless repo evidence shows otherwise.

## What is blocked / not authorized

- Provider calls, hosted model calls, local model calls, token use, credential access, billing inspection, dashboard exposure, `/v1/solve` exposure, public API exposure, Pi.dev installation/execution/integration, package-install experiments, and Google Sheets mutation.
- Value experiment execution and Alpha-vs-baseline claims. PR #568 is `VALUE_READ_BLOCKED`: it generated no Alpha outputs, baseline outputs, blind scores, or measured discrimination-delta.
- Local Ollama validation claims. PR #573 records a failed-closed local timeout/backend error and no local model answer.
- Security/privacy completion, production readiness, public MVP readiness, benchmark validation/superiority, broad-user readiness, autonomous readiness, provider validation, local Ollama validation, `/v1/solve` readiness, dashboard readiness, or Alpha superiority.

## What must not be claimed

This phase does **not** support claims of value, OpenAI validation, provider validation, local Ollama validation, Pi.dev integration, runtime readiness, production readiness, public MVP readiness, security/privacy completion, DEF-002 resolved, DEF-003 resolved, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, dashboard readiness, Google Sheets synchronization, or Alpha superiority.
