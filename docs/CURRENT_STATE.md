# Alpha Solver — Current State

> Source-of-truth navigation doc. Last verified **2026-06-15** for post-#578 manual Value Read output-generation pilot.
> Docs-only; no provider/runtime claims.

## Current verified phase

**Post-#578 manual Value Read output-generation pilot posture: the manual no-provider raw-output pilot is complete, and operator review is required before any scoring or interpretation lane.**

The merged #569–#574 wave updated the repository from the post-#568 blocked Value Read state to a broader documentation-and-boundary posture. PR #576 was superseded by PR #577 and should be closed unmerged. PR #577 completes `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` as a docs-only Alpha-native local operator harness design note.

The current control posture is now `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_MANUAL_OUTPUT_GENERATION_PILOT_POST_578_001`: the operator-authorized manual no-provider prompt-contract simulation generated raw Alpha and baseline outputs for the selected 10 committed synthetic cases. The operator must separately authorize blind scorer packet construction, scoring, unblinding, and any final interpretation before those activities occur.

These are docs, gate, helper, static/research, and blocked-attempt artifacts. They do not prove provider behavior, model quality, value, readiness, benchmark success, security/privacy completion, local Ollama validation, `/v1/solve` readiness, production/public readiness, scoring outcomes, or Alpha superiority.

## At a glance

| Field | Value |
|-------|-------|
| Latest verified completed lane in this wave | **`ALPHA-SOLVER-VALUE-READ-MANUAL-OUTPUT-GENERATION-PILOT-POST-578-001`** |
| Live pre-edit verification | PR #578 merged; no open PRs at verification time |
| Closed-unmerged superseded PR | **#561** — superseded by merged PR #562 |
| Current controlling posture | Operator review required after completed manual no-provider Value Read output-generation pilot |
| Selected next state | **`OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_MANUAL_OUTPUT_GENERATION_PILOT_POST_578_001`** |
| Strategic boundary | Raw Alpha and raw baseline outputs were generated only as manual no-provider prompt-contract simulation artifacts. No scoring, blind-score filling, unblinding, final interpretation, provider call, local-model call, runtime endpoint, dashboard, public API exposure, Google Sheets mutation, benchmark claim, readiness claim, value claim, provider claim, local-model claim, security/privacy claim, or Alpha-superiority claim is authorized until separately approved |

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
| #576 | Superseded local operator harness design note PR | Superseded by PR #577; should be closed unmerged and not cited as the completion artifact. |
| #577 | `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` | Completes the docs-only Alpha-native local operator harness design note; no implementation or execution authorization. |
| post-577 lane | `ALPHA-SOLVER-VALUE-READ-EXECUTION-AUTHORIZATION-DECISION-POST-577-001` | Completes a docs-only authorization-decision packet for returning to Value Read execution authorization review. |
| post-578 lane | `ALPHA-SOLVER-VALUE-READ-MANUAL-OUTPUT-GENERATION-PILOT-POST-578-001` | Completes a bounded manual no-provider prompt-contract simulation output-generation pilot for 10 synthetic Value Read cases; raw Alpha and baseline outputs are documentation artifacts only, with no scoring, unblinding, provider/local-model call, endpoint exposure, or value/readiness claim. |

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for the PR status ledger and [`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lifecycle classification.

## Selected next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_MANUAL_OUTPUT_GENERATION_PILOT_POST_578_001`** is the current global selected next state.

This is a review state, not a scoring or interpretation lane. It means the raw manual no-provider Alpha and baseline outputs exist for the authorized subset, but no scoring, blind-score filling, unblinding, final interpretation, provider/local-model execution, runtime endpoint, dashboard/public API exposure, or Google Sheets mutation is authorized. The operator must separately authorize blind scorer packet construction and scoring.

This selected state authorizes no scoring, blind-score filling, unblinding, final interpretation, provider call, local model call, runtime endpoint, dashboard, public API exposure, Google Sheets mutation, benchmark claim, readiness claim, value claim, provider claim, local-model claim, security/privacy claim, or Alpha superiority claim.

## Open deferrals (see [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md))

- **DEF-001** — Self Operator execution evidence: substantially advanced within local-only scope; does not prove provider/runtime readiness.
- **DEF-002** — Product security/privacy review: open; `/v1/solve` exposure remains blocked by PR #571.
- **DEF-003** — Prior Fable delta-audit custody/replacement: open.
- **DEF-004** — Audit custody/provenance: open unless repo evidence shows otherwise.

## What is blocked / not authorized

- Provider calls, hosted model calls, local model calls, token use, credential access, billing inspection, dashboard exposure, `/v1/solve` exposure, public API exposure, Pi.dev installation/execution/integration, package-install experiments, and Google Sheets mutation.
- Value experiment execution and Alpha-vs-baseline claims. PR #568 is `VALUE_READ_BLOCKED`: it generated no Alpha outputs, baseline outputs, blind scores, or measured discrimination-delta. The post-577 authorization-decision lane prepares only an authorization-decision packet and still does not authorize execution.
- Local Ollama validation claims. PR #573 records a failed-closed local timeout/backend error and no local model answer.
- Security/privacy completion, production readiness, public MVP readiness, benchmark validation/superiority, broad-user readiness, autonomous readiness, provider validation, local Ollama validation, `/v1/solve` readiness, dashboard readiness, or Alpha superiority.

## What must not be claimed

This phase does **not** support claims of value, OpenAI validation, provider validation, local Ollama validation, Pi.dev integration, runtime readiness, production readiness, public MVP readiness, security/privacy completion, DEF-002 resolved, DEF-003 resolved, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, dashboard readiness, Google Sheets synchronization, or Alpha superiority.
