# Alpha Solver - Current State

> Source-of-truth navigation doc. Last verified **2026-06-16** for local/OpenAI smoke runner.
> This lane adds a safe local/OpenAI smoke runner and runbook. The PR does not run smoke checks and makes no provider/runtime quality or readiness claims.

## Current verified phase

**Local/OpenAI smoke runner lane completed: the selected next state is review-only operator review after the smoke runner.**

The merged #569–#574 wave updated the repository from the post-#568 blocked Value Read state to a broader documentation-and-boundary posture. PR #576 was superseded by PR #577 and should be closed unmerged. PR #577 completes `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` as a docs-only Alpha-native local operator harness design note.

The previous Value Read control posture was `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_UNBLINDING_FINAL_INTERPRETATION_PASS_001`: `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001` completed as a docs-only evidence interpretation lane. Source identities were reviewed using an operator-provided map, locked scores were not changed, and the final interpretation remains bounded to the manual no-provider prompt-contract simulation. No release implementation lane is selected by this pass.

These are docs, gate, helper, static/research, blocked-attempt, scoring-only, selector, authorization-preparation, and bounded interpretation artifacts. They do not prove provider behavior, model quality, broad value, readiness, benchmark success, security/privacy completion, local Ollama validation, `/v1/solve` readiness, production/public readiness, or Alpha superiority.

## At a glance

| Field | Value |
|-------|-------|
| Latest verified completed lane in this wave | **`ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001`** |
| Source-of-truth sync | Current docs record the completed local/OpenAI smoke runner and a review-only selected next state |
| Closed-unmerged superseded PR | **#561** - superseded by merged PR #562 |
| Current controlling posture | Operator review required after local/OpenAI smoke runner |
| Selected next state | **`OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`** |
| Strategic boundary | This review-only state records the completed local/OpenAI smoke runner and runbook; it does not run smoke checks, authorize UI implementation without later reviewed smoke results, expose `/v1/solve`, mutate Google Sheets, generate scores, or support provider/local-model quality, readiness, benchmark, production/public, security/privacy, partnership/Pi.dev integration, or Alpha-superiority claims |

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
| PR #584 lane | `ALPHA-SOLVER-NEXT-RELEASE-SELECTOR-AFTER-VALUE-READ-001` | Completes a docs-only next-release selection gate with verdict `NEXT_RELEASE_SELECTION_BLOCKED_PENDING_VALUE_READ_UNBLINDING_AND_FINAL_INTERPRETATION`; selects no implementation lane because locked blind scores remain blinded and uninterpreted. |
| authorization-preparation lane | `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-AUTHORIZATION-001` | Completes a docs-only authorization-decision packet for a future unblinding/source-identity review and final interpretation pass. |
| unblinding-final-interpretation lane | `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001` | Completes source-identity review using the operator-provided map and final bounded interpretation; locked scores were not changed, claims remain bounded to the manual no-provider prompt-contract simulation, and no release implementation lane is selected. |
| PR #587 lane | `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-ASSET-001` | Completes a docs-only discrimination task-bank asset feasibility packet with verdict `FEASIBLE_WITH_GUARDED_NEXT_STEP`; no task execution, output generation, scoring, runtime/provider/local-model/API/Sheet work, benchmark, readiness, value, or superiority claim occurs. |
| PR #588 lane | `ALPHA-SOLVER-DEMO-EVIDENCE-PACKET-TO-DEMO-001` | Completes a docs-only claim-safe demo evidence packet feasibility packet with verdict `FEASIBLE_WITH_STRICT_EVIDENCE_BOUNDARIES`; no runtime demo, provider/local-model/API/Sheet work, product proof, value/readiness/superiority claim, or external-use approval occurs. |
| group-sync lane | `ALPHA-SOLVER-PARALLEL-FEASIBILITY-GROUP-SYNC-001` | Completes a preservation-only source-of-truth sync after the tabs 13-16 feasibility group settled; PR #581, PR #587, and PR #588 are merged, no open PR is editing the same source-of-truth docs, and deferred follow-up choices require a single operator decision. |
| selector-after-final-interpretation lane | `ALPHA-SOLVER-NEXT-RELEASE-SELECTOR-AFTER-FINAL-INTERPRETATION-001` | Completes a docs-only selector after final interpretation and the parallel feasibility group sync; selects `ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001` for operator review and does not create or implement that lane. |
| derivation-check lane | `ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001` | Completes a docs-first review-only substantive derivation / no-echo gate packet that defines criteria, fixture planning, heuristic review aids, stop conditions, non-actions, and non-claims; no implementation, provider/local-model/runtime/API/Sheet/scoring/unblinding/source-map/raw-output/release work or broad claims occur. |
| cheap-test packet lane | `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001` | Completes a docs-only first cheap-test packet with five representative taxonomy task cards for discrimination task-bank preparation, grounded in the derivation / no-echo gate and task-bank asset; no task execution, Alpha or baseline output generation, scoring, raw output inspection, unblinding, source-map work, provider/local-model/runtime/API/Sheet work, dependency addition, release implementation, or broad claims occur. |
| smoke-runner lane | `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001` | Adds `tools/operator_smoke_runner.py` and the operator packet for explicit local/Ollama or OpenAI smoke checks; this PR does not run either smoke and proves no provider quality, local model quality, readiness, benchmark success, production readiness, public readiness, or Alpha superiority. |

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for the PR status ledger and [`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lifecycle classification.

## Selected next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`** is the current global selected next state.

This is a review-only state after `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001`. It means the smoke runner and runbook have been created for operator review. It does not mean either smoke was run by this PR.

This state authorizes no UI implementation unless the Operator later provides reviewed smoke results, and no task execution, output generation, scoring, score change, source-map work, unblinding, raw Alpha output inspection, raw baseline output inspection, provider call, local model call, runtime work, API work, `/v1/solve` exposure, dashboard/public API exposure, Google Sheets mutation, dependency addition, routing behavior, council behavior, benchmark work, release behavior, readiness claim, broad value claim, provider claim, local-model claim, security/privacy claim, production/public claim, partnership/Pi.dev integration claim, demo external-use approval, discrimination-task execution/scoring, or Alpha-superiority claim.

## Open deferrals (see [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md))

- **DEF-001** - Self Operator execution evidence: substantially advanced within local-only scope; does not prove provider/runtime readiness.
- **DEF-002** - Product security/privacy review: open; `/v1/solve` exposure remains blocked by PR #571.
- **DEF-003** - Prior Fable delta-audit custody/replacement: open.
- **DEF-004** - Audit custody/provenance: open unless repo evidence shows otherwise.

## What is blocked / not authorized

- Provider calls, hosted model calls, local model calls, token use, credential access, billing inspection, dashboard exposure, `/v1/solve` exposure, public API exposure, Pi.dev installation/execution/integration, package-install experiments, and Google Sheets mutation.
- Release implementation lanes and broad Alpha-vs-baseline claims. The bounded manual no-provider pilot now has locked blind scores and a final interpretation, but this pass selects no release implementation lane and does not support claims beyond the 10-case manual no-provider prompt-contract simulation.
- Local Ollama validation claims. PR #573 records a failed-closed local timeout/backend error and no local model answer.
- Security/privacy completion, production readiness, public MVP readiness, benchmark validation/superiority, broad-user readiness, autonomous readiness, provider validation, local Ollama validation, `/v1/solve` readiness, dashboard readiness, or Alpha superiority.

## What must not be claimed

This phase does **not** support claims of broad value, OpenAI validation, provider validation, local Ollama validation, Pi.dev integration, runtime readiness, production readiness, public MVP readiness, security/privacy completion, DEF-002 resolved, DEF-003 resolved, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, dashboard readiness, Google Sheets synchronization, or Alpha superiority.
