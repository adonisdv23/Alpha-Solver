# Alpha Solver — Current State

> Source-of-truth navigation doc. Last verified **2026-06-16** for post-581 blinded scoring pass completion and MVP scorecard score-state update.
> Docs-only; no provider/runtime claims.

## Current verified phase

**Post-581 blinded scoring pass posture plus MVP scorecard score-state update: the authorized blinded scorer packet has been scored and score-locked, the MVP scorecard now records that locked blind scores exist, and operator review is required before any unblinding or final interpretation happens.**

The merged #569–#574 wave updated the repository from the post-#568 blocked Value Read state to a broader documentation-and-boundary posture. PR #576 was superseded by PR #577 and should be closed unmerged. PR #577 completes `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` as a docs-only Alpha-native local operator harness design note.

The current control posture is now `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_BLIND_SCORING_PASS_POST_581_001`: the authorized blinded scorer packet has been scored in a scoring-only lane, the scores are locked, and the docs-only MVP scorecard update records score-state existence without score interpretation. The operator must separately authorize unblinding or final interpretation before either activity occurs.

These are docs, gate, helper, static/research, and blocked-attempt artifacts. They do not prove provider behavior, model quality, value, readiness, benchmark success, security/privacy completion, local Ollama validation, `/v1/solve` readiness, production/public readiness, unblinding outcome, final interpretation, or Alpha superiority.

## At a glance

| Field | Value |
|-------|-------|
| Latest verified completed lane in this wave | **`ALPHA-SOLVER-MVP-SCORECARD-AFTER-VALUE-READ-SCORE-001`** |
| Live pre-edit verification | PR #581 merged; no open PRs at verification time |
| Closed-unmerged superseded PR | **#561** — superseded by merged PR #562 |
| Current controlling posture | Operator review required after completed blinded scoring pass and score lock |
| Selected next state | **`OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_BLIND_SCORING_PASS_POST_581_001`** |
| Strategic boundary | The authorized blinded scorer packet has case-level blind scores and score-lock confirmation for the preserved manual no-provider raw-output pilot. No unblinding, final interpretation, provider call, local-model call, runtime endpoint, dashboard, public API exposure, Google Sheets mutation, benchmark claim, readiness claim, value claim, provider claim, local-model claim, security/privacy claim, or Alpha-superiority claim is authorized until separately approved |

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
| post-579 lane | `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PACKET-CONSTRUCTION-POST-579-001` | Completes docs-only blind scorer packet construction for the 10-case manual no-provider pilot; all scoring fields remain blank, the unblinding map is not committed, and no scoring, unblinding, provider/local-model call, endpoint exposure, or value/readiness claim occurs. |
| post-blind-packet lane | `ALPHA-SOLVER-VALUE-READ-SCORING-REVIEW-AUTHORIZATION-POST-BLIND-PACKET-001` | Completes docs-only scoring-review authorization preparation; scoring authorization language and blank score-output structure exist, but scoring, unblinding, final interpretation, provider/local-model calls, endpoint exposure, and value/readiness claims have not occurred. |
| post-581 lane | `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001` | Completes scoring-only review of the blinded scorer packet; case-level blind scores, notes, contested-score flags, scorer identity/tool, scoring method, timestamp, and score-lock confirmation are recorded, with no unblinding, final interpretation, provider/local-model call, endpoint exposure, or value/readiness claim. |
| scorecard-after-score lane | `ALPHA-SOLVER-MVP-SCORECARD-AFTER-VALUE-READ-SCORE-001` | Updates the docs-only MVP scorecard posture to record that locked blind scores exist while preserving the no-unblinding, no-final-interpretation, no-source-identity, and no-value/readiness/superiority-claim boundary. |

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for the PR status ledger and [`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lifecycle classification.

## Selected next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_BLIND_SCORING_PASS_POST_581_001`** is the current global selected next state.

This is a review state, not an unblinding or interpretation lane. It means blind scores and score-lock confirmation exist for the blinded scorer packet, but no unblinding, final interpretation, provider/local-model execution, runtime endpoint, dashboard/public API exposure, or Google Sheets mutation is authorized. The operator must separately authorize unblinding or final interpretation before either activity happens.

This selected state authorizes no unblinding, final interpretation, provider call, local model call, runtime endpoint, dashboard, public API exposure, Google Sheets mutation, benchmark claim, readiness claim, value claim, provider claim, local-model claim, security/privacy claim, or Alpha superiority claim.

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
