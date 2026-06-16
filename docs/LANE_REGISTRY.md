# Lane Registry

> Source-of-truth lane lifecycle registry. Verification date **2026-06-16** for
> post-581 blinded scoring pass completion.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| Post-581 blinded scoring pass posture | **current control posture** | `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001` is completed as scoring-only review for the post-579 blind scorer packet. The current selected state is operator review required, not an unblinding or interpretation lane. |

## Next ready / current selected state

| State | Lifecycle | Notes |
|-------|-----------|-------|
| **`OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_BLIND_SCORING_PASS_POST_581_001`** | **selected next state; review state, not an unblinding or interpretation lane** | The operator must separately authorize unblinding or final interpretation before either activity happens. No unblinding, final interpretation, provider call, local model call, runtime endpoint, dashboard/public API, Google Sheets mutation, benchmark claim, readiness claim, value claim, provider claim, local-model claim, security/privacy claim, or Alpha-superiority claim is authorized. |

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
- `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001` (stable post-merge state) — scoring-only review of the blinded scorer packet; blind scores are locked, with no unblinding, final interpretation, provider/local-model call, endpoint exposure, or value/readiness claim.

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
- Any selected-next pointer that conflicts with `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_BLIND_SCORING_PASS_POST_581_001`.
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
OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_BLIND_SCORING_PASS_POST_581_001 ← selected next state; review only, not unblinding or interpretation
```

This registry does not authorize any provider call, local model call, unblinding, final interpretation, Pi.dev install/run/integration, runtime endpoint, dashboard exposure, public API exposure, Google Sheets mutation, benchmark, or readiness/value/security/privacy/provider/local-Ollama/Alpha-superiority claim.
