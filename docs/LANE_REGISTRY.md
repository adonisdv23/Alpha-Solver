# Lane Registry

> Source-of-truth lane lifecycle registry. Verification date **2026-06-16** for
> preservation-only parallel feasibility group sync after tabs 13-16.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| Preservation-only parallel feasibility group sync | **current control posture** | `ALPHA-SOLVER-PARALLEL-FEASIBILITY-GROUP-SYNC-001` completed after tabs 13-16 settled. PR #581, PR #587, and PR #588 are merged; live verification found zero open PRs and no open source-of-truth doc conflict. The sync records merged preservation-only feasibility packets and defers follow-up choice to one operator decision state. |

## Next ready / current selected state

| State | Lifecycle | Notes |
|-------|-----------|-------|
| **`OPERATOR_DECISION_REQUIRED_AFTER_PARALLEL_FEASIBILITY_GROUP_SYNC_001`** | **selected next state; operator decision state, not an implementation lane** | The preservation-only feasibility group after tabs 13-16 has settled and source-of-truth docs now record what merged. Operator decision is required before choosing any one future follow-up lane. No new feasibility content, runtime work, providers, local models, dashboard/public API work, `/v1/solve`, Google Sheets mutation, scoring, source-map work, final interpretation, implementation lane, readiness/broad-value/provider/local-model/security/privacy/production/public/partnership/Pi.dev integration/demo external-use/discrimination-scoring claim, or Alpha-superiority claim is authorized. |

## Completed (kept as evidence)

- `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001` (PR #557) — no-echo substantive generation gate.
- `ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001` (PR #558) — false-premise and hidden-constraint perturbation case set.
- `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001` (PR #559) — narrative claim-safety linter.
- `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001` (PR #560) — calibrated-confidence output contract.
- `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001` (PR #562) — docs-only needs-human escalation protocol.
- `ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001` (PR #563) — higher-headroom Value Read case set.
- `ALPHA-SOLVER-PROMPT-CONTRACT-SIMULATION-METHODOLOGY-001` (PR #564) — prompt-contract simulation methodology.
- `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001` (PR #565) — local Ollama singlepath lab scaffold.
- `ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001` (PRs #566–#568) — packet refresh plus blocked manual-run artifact; no Alpha/baseline outputs or scores.
- Post-#568 current-state sync (PR #569) — source-of-truth docs and MVP scorecard refresh for `VALUE_READ_BLOCKED`.
- Founder memo refresh (PR #570) — narrative positioning for the blocked Value Read state.
- `14 - V1 Solve Exposure Gate Packet` (PR #571) — `/v1/solve` public exposure is `BLOCKED`.
- Local Ollama singlepath operator helper (PR #572) — local-only helper added; no successful model run implied.
- Local Ollama singlepath blocked attempt (PR #573) — exact `gemma3:4b` model preflight passed, then helper failed closed with timeout/backend error and produced no local answer.
- `18 - PI.DEV-HARNESS-FEASIBILITY` (PR #574) — `BORROW_PATTERNS_ONLY_NO_INTEGRATION` research note.
- `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` (PR #577) — docs-only Alpha-native local operator harness design note; completed by PR #577 with no implementation or execution authorization.
- `ALPHA-SOLVER-VALUE-READ-EXECUTION-AUTHORIZATION-DECISION-POST-577-001` (stable post-merge state) — docs-only authorization-decision packet.
- `ALPHA-SOLVER-VALUE-READ-MANUAL-OUTPUT-GENERATION-PILOT-POST-578-001` (stable post-merge state) — manual no-provider prompt-contract simulation raw-output pilot; no scoring, unblinding, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PACKET-CONSTRUCTION-POST-579-001` (stable post-merge state) — docs-only blind scorer packet construction; no scoring, unblinding, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-VALUE-READ-SCORING-REVIEW-AUTHORIZATION-POST-BLIND-PACKET-001` (stable post-merge state) — docs-only scoring-review authorization preparation; scoring language and blank score-output structure exist, but no scoring, unblinding, provider/local-model call, endpoint exposure, final interpretation, or value/readiness claim.
- `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001` (stable post-merge state) — scoring-only review of the blinded scorer packet; blind scores are locked, with no score change, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-MVP-SCORECARD-AFTER-VALUE-READ-SCORE-001` (stable post-merge state) — docs-only MVP scorecard score-state update; locked blind scores exist, but score interpretation remains blocked with no unblinding, source-identity reveal, final interpretation, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-NEXT-RELEASE-SELECTOR-AFTER-VALUE-READ-001` (PR #584) — docs-only next-release selector; verdict `NEXT_RELEASE_SELECTION_BLOCKED_PENDING_VALUE_READ_UNBLINDING_AND_FINAL_INTERPRETATION`; selected no implementation lane because locked blind scores remain blinded and uninterpreted.
- `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-AUTHORIZATION-001` (stable post-merge state) — docs-only authorization-decision packet; prepared unblinding/source-identity review and final interpretation authorization language and protocols.
- `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001` (stable post-merge state) — docs-only source-identity review and final bounded interpretation; source identities were reviewed using the operator-provided map, locked scores were not changed, final interpretation exists, claims remain bounded to the manual no-provider prompt-contract simulation, and no release implementation lane is selected.
- `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-ASSET-001` (PR #587) — docs-only discrimination task-bank asset feasibility packet; guarded follow-up deferred, no execution/scoring/runtime/provider/local-model/API/Sheet/readiness/value/superiority claim.
- `ALPHA-SOLVER-DEMO-EVIDENCE-PACKET-TO-DEMO-001` (PR #588) — docs-only claim-safe demo evidence packet feasibility packet; strict evidence-boundary follow-up deferred, no runtime demo/external-use approval/product proof/value/readiness/superiority claim.
- `ALPHA-SOLVER-PARALLEL-FEASIBILITY-GROUP-SYNC-001` (stable post-merge state) — preservation-only source-of-truth sync after tabs 13-16; records PR #581, #587, and #588 as merged and no open source-of-truth doc conflict.

## Superseded

| Lane / PR | Superseded by | Why |
|-----------|---------------|-----|
| PR #561 — `Add needs-human escalation protocol` | PR #562 | #561 is closed unmerged; #562 merged the docs-only needs-human protocol. |
| Older smoke-authorization selected-next pointers | Post-#568 and post-#574 selected-next lanes in this registry and [`CURRENT_STATE.md`](CURRENT_STATE.md) | The #557–#574 wave changed the active posture to Value Read blocked evidence, exposure/local-lab gates, and an Alpha-native harness design next step. |
| `ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001` as older immediate next pointer | Historical pointer; not current selected state | Value Read execution remains blocked unless the operator separately authorizes a future output-generation lane. |
| `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` as selected next after PR #575 | PR #577 completed that lane | Future operators must not be routed back to the completed design-note lane. |
| PR #576 - Add Alpha-native local operator harness design note | PR #577 | PR #577 includes the design note plus source-of-truth closeout and green checks; #576 should be closed unmerged and not cited as merged evidence. |
| `OPERATOR_DECISION_REQUIRED_AFTER_LOCAL_OPERATOR_HARNESS_DESIGN_NOTE_001` as post-#577 decision state | `ALPHA-SOLVER-VALUE-READ-EXECUTION-AUTHORIZATION-DECISION-POST-577-001` | This was the decision-only state after PR #577. PR #578 records the operator decision to return to Value Read execution authorization review by completing the docs-only authorization-decision packet. |
| `ALPHA-SOLVER-VALUE-READ-EXECUTION-AUTHORIZATION-DECISION-POST-577-001` | `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_MANUAL_OUTPUT_GENERATION_PILOT_POST_578_001` | The post-578 manual pilot supersedes the prior review-state pointer. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_MANUAL_OUTPUT_GENERATION_PILOT_POST_578_001` | `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_SCORING_REVIEW_AUTHORIZATION_POST_BLIND_PACKET_001` | The post-579 blind scoring packet construction supersedes the post-578 review pointer. The current selected state is operator review only, not a scoring or interpretation lane. |

## Blocked / not authorized

| Lane / activity | Blocked by | Unblock condition |
|-----------------|-----------|-------------------|
| Provider calls / hosted model runs / token use | Hard boundary for current docs-only sync | Separate explicit operator authorization in a future lane. |
| Local model / Ollama execution | Current evidence includes a failed-closed local attempt, not validation | Separate operator-managed local run authorization and preserved evidence boundaries; do not treat #573 as quality/readiness evidence. |
| Dashboard, `/v1/solve`, public API exposure | PR #571 exposure gate verdict is `BLOCKED` | Separate exposure/readiness/security lane after identity, tenancy, logging, redaction, rate-limit, CORS/ingress, monitoring, incident-response, rollback, and authorization questions are resolved. |
| Pi.dev installation, execution, or integration | PR #574 recommends patterns-only/no-integration | Separate spec, threat model, package/provenance review, sandbox, no-secret workspace, provider/key policy, export policy, and operator authorization. |
| Google Sheets or backlog workbook mutation | Repo task boundary | Operator-managed external ledger process only; this repo PR may include paste-ready sheet updates but must not mutate the Sheet. |
| Value/readiness/provider/security/privacy/local-Ollama/Pi.dev/Alpha-superiority claims | No execution or validation evidence exists; #568 has no outputs/scores and #573 failed closed | Properly scoped future evidence with pre-registered boundaries. |

## Do not run again (as-is)

- PR #561 lane as a standalone needs-human protocol PR — closed unmerged and superseded by PR #562.
- Any merged packet lane verbatim — packets are immutable evidence; create a new lane id instead.
- Any selected-next pointer that conflicts with `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_UNBLINDING_FINAL_INTERPRETATION_PASS_001`.
- Direct Pi.dev integration from PR #574's research lane — the recorded verdict is patterns-only/no-integration.

## Forward path (single track)

```text
#557 no-echo gate
#558 false-premise / hidden-constraint set
#559 claim-safety linter
#560 calibrated-confidence contract
#562 needs-human protocol (supersedes #561)
#563 higher-headroom cases
#564 prompt-contract methodology
#565 local Ollama singlepath scaffold
        │
        ▼
ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001 / PR #568 artifact ← VALUE_READ_BLOCKED
        │
        ▼
#569 current-state sync
#570 founder memo refresh
#571 /v1/solve exposure gate ← BLOCKED
#572 local Ollama helper
#573 local Ollama attempt ← FAILED_CLOSED_TIMEOUT / no local answer
#574 Pi.dev harness feasibility ← BORROW_PATTERNS_ONLY_NO_INTEGRATION
        │
        ▼
#577 local operator harness design note completed
        │
        ▼
ALPHA-SOLVER-VALUE-READ-EXECUTION-AUTHORIZATION-DECISION-POST-577-001 ← docs-only packet
        │
        ▼
ALPHA-SOLVER-VALUE-READ-MANUAL-OUTPUT-GENERATION-PILOT-POST-578-001 ← manual no-provider raw outputs; no scoring/unblinding
        │
        ▼
ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PACKET-CONSTRUCTION-POST-579-001 ← blinded packet exists; no scoring/unblinding
        │
        ▼
ALPHA-SOLVER-VALUE-READ-SCORING-REVIEW-AUTHORIZATION-POST-BLIND-PACKET-001 ← scoring authorization materials
        │
        ▼
ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001 ← blind scores locked; no unblinding/final interpretation
        │
        ▼
ALPHA-SOLVER-NEXT-RELEASE-SELECTOR-AFTER-VALUE-READ-001 ← docs-only selection gate; no implementation lane selected
        │
        ▼
ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-AUTHORIZATION-001 ← docs-only authorization-decision packet
        │
        ▼
ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001 ← source identities reviewed with operator-provided map; locked scores unchanged; bounded final interpretation exists
        │
        ▼
#587 / #588 preservation-only feasibility packets ← merged; follow-ups deferred
        │
        ▼
ALPHA-SOLVER-PARALLEL-FEASIBILITY-GROUP-SYNC-001 ← source-of-truth sync; no open PR conflicts
        │
        ▼
OPERATOR_DECISION_REQUIRED_AFTER_PARALLEL_FEASIBILITY_GROUP_SYNC_001 ← selected next state; operator decision, not implementation
```

This registry does not authorize any provider call, local model call, score change, Pi.dev install/run/integration, runtime endpoint, dashboard exposure, public API exposure, Google Sheets mutation, benchmark, release implementation lane, or readiness/broad-value/security/privacy/provider/local-Ollama/Alpha-superiority claim.
