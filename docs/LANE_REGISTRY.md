# Lane Registry

> Source-of-truth lane lifecycle registry. Verification date **2026-06-18** for
> console target-parity product pass.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| Console target-parity product pass | **current control posture** | `ALPHA-SOLVER-CONSOLE-TARGET-PARITY-PRODUCT-PASS-001` adds route-flow, task-interpretation, model-route, tool-route, manual-override, and evidence-boundary cards to the local-only console. Selected next state is `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001`. |

## Next ready / current selected state

| State | Lifecycle | Notes |
|-------|-----------|-------|
| **`OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001`** | **deferred-review selected next state** | Operator review remains deferred while another narrow local-console build or gap-closure lane moves closer to the uploaded HTML capability guide and target diagrams. Provider/local-model/hosted-model/tool/web execution, runtime GitHub calls, `/v1/solve`, Sheets, scoring, unblinding, readiness/value/superiority claims, and model/tool quality claims remain unauthorized. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_METADATA_DISPLAY_001` | prior review-only selected next state | Operator review was required after the local-console route-preview metadata display lane before this packet was prepared. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001` | prior review-only selected next state | Blinded scorer packet construction was recorded before blind scoring authorization prep. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUTS_001` | prior review-only selected next state | Manual prompt-contract simulation outputs were recorded before blinded scorer packet construction. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001` | prior review-only selected next state | Blank operator-fillable templates were recorded after `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001`. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001` | prior review-only selected next state | Docs-only routed-vs-plain pilot authorization was recorded after `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001`. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` | prior review-only selected next state | Partial screenshot-only local MVP manual review was recorded after `ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001`; verdict was `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST`. |
| `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001` | prior review-only selected next state | Operator review was required after the static routed-vs-plain pilot packet. The pilot was not executed; no provider/local-model calls, tool execution, browsing, Alpha output generation, baseline output generation, scoring, unblinding, raw output inspection, source-map work, Google Sheets mutation, or `/v1/solve` exposure/invocation occurred. No readiness, benchmark, production/public, provider, local-model, tool-quality, security/privacy, or Alpha-superiority claim is created by this lane. The prior selected next state was `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001`. |

## Completed (kept as evidence)

- `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001` (PR #557) - no-echo substantive generation gate.
- `ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001` (PR #558) - false-premise and hidden-constraint perturbation case set.
- `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001` (PR #559) - narrative claim-safety linter.
- `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001` (PR #560) - calibrated-confidence output contract.
- `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001` (PR #562) - docs-only needs-human escalation protocol.
- `ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001` (PR #563) - higher-headroom Value Read case set.
- `ALPHA-SOLVER-PROMPT-CONTRACT-SIMULATION-METHODOLOGY-001` (PR #564) - prompt-contract simulation methodology.
- `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001` (PR #565) - local Ollama singlepath lab scaffold.
- `ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001` (PRs #566–#568) - packet refresh plus blocked manual-run artifact; no Alpha/baseline outputs or scores.
- Post-#568 current-state sync (PR #569) - source-of-truth docs and MVP scorecard refresh for `VALUE_READ_BLOCKED`.
- Founder memo refresh (PR #570) - narrative positioning for the blocked Value Read state.
- `14 - V1 Solve Exposure Gate Packet` (PR #571) - `/v1/solve` public exposure is `BLOCKED`.
- Local Ollama singlepath operator helper (PR #572) - local-only helper added; no successful model run implied.
- Local Ollama singlepath blocked attempt (PR #573) - exact `gemma3:4b` model preflight passed, then helper failed closed with timeout/backend error and produced no local answer.
- `18 - PI.DEV-HARNESS-FEASIBILITY` (PR #574) - `BORROW_PATTERNS_ONLY_NO_INTEGRATION` research note.
- `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` (PR #577) - docs-only Alpha-native local operator harness design note; completed by PR #577 with no implementation or execution authorization.
- `ALPHA-SOLVER-VALUE-READ-EXECUTION-AUTHORIZATION-DECISION-POST-577-001` (stable post-merge state) - docs-only authorization-decision packet.
- `ALPHA-SOLVER-VALUE-READ-MANUAL-OUTPUT-GENERATION-PILOT-POST-578-001` (stable post-merge state) - manual no-provider prompt-contract simulation raw-output pilot; no scoring, unblinding, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PACKET-CONSTRUCTION-POST-579-001` (stable post-merge state) - docs-only blind scorer packet construction; no scoring, unblinding, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-VALUE-READ-SCORING-REVIEW-AUTHORIZATION-POST-BLIND-PACKET-001` (stable post-merge state) - docs-only scoring-review authorization preparation; scoring language and blank score-output structure exist, but no scoring, unblinding, provider/local-model call, endpoint exposure, final interpretation, or value/readiness claim.
- `ALPHA-SOLVER-VALUE-READ-BLIND-SCORING-PASS-POST-581-001` (stable post-merge state) - scoring-only review of the blinded scorer packet; blind scores are locked, with no score change, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-MVP-SCORECARD-AFTER-VALUE-READ-SCORE-001` (stable post-merge state) - docs-only MVP scorecard score-state update; locked blind scores exist, but score interpretation remains blocked with no unblinding, source-identity reveal, final interpretation, provider/local-model call, endpoint exposure, or value/readiness claim.
- `ALPHA-SOLVER-NEXT-RELEASE-SELECTOR-AFTER-VALUE-READ-001` (PR #584) - docs-only next-release selector; verdict `NEXT_RELEASE_SELECTION_BLOCKED_PENDING_VALUE_READ_UNBLINDING_AND_FINAL_INTERPRETATION`; selected no implementation lane because locked blind scores remain blinded and uninterpreted.
- `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-AUTHORIZATION-001` (stable post-merge state) - docs-only authorization-decision packet; prepared unblinding/source-identity review and final interpretation authorization language and protocols.
- `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001` (stable post-merge state) - docs-only source-identity review and final bounded interpretation; source identities were reviewed using the operator-provided map, locked scores were not changed, final interpretation exists, claims remain bounded to the manual no-provider prompt-contract simulation, and no release implementation lane is selected.
- `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-ASSET-001` (PR #587) - docs-only discrimination task-bank asset feasibility packet; guarded follow-up deferred, no execution/scoring/runtime/provider/local-model/API/Sheet/readiness/value/superiority claim.
- `ALPHA-SOLVER-DEMO-EVIDENCE-PACKET-TO-DEMO-001` (PR #588) - docs-only claim-safe demo evidence packet feasibility packet; strict evidence-boundary follow-up deferred, no runtime demo/external-use approval/product proof/value/readiness/superiority claim.
- `ALPHA-SOLVER-PARALLEL-FEASIBILITY-GROUP-SYNC-001` (stable post-merge state) - preservation-only source-of-truth sync after tabs 13-16; records PR #581, #587, and #588 as merged and no open source-of-truth doc conflict.
- `ALPHA-SOLVER-NEXT-RELEASE-SELECTOR-AFTER-FINAL-INTERPRETATION-001` (stable post-merge state) - docs-only selector after final interpretation and the parallel feasibility group sync; selects `ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001` for operator review and does not create or implement it.
- `ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001` (merged PR #591) - docs-first substantive derivation / no-echo gate packet; defines criteria, fixture planning, heuristic review aids, stop conditions, non-actions, and non-claims, with no implementation or broad claims.
- `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001` (merged PR #595) - docs-only first cheap-test packet with five representative taxonomy task cards for discrimination task-bank preparation; no task execution, output generation, scoring, raw output inspection, unblinding, source-map work, provider/local-model/runtime/API/Sheet work, dependency addition, release implementation, or broad claims.

- `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001` (merged PR #597) - smoke runner and runbook completed; no smoke execution or quality/readiness claim.
- `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001` (merged PR #598) - docs-only import of Operator-provided, redacted smoke-only results; no behavior quality, readiness, benchmark, production/public, security/privacy, or Alpha-superiority claim.
- `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001` (merged PR #599) - local-only Operator smoke test console; no provider/local-model quality, readiness, benchmark, production/public, security/privacy, or Alpha-superiority claim.
- `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001` (merged PR #600) - local-only test console UX/redaction refinement; no quality, readiness, benchmark, production/public, security/privacy, or Alpha-superiority claim.
- `ALPHA-SOLVER-MODEL-CATALOG-ROUTING-PREVIEW-001` (merged PR #601) - configurable backend model catalog metadata and deterministic routing preview; no provider/local-model execution or quality, readiness, benchmark, production/public, security/privacy, or Alpha-superiority claim.
- `ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001` (merged PR #603) - metadata-only tool catalog and deterministic recommendation preview; no tool execution, browsing, provider/local-model calls, runtime GitHub calls, or quality/readiness/benchmark/production/public/security/privacy/Alpha-superiority claim.
- `ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001` (merged PR #605) - metadata-only model catalog expansion and cost tiers with deterministic routing preview; no provider/local-model execution or quality, readiness, benchmark, production/public, security/privacy, or Alpha-superiority claim.
- `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-METADATA-DISPLAY-001` (prior state) - local-console route-preview metadata display; no provider/local-model/tool execution or quality/readiness/value/superiority claim.
- `ALPHA-SOLVER-CONSOLE-TARGET-PARITY-PRODUCT-PASS-001` (current state) - local-console target-parity product pass; selected next state is `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001`, with no provider/local-model/tool execution or quality/readiness/value/superiority claim.
- `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-METADATA-OPERATOR-REVIEW-PACKET-001` (prior state) - docs/test-support operator review packet; no console execution, operator review performance, provider/local-model/tool execution, or quality/readiness/value/superiority claim.
- `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUTS-001` (stable prior state) - docs-only manual prompt-contract simulation outputs for all 12 routed-vs-plain pilot tasks; no runtime, provider/local-model/tool/web execution, scoring, unblinding, readiness, quality, benchmark, or superiority claim.
- `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001` (stable prior state) - docs-only blinded scorer packet construction; no scoring, unblinding, source identity map commit, runtime, provider/local-model/tool/web execution, readiness, quality, benchmark, or superiority claim.

## Superseded

| Lane / PR | Superseded by | Why |
|-----------|---------------|-----|
| PR #561 - `Add needs-human escalation protocol` | PR #562 | #561 is closed unmerged; #562 merged the docs-only needs-human protocol. |
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

- PR #561 lane as a standalone needs-human protocol PR - closed unmerged and superseded by PR #562.
- Any merged packet lane verbatim - packets are immutable evidence; create a new lane id instead.
- Any selected-next pointer that conflicts with `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUTS_001`. Earlier selected-next pointers, including `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001`, `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RESULTS_IMPORT_001`, `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`, `OPERATOR_REVIEW_REQUIRED_AFTER_DISCRIMINATION_TASK_BANK_FIRST_CHEAP_TEST_001`, `OPERATOR_REVIEW_REQUIRED_AFTER_TOOL_CATALOG_ROUTING_REGISTRY_001`, and `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001`, are prior review states and must not be treated as current.
- Direct Pi.dev integration from PR #574's research lane - the recorded verdict is patterns-only/no-integration.

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
ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001 ← docs-first criteria packet completed; no implementation
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_SUBSTANTIVE_DERIVATION_CHECK_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001 ← docs-only cheap-test packet completed; no execution
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_DISCRIMINATION_TASK_BANK_FIRST_CHEAP_TEST_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001 ← smoke runner and runbook completed; no smoke execution
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001 ← smoke-only results imported; local/Ollama and OpenAI passed
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RESULTS_IMPORT_001 ← prior review-only selected next state
        ↓
ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001 ← local-only smoke console added
        ↓
OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001 ← prior review-only selected next state
        ↓
ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001 ← local-only smoke console UX/redaction refinement
        ↓
OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UX_REDUCTION_001 ← prior review-only selected next state
        ↓
ALPHA-SOLVER-MODEL-CATALOG-ROUTING-PREVIEW-001 ← backend metadata and deterministic routing preview completed
        ↓
OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_PREVIEW_001 ← prior review-only selected next state
        ↓
ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001 ← metadata-only tool catalog and recommendation preview completed
        ↓
OPERATOR_REVIEW_REQUIRED_AFTER_TOOL_CATALOG_ROUTING_REGISTRY_001 ← prior review-only selected next state
        ↓
ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001 ← metadata-only model catalog expansion and cost tiers completed
        ↓
OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001 ← prior review-only selected next state
        ↓
ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001 ← local-only smoke console UI polish
        ↓
OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001 ← local-only metadata route preview integration
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001 ← docs-only routed-vs-plain pilot packet completed
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001 ← prior review-only selected next state
ALPHA-SOLVER-MVP-CUTOVER-REVIEW-001 ← docs-only MVP cutover review completed
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001 ← partial screenshot-only manual review completed
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001 ← docs-only authorization completed
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001 ← output collection prep completed; no pilot outputs recorded
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001 ← prior review-only selected next state
        │
        ▼
ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUTS-001 ← manual prompt-contract simulation outputs recorded; no runtime/provider/local-model/tool/web execution; no scoring/unblinding
ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001 ← blinded scorer packet constructed; no scoring/unblinding/source-map commit
        │
        ▼
OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001 ← current review-only selected next state after packet construction
```

This registry does not authorize production/public UI exposure, dashboard readiness, public provider exposure, local model validation claims, further task execution outside this manual simulation packet, scoring, score change, unblinding, source-map work, raw output inspection, Pi.dev install/run/integration, runtime endpoint exposure, public API exposure, `/v1/solve` exposure, Google Sheets mutation, benchmark, dependency addition, release implementation lane, or readiness/broad-value/security/privacy/provider/local-Ollama/Alpha-superiority claim.

## Local/OpenAI smoke runner lane

| Lane | State | Evidence |
|------|-------|----------|
| `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001` | completed packet / review-only selected next | Adds `tools/operator_smoke_runner.py` and `docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/` so the Operator can explicitly run one local/Ollama smoke check or one OpenAI smoke check with sanitized JSON output. The lane itself does not run smoke checks. |

Prior selected next state after runner lane: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`.

Prior selected next state after test console: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001`.

Prior selected next state after test console UX/redaction refinement: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UX_REDUCTION_001`.

Prior selected next state after model catalog routing preview: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_PREVIEW_001`.

Prior selected next state after model catalog expansion cost tiers: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001`.

Prior selected next state after test console routing preview integration: `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001`.

Prior selected next state after routed-vs-plain blinded scorer packet construction: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001`.

Boundary: no provider quality, local model quality, readiness, benchmark success, production readiness, public readiness, security/privacy completion, UI authorization, or Alpha-superiority claim is created.

- `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001` (merged PR #598) - docs-only import of Operator-provided, redacted smoke-only results: local/Ollama passed using `qwen2.5:3b`, and OpenAI passed using `gpt-4.1-mini-2025-04-14`; no behavior quality, provider quality, local-model quality, readiness, benchmark, production/public, or Alpha-superiority claim.

## ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001

- Packet: `docs/evals/runs/alpha-solver-local-openai-smoke-results-import-001/`
- Lifecycle: completed docs-only evidence import with review-only selected next state.
- Local/Ollama smoke: passed using `qwen2.5:3b`.
- OpenAI smoke: passed using `gpt-4.1-mini-2025-04-14`.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RESULTS_IMPORT_001`.
- Boundary: smoke-only evidence; no behavior quality, provider quality, local-model quality, readiness, benchmark, production/public, or Alpha-superiority claim.


## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001

- Purpose: local-only operator smoke testing console.
- Packet: `docs/evals/runs/alpha-solver-local-openai-test-console-001/`.
- Implementation: `tools/operator_test_console.py`.
- Tests: `tests/test_operator_test_console.py`.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001`.
- Evidence boundary: console implementation only, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim.

- `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001` (merged PR #600) - local-only test console UX/redaction refinement. Purpose: preserve submitted form state after console runs and avoid over-redacting safe usage token counts. Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UX_REDUCTION_001`. Boundary: no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim.

## ALPHA-SOLVER-MODEL-CATALOG-ROUTING-PREVIEW-001

| Field | Value |
|-------|-------|
| Status | completed backend implementation / review-only selected next |
| Purpose | Add configurable model catalog metadata and deterministic routing preview backend. |
| Packet | `docs/evals/runs/alpha-solver-model-catalog-routing-preview-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_PREVIEW_001` |
| Evidence boundary | Routing preview only; no provider/local-model calls; no quality, readiness, benchmark, production/public, security/privacy, Alpha-superiority, partnership/Pi.dev integration, buyer-validation, or traction claim. |

## ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001

- Artifact: `alpha/tool_catalog.py`, `alpha/tool_router.py`, and `configs/tool_catalog.json`
- Packet: `docs/evals/runs/alpha-solver-tool-catalog-routing-registry-001/`
- Purpose: add metadata-only tool catalog and deterministic recommendation preview.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_TOOL_CATALOG_ROUTING_REGISTRY_001`.
- Evidence boundary: recommendation preview only, no tool execution, no browsing, no provider/local-model calls, no runtime GitHub calls, no quality/readiness/benchmark/production/public/security/privacy/Alpha-superiority claim.


## ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001

| Field | Value |
| --- | --- |
| Status | completed backend metadata implementation / review-only selected next |
| Evidence packet | `docs/evals/runs/alpha-solver-model-catalog-expansion-cost-tiers-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001` |
| Boundary | Metadata-only model catalog and routing preview; no provider/local model execution and no quality/readiness/benchmark claim. |

## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001

- Purpose: improve local-only console usability with model dropdowns, a prompt counter, a friendly result display, and a copyable sanitized JSON panel.
- Packet: `docs/evals/runs/alpha-solver-local-openai-test-console-ui-polish-001/`.
- Implementation: `tools/operator_test_console.py`.
- Tests: `tests/test_operator_test_console.py`.
- Builds on baseline: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001`.
- Selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001`.
- Evidence boundary: UI polish only, no model catalog or tool catalog logic change, and no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim.

## ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001

| Field | Value |
|-------|-------|
| Status | completed local-only console integration / review-only selected next |
| Packet | `docs/evals/runs/alpha-solver-test-console-routing-preview-integration-001/` |
| Changed implementation | `tools/operator_test_console.py`; `tests/test_operator_test_console.py` |
| Preserved history | `ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001`; `ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001`; `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001` |
| Boundary | metadata-only route preview; no provider/local-model execution, no tool execution, no browsing, no runtime GitHub calls, no `/v1/solve` exposure, no dependencies, no persistence, no telemetry, and no readiness/quality/benchmark/production/public/security/privacy/provider/local-model/tool-quality/Alpha-superiority claim |


## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001

| Field | Value |
|-------|-------|
| Status | completed docs-only pilot packet / review-only selected next |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-packet-001/` |
| Preserved history | `ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001`; `ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001`; `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001`; `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001` |
| Boundary | packet only; no pilot execution, provider/local/hosted model execution, tool execution, browsing, output generation, scoring, score change, unblinding, raw output inspection, source-map work, Google Sheets mutation, dependency addition, `/v1/solve` exposure, dashboard/public API behavior, or readiness/benchmark/production/public/security/privacy/provider/local-model/tool-quality/Alpha-superiority claim |


## ALPHA-SOLVER-MVP-CUTOVER-REVIEW-001

| Field | Value |
|-------|-------|
| Status | completed docs-only review |
| Packet | `docs/evals/runs/alpha-solver-mvp-cutover-review-001/` |
| Verdict | `LOCAL_OPERATOR_MVP_CANDIDATE_READY_FOR_MANUAL_REVIEW` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` |
| Boundary | No provider/local-model/tool/pilot execution, output generation, scoring, unblinding, raw-output inspection, source-map work, dependency addition, Google Sheets mutation, `/v1/solve` exposure, dashboard/public API exposure, deployment, production/public readiness, benchmark, provider/local-model/tool-quality, security/privacy completion, autonomous-readiness, or Alpha-superiority claim. |

## ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001

| Field | Value |
|-------|-------|
| Status | completed partial docs-only manual review |
| Packet | `docs/evals/runs/alpha-solver-local-mvp-manual-review-001/` |
| Verdict | `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` |
| Boundary | Screenshot-only operator-provided evidence; no full manual review pass, provider/local-model/tool/pilot execution, output generation, scoring, unblinding, source-map work, dependency addition, Google Sheets mutation, `/v1/solve` exposure, runtime/router/console/config/test change, production/public readiness, benchmark validation, provider/local-model/tool-quality, security/privacy completion, autonomous-readiness, or Alpha-superiority claim. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001

| Field | Value |
|-------|-------|
| Status | completed docs-only authorization packet |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-authorization-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001` |
| Boundary | Authorizes only future operator-reviewed output collection under the packet protocol; provider/local/model/tool/web execution, scoring, unblinding, raw prior-output inspection, Sheets mutation, dependency addition, `/v1/solve` exposure, and readiness/benchmark/quality/superiority claims remain unauthorized. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001

| Field | Value |
|-------|-------|
| Status | completed output collection preparation packet |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-output-collection-prep-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001` |
| Evidence value | Records blank templates for 12 task IDs for `RVP-001` through `RVP-012`, with one plain baseline output, one routed Alpha output, and route metadata per task. |
| Boundary | Manual simulation only; no Alpha runtime, `/v1/solve`, provider API, hosted model, local model, tool execution, web/current research, scoring, unblinding, Sheet mutation, benchmark, readiness, quality, security/privacy completion, autonomous-readiness, or Alpha-superiority evidence. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUTS-001

| Field | Value |
|-------|-------|
| Status | completed manual prompt-contract simulation output packet / review-only selected next |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-outputs-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUTS_001` |
| Evidence value | Records one manual plain output, one manual routed Alpha output, and one route metadata record for each `RVP-001` through `RVP-012`. |
| Boundary | Manual prompt-contract simulation artifacts only; no Alpha runtime, `/v1/solve`, provider API, hosted model, local model, tool execution, web/current research, scoring, unblinding, source-map work, Sheet mutation, benchmark, readiness, production/public, quality, security/privacy completion, autonomous-readiness, or Alpha-superiority evidence. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001

| Field | Value |
| --- | --- |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-blinded-scorer-packet-construction-001/` |
| Status | completed pending PR |
| Boundary | Docs-only blinded scorer packet construction; no scoring, unblinding, source identity map commit, runtime/provider/local-model/tool/web execution, readiness, quality, benchmark, or Alpha-superiority claim. |


## ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-AUTHORIZATION-001

| Field | Value |
|-------|-------|
| Status | completed docs-only authorization/prep packet |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-blind-scoring-pass-authorization-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_AUTHORIZATION_001` |
| Evidence value | Prepares operator review materials for a future blind scoring pass using the PR #619 scorer-facing packet; includes authorization language, scoring protocol, blank score-entry template, score-lock protocol, custody rules, stop conditions, non-actions, non-claims, and checks documentation. |
| Boundary | No scoring, score filling, winner selection, aggregate computation, unblinding, interpretation, A/B key inspection or commit, source-map inspection or commit, source artifact inspection for scoring, runtime/provider/local-model/tool/web execution, Sheets mutation, dependencies, deployment, readiness, benchmark, value, or Alpha-superiority claim. |



## ALPHA-SOLVER-MODEL-CATALOG-ROUTING-METADATA-EXPANSION-001

| Field | Value |
|---|---|
| Status | completed product-foundation lane |
| Packet | `docs/evals/runs/alpha-solver-model-catalog-routing-metadata-expansion-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_METADATA_EXPANSION_001` |
| Boundary | Static catalog metadata and deterministic route preview only; no runtime behavior, `/v1/solve`, providers, hosted/local models, Ollama, tools, browsing, Sheets mutation, scoring, unblinding, A/B key inspection, source-map inspection, readiness/value/benchmark/quality/production/public/security/privacy/autonomous-readiness/Alpha-superiority claim. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-001

| Field | Value |
|---|---|
| Status | completed locked blind scoring pass |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-blind-scoring-pass-001/` |
| Task count | 12 tasks scored: `RVP-001` through `RVP-012` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_AUTHORIZATION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_001` |
| Boundary | Blind scoring only; no unblinding, source identity review, source-map review, A/B key inspection, source artifact inspection, route metadata inspection, runtime/provider/local-model/tool/web execution, Google Sheets mutation, final interpretation, readiness/value/benchmark/production/public/provider/local-model/tool/security/privacy/autonomous-readiness/Alpha-superiority claim. |


## ALPHA-SOLVER-CONSOLE-TARGET-PARITY-PRODUCT-PASS-001

Completed local-console product-foundation lane. Evidence packet: `docs/evals/runs/alpha-solver-console-target-parity-product-pass-001/`. Selected next state: `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001`.
