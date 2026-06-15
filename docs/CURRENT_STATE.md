# Alpha Solver — Current State

> Source-of-truth navigation doc. Last verified **2026-06-15** after live
> GitHub API verification of **0 open PRs** and merged PRs **#569–#574**.
> Docs-only; no provider/runtime claims.

## Current verified phase

**Post-#574 backlog/current-state sync posture; selected next lane is an Alpha-native local operator harness design note.**

The merged #569–#574 wave updated the repository from the post-#568 blocked Value Read state to a broader documentation-and-boundary posture:

- PR #569 refreshed the current-state, lane, evidence, and MVP scorecard docs after PR #568 recorded `VALUE_READ_BLOCKED`.
- PR #570 refreshed the founder memo for the post-#568 state.
- PR #571 added a blocked `/v1/solve` exposure gate packet.
- PR #572 added a local Ollama singlepath operator helper.
- PR #573 recorded a blocked local Ollama singlepath attempt: exact `gemma3:4b` preflight passed, but the local helper failed closed with a timeout/backend error and produced no local model answer.
- PR #574 recorded Pi.dev harness feasibility research and recommended borrowing patterns only, with no direct integration.

These are docs, gate, helper, static/research, and blocked-attempt artifacts. They do not prove provider behavior, model quality, value, readiness, benchmark success, security/privacy completion, local Ollama validation, `/v1/solve` readiness, production/public readiness, or Alpha superiority.

## At a glance

| Field | Value |
|-------|-------|
| Latest verified merged PR in this wave | **#574** — Pi.dev harness feasibility research note |
| Live open PR state at verification | **0 open PRs** on `adonisdv23/Alpha-Solver` |
| Closed-unmerged superseded PR | **#561** — superseded by merged PR #562 |
| Current controlling posture | Docs/research sync after blocked Value Read, blocked `/v1/solve` exposure gate, blocked local Ollama attempt, and Pi.dev no-integration decision |
| Selected next lane | **`ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001`** |
| Strategic boundary | Convert useful Pi.dev-style operator-harness patterns into Alpha-native design only, without installing Pi.dev, calling providers, exposing runtime surfaces, or claiming readiness/value evidence |

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

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for the PR status ledger and [`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lifecycle classification.

## Selected next lane

**`ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001`** is the recommended next active lane.

Purpose:

1. Define Alpha-native local operator-harness concepts inspired by Pi.dev patterns without importing or integrating Pi.dev.
2. Map prompt packets to named local templates and define a local session evidence format, branch labels, export redaction, and interrupt/follow-up semantics.
3. Preserve Alpha Solver's repo-native specs, evidence boundaries, budget guardrails, local-first posture, and no-runtime-change boundary.

This lane does **not** itself authorize provider calls, token use, credential access, billing inspection, hosted model calls, local model calls, Pi.dev installation, Pi.dev execution, package installation, dashboard exposure, `/v1/solve` exposure, public API exposure, Google Sheets mutation, benchmark execution, or value/readiness/security/privacy/provider/local-Ollama/Alpha-superiority claims unless a future operator authorization explicitly supplies those boundaries.

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
