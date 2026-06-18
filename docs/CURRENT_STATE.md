# Alpha Solver - Current State

> Source-of-truth navigation doc. Last verified **2026-06-18** for routed-vs-plain blind scoring pass.
> This lane records locked blind scoring of the routed-vs-plain scorer-facing packet. It does not run Alpha runtime, invoke `/v1/solve`, call providers, run hosted or local models, execute tools, browse, unblind, inspect source identities, inspect route metadata, mutate Sheets, deploy, interpret final results, or make production/public/benchmark/provider/local-model/tool/security/privacy/autonomous-readiness/Alpha-superiority claims.

## Current verified phase

**Routed-vs-plain blind scoring pass completed: the selected next state is operator review of locked blind scores before any unblinding or final interpretation lane.**

The merged #569–#574 wave updated the repository from the post-#568 blocked Value Read state to a broader documentation-and-boundary posture. PR #576 was superseded by PR #577 and should be closed unmerged. PR #577 completes `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` as a docs-only Alpha-native local operator harness design note.

The previous Value Read control posture was `OPERATOR_REVIEW_REQUIRED_AFTER_VALUE_READ_UNBLINDING_FINAL_INTERPRETATION_PASS_001`: `ALPHA-SOLVER-VALUE-READ-UNBLINDING-FINAL-INTERPRETATION-PASS-001` completed as a docs-only evidence interpretation lane. Source identities were reviewed using an operator-provided map, locked scores were not changed, and the final interpretation remains bounded to the manual no-provider prompt-contract simulation. No release implementation lane is selected by this pass.

These are docs, gate, helper, static/research, blocked-attempt, scoring-only, selector, authorization-preparation, and bounded interpretation artifacts. They do not prove provider behavior, model quality, broad value, readiness, benchmark success, security/privacy completion, local Ollama validation, `/v1/solve` readiness, production/public readiness, or Alpha superiority.

## At a glance

| Field | Value |
|-------|-------|
| Latest verified completed lane in this wave | **`ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-001`** |
| Source-of-truth sync | Current docs record the completed routed-vs-plain blind scoring pass lane and a review-only selected next state before any unblinding or final interpretation |
| Closed-unmerged superseded PR | **#561** - superseded by merged PR #562 |
| Current controlling posture | Operator review required after routed-vs-plain locked blind scoring pass |
| Selected next state | **`OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_001`** |
| Strategic boundary | This review-only state records locked blind scores only; it does not prove runtime, `/v1/solve`, provider, hosted-model, local-model, tool, web, benchmark, production/public readiness, security/privacy, quality, autonomous-readiness, or Alpha-superiority claims and does not authorize unblinding or interpretation |

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
| smoke-runner lane | `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001` | Adds `tools/operator_smoke_runner.py` and the operator packet for explicit local/Ollama or OpenAI smoke checks; the merged runner lane did not run either smoke and proves no provider quality, local model quality, readiness, benchmark success, production readiness, public readiness, or Alpha superiority. |
| smoke-results-import lane | `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001` | Imports Operator-provided, redacted smoke-only results showing local/Ollama passed using `qwen2.5:3b` and OpenAI passed using `gpt-4.1-mini-2025-04-14`; proves no behavior quality, provider quality, local-model quality, readiness, benchmark success, production/public readiness, or Alpha superiority. |
| test-console lane | `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001` | Adds a local-only Operator console for bounded local/Ollama and OpenAI smoke checks through the existing smoke runner path; proves no behavior quality, provider quality, local-model quality, readiness, benchmark success, production/public readiness, security/privacy completion, or Alpha superiority. |
| test-console-ux-redaction lane | `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001` | Preserves submitted form state after console runs and avoids over-redacting safe numeric usage token counts; proves no behavior quality, provider quality, local-model quality, readiness, benchmark success, production/public readiness, security/privacy completion, or Alpha superiority. |
| model-catalog-routing-preview lane | `ALPHA-SOLVER-MODEL-CATALOG-ROUTING-PREVIEW-001` | Adds configurable backend model catalog metadata and deterministic routing preview; performs no provider/local-model calls and proves no quality, readiness, benchmark, production/public, security/privacy, or Alpha-superiority claim. |
| tool-catalog-routing-registry lane | `ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001` | Adds metadata-only tool catalog and deterministic recommendation preview; performs no tool execution, browsing, provider/local-model calls, runtime GitHub calls, dependency addition, endpoint exposure, scoring, unblinding, source-map work, raw-output inspection, readiness/quality/security/privacy/production/public/provider/local-model/tool-quality/Alpha-superiority claim. |
| model-catalog-expansion lane | `ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001` | Expands metadata-only model catalog fields and deterministic routing preview warnings/fallbacks; performs no provider/local-model execution and proves no quality, readiness, benchmark, production/public, security/privacy, or Alpha superiority. |
| test-console-ui-polish lane | `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001` | Polishes the local-only console UI with mode and model dropdowns, a prompt counter and 500-character limit warning, a friendly result display, and a copyable sanitized JSON panel; modifies no model catalog or tool catalog logic and proves no behavior quality, provider quality, local-model quality, readiness, benchmark success, production/public readiness, security/privacy completion, or Alpha superiority. |
| test-console-routing-preview lane | `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001` | Wires the local-only Operator console to metadata-only model/tool route preview before separate smoke execution; proves no provider/local-model/tool quality, readiness, benchmark, production/public, security/privacy, or Alpha superiority. |
| routed-vs-plain pilot packet lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001` | Creates a docs-only routed-vs-plain pilot packet with task cards, rubric, comparison protocol, blank result template, runbook, stop conditions, non-actions, and non-claims; runs no pilot and generates no outputs or scores. |
| MVP cutover review lane | `ALPHA-SOLVER-MVP-CUTOVER-REVIEW-001` | Records a STOP / go-no-go review with verdict `LOCAL_OPERATOR_MVP_CANDIDATE_READY_FOR_MANUAL_REVIEW`; creates no provider/local-model/tool/pilot execution, output generation, scoring, readiness, benchmark, production/public, security/privacy completion, tool-quality, autonomous-readiness, or Alpha-superiority evidence. |
| local MVP manual review lane | `ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001` | Records operator-provided screenshot-only partial manual review evidence with verdict `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST`; full manual UI testing remains deferred, and no provider/local-model/tool/pilot execution or quality/readiness claim occurs. |
| routed-vs-plain pilot authorization lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001` | Completes a docs-only authorization packet for a future routed-vs-plain output-collection lane; it defines the task set, output collection method, plain baseline identity, routed Alpha identity, execution permission boundaries, task-id preservation, route metadata capture, blinding, scoring authorization gate, stop conditions, evidence boundaries, non-actions, and non-claims. Provider calls, hosted-model calls, local-model calls, tool execution, and web/current research are not authorized by this packet; later collection must use operator-provided outputs unless separately authorized. |
| routed-vs-plain pilot output collection prep lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001` | Records 12 blank operator-fillable capture templates for `RVP-001` through `RVP-012`, including blank fields for plain baseline outputs, routed Alpha outputs, and route metadata. This is not Alpha runtime, `/v1/solve`, provider, hosted-model, local-model, tool-execution, web/current research, scoring, unblinding, benchmark, readiness, quality, or superiority evidence. |
| routed-vs-plain pilot manual output collection lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUTS-001` | Records manual prompt-contract simulation outputs for all 12 routed-vs-plain pilot tasks, with one plain output, one routed output, and one metadata record per task. This is not runtime, `/v1/solve`, provider, hosted/local-model, tool, web/current research, scoring, unblinding, benchmark, readiness, quality, or superiority evidence. |
| routed-vs-plain blinded scorer packet construction lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001` | Constructs a source-neutral scorer-facing blinded packet for all 12 routed-vs-plain tasks, freezes blank scoring/preference/rationale fields, and keeps the A/B identity key out of the repository. This is not scoring, unblinding, runtime, `/v1/solve`, provider/local-model/tool/web execution, benchmark, readiness, quality, or superiority evidence. |

| routed-vs-plain blind scoring pass authorization lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-AUTHORIZATION-001` | Completes a docs-only authorization/prep packet for a future blind scoring pass using the PR #619 scorer-facing packet; scoring remains unauthorized until a later operator-authorized scoring lane. |

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for the PR status ledger and [`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lifecycle classification.

## Selected next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_001`** is the current global selected next state.

This is a review-only state after `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-001`. The prior selected next state was `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_AUTHORIZATION_001`. The lane records locked blind scores, blind preferences, rationales, caveats, contested-score flags, scorer method, scoring timestamps, score-lock confirmation, custody notes, non-actions, and non-claims for the scorer-facing packet. It does not run Alpha runtime, invoke `/v1/solve`, call providers, run hosted or local models, execute tools, browse, use current external research, mutate Sheets, add dependencies, unblind, inspect answer identities, interpret final results, inspect or commit an A/B key, inspect or commit source maps, deploy, or make readiness, benchmark, production/public, provider-quality, local-model-quality, tool-quality, security/privacy, autonomous-readiness, or Alpha-superiority claims.

The prior state was a review-only state after `ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001`. The prior selected next state was `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001`. The review verdict is `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST` based only on operator-provided screenshot observations. It does not claim a full local MVP manual review pass. The next action may proceed to routed-vs-plain pilot authorization because that next lane is docs-only and does not require UI testing to execute. Full manual UI testing remains deferred before any broader user-testing, production/public readiness, benchmark, provider-quality, local-model-quality, tool-quality, security/privacy completion, autonomous execution readiness, or Alpha-superiority claim. This state does not run providers, hosted models, local models, tools, the routed-vs-plain pilot, output generation, scoring, unblinding, raw output inspection, source-map work, dependency installation, Google Sheets mutation, `/v1/solve`, dashboard/public API behavior, or deployment.

The prior state was a review-only state after `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001`. The prior selected next state was `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001`. It means the repository now contains a static routed-vs-plain pilot packet for future operator review only: the pilot was not executed; no provider or local-model calls occurred; no tools were executed; no browsing occurred; no Alpha outputs or baseline outputs were generated; no scoring, unblinding, raw output inspection, or source-map work occurred; no Google Sheets mutation occurred; and `/v1/solve` was not exposed or invoked. The state makes no readiness, benchmark, production/public, provider, local-model, tool-quality, security/privacy, or Alpha-superiority claims. The prior selected next state after UI polish was `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001`.

This state authorizes no production/public exposure, no task execution outside explicit local Operator submission, no output generation for evals, scoring, score change, source-map work, unblinding, raw Alpha output inspection, raw baseline output inspection, `/v1/solve` exposure, dashboard/public API exposure, Google Sheets mutation, benchmark work, release behavior, readiness claim, broad value claim, provider claim, local-model claim, security/privacy claim, production/public claim, partnership/Pi.dev integration claim, demo external-use approval, discrimination-task execution/scoring, or Alpha-superiority claim.

## Open deferrals (see [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md))

- **DEF-001** - Self Operator execution evidence: substantially advanced within local-only scope; does not prove provider/runtime readiness.
- **DEF-002** - Product security/privacy review: open; `/v1/solve` exposure remains blocked by PR #571.
- **DEF-003** - Prior Fable delta-audit custody/replacement: open.
- **DEF-004** - Audit custody/provenance: open unless repo evidence shows otherwise.

## What is blocked / not authorized

- New provider calls, hosted model calls, local model calls, token use, credential access, billing inspection, dashboard exposure, `/v1/solve` exposure, public API exposure, Pi.dev installation/execution/integration, package-install experiments, and Google Sheets mutation.
- Release implementation lanes and broad Alpha-vs-baseline claims. The earlier Value Read bounded manual no-provider pilot has locked blind scores and a final interpretation, but this pass selects no release implementation lane and does not support claims beyond the 10-case manual no-provider prompt-contract simulation.
- Local Ollama validation claims. PR #573 records a failed-closed local timeout/backend error and no local model answer.
- Not authorized: security/privacy completion, production readiness, public MVP readiness, benchmark validation/superiority, broad-user readiness, autonomous readiness, provider validation, local Ollama validation, `/v1/solve` readiness, dashboard readiness, or Alpha superiority.

## What must not be claimed

This phase does **not** support claims of broad value, OpenAI validation, provider validation, local Ollama validation, Pi.dev integration, runtime readiness, production readiness, public MVP readiness, security/privacy completion, DEF-002 resolved, DEF-003 resolved, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, dashboard readiness, Google Sheets synchronization, or Alpha superiority.


## ALPHA-SOLVER-MVP-CUTOVER-REVIEW-001

- Packet: `docs/evals/runs/alpha-solver-mvp-cutover-review-001/`
- Evidence type: docs-only STOP / go-no-go local operator MVP candidate cutover review.
- Verdict: `LOCAL_OPERATOR_MVP_CANDIDATE_READY_FOR_MANUAL_REVIEW`.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001`.
- Selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001`.
- Boundary: manual-review candidate only; no provider/local-model/tool/pilot execution, output generation, scoring, unblinding, source-map work, dependency addition, `/v1/solve` exposure, dashboard/public API exposure, deployment, production/public readiness, benchmark, provider/local-model/tool-quality, security/privacy completion, autonomous-readiness, or Alpha-superiority evidence.

## ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001

- Packet: `docs/evals/runs/alpha-solver-local-openai-smoke-results-import-001/`
- Evidence type: Operator-provided, redacted smoke-only result import.
- Local/Ollama smoke result: passed using `qwen2.5:3b`.
- OpenAI smoke result: passed using `gpt-4.1-mini-2025-04-14`.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RESULTS_IMPORT_001`.
- Boundary: does not prove behavior quality, provider quality, local-model quality, readiness, benchmark success, production readiness, public readiness, security/privacy completion, buyer validation, traction, partnership/Pi.dev integration, or Alpha superiority.


## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001

- Packet: `docs/evals/runs/alpha-solver-local-openai-test-console-001/`
- Evidence type: Local-only Operator smoke test console implementation.
- Console: `tools/operator_test_console.py`.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001`.
- Boundary: console implementation only, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim.


## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001

- Packet: `docs/evals/runs/alpha-solver-local-openai-test-console-ux-reduction-001/`
- Evidence type: Local-only Operator smoke test console UX/redaction refinement.
- Purpose: preserve submitted form state after console runs and avoid over-redacting safe usage token counts.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UX_REDUCTION_001`.
- Boundary: UX/redaction refinement only, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim.

## ALPHA-SOLVER-MODEL-CATALOG-ROUTING-PREVIEW-001

- Artifact: `alpha/model_catalog.py`, `alpha/model_router.py`, and `configs/model_catalog.json`
- Packet: `docs/evals/runs/alpha-solver-model-catalog-routing-preview-001/`
- Evidence type: backend metadata and deterministic routing preview only.
- Provider/local execution status: not run by this lane.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_PREVIEW_001`.
- Boundary: does not prove provider quality, local model quality, readiness, benchmark success, production readiness, public readiness, security/privacy completion, buyer validation, traction, partnership/Pi.dev integration, or Alpha superiority.

## ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001

- Artifact: `alpha/tool_catalog.py`, `alpha/tool_router.py`, and `configs/tool_catalog.json`
- Packet: `docs/evals/runs/alpha-solver-tool-catalog-routing-registry-001/`
- Evidence type: metadata-only tool catalog and deterministic recommendation preview only.
- Tool execution status: not run by this lane.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_TOOL_CATALOG_ROUTING_REGISTRY_001`.
- Boundary: recommendations such as Python/computation, web/current research, or GitHub/code are metadata-only preview outputs, not execution, browsing, provider calls, GitHub runtime calls, file mutation, readiness evidence, tool-quality evidence, or Alpha-superiority evidence.


## ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001

- Status: completed backend metadata implementation / review-only selected next.
- Evidence packet: `docs/evals/runs/alpha-solver-model-catalog-expansion-cost-tiers-001/`.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001`.
- Boundary: metadata-only routing preview; no provider or local model execution, no quality/readiness/benchmark claim, no public API or dashboard behavior, no `/v1/solve`, and no Google Sheets mutation.

## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001

- Packet: `docs/evals/runs/alpha-solver-local-openai-test-console-ui-polish-001/`
- Evidence type: Local-only Operator smoke test console UI polish.
- Purpose: improve local-only console usability with model dropdowns, a prompt counter, a friendly result display, and a copyable sanitized JSON panel.
- Builds on baseline: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001`.
- Selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001`.
- Boundary: UI polish only, no model catalog or tool catalog logic change, and no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim.

## ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001

- Packet: `docs/evals/runs/alpha-solver-test-console-routing-preview-integration-001/`
- Evidence type: local-only Operator console routing-preview integration.
- Console: `tools/operator_test_console.py`.
- Builds on baseline: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001`.
- Selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001`.
- Boundary: metadata-only route preview before separate smoke execution; no provider/local-model execution, no tool execution, no browsing, no runtime GitHub calls, no `/v1/solve` exposure, no persistence/telemetry/dependency addition, and no quality/readiness/benchmark/public/production/security/privacy/provider/local-model/tool-quality/Alpha-superiority claim.


## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001

- Packet: `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-packet-001/`
- Evidence type: docs-only routed-vs-plain pilot packet.
- Purpose: prepare later operator review of whether route metadata and routing discipline create value beyond a plain single-model answer.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001`.
- Selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001`.
- Boundary: does not execute the pilot, call providers, run hosted/local models, execute tools, browse, generate Alpha or baseline outputs, score outputs, change scores, unblind, inspect raw outputs, perform source-map work, mutate Google Sheets, add dependencies, expose `/v1/solve`, expose dashboard/public API behavior, or make readiness/benchmark/production/public/security/privacy/provider/local-model/tool-quality/Alpha-superiority claims.

## ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001

| Field | Value |
|-------|-------|
| Status | completed partial docs-only manual review |
| Packet | `docs/evals/runs/alpha-solver-local-mvp-manual-review-001/` |
| Verdict | `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` |
| Boundary | Screenshot-only operator-provided evidence; full manual UI testing remains deferred before broader user-testing, production/public readiness, benchmark, provider-quality, local-model-quality, tool-quality, security/privacy completion, autonomous execution readiness, or Alpha-superiority claims. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001

- Packet: `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-output-collection-prep-001/`
- Evidence type: manual no-provider prompt-contract simulation output capture.
- Scope: 12 task pairs for `RVP-001` through `RVP-012`, with one plain baseline output and one routed Alpha output per task plus route metadata.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001`.
- Selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001`.
- Boundary: not Alpha runtime, `/v1/solve`, provider, hosted-model, local-model, tool-execution, web/current research, scoring, unblinding, benchmark, production/public readiness, quality, security/privacy completion, autonomous-readiness, or Alpha-superiority evidence.
