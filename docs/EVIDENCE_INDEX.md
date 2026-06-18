# Evidence Index - test console routing metadata operator review packet

> Source-of-truth evidence ledger. Verification date **2026-06-18** after console target-parity product pass lane `ALPHA-SOLVER-CONSOLE-TARGET-PARITY-PRODUCT-PASS-001`.

## How to read "evidence value"

The entries below are design, documentation, gate, helper, static-checking, methodology, blocked-attempt, or research evidence. They are not provider validation, local-model validation, value evidence, benchmark evidence, production readiness evidence, security/privacy completion evidence, `/v1/solve` readiness evidence, Pi.dev integration evidence, or Alpha-superiority evidence.

## PR table

| PR | Title | Merged / status | Primary artifact | Evidence value | Non-claims | Lifecycle |
|----|-------|-----------------|------------------|----------------|------------|-----------|
| #557 | Add post-552 no-echo substantive generation gate | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001.md`; `docs/evals/runs/alpha-solver-no-echo-substantive-generation-gate-post-552-successor-001/` | Records a substantive-generation / no-echo gate after the post-552 sequence. | Does not prove model quality, provider behavior, or value. | completed |
| #558 | Add false-premise & hidden-constraint perturbation case set for Value Read | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001.md` | Adds future Value Read perturbation material for false-premise and hidden-constraint handling. | Does not run an eval, call a model, or prove robustness. | completed |
| #559 | Add narrative claim-safety linter | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001.md`; `docs/evals/runs/alpha-solver-narrative-claim-safety-linter-001/` | Adds claim-safety linting infrastructure for unsupported narrative claims. | Does not certify all docs, security/privacy, readiness, or claim safety globally. | completed |
| #560 | Add calibrated-confidence output contract for Alpha Solver | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001.md` | Defines answerability, confidence, non-claims, evidence gaps, assumptions, false-premise risk, hidden-constraint risk, and next-safe-action vocabulary. | Does not prove runtime enforcement or calibrated model behavior. | completed |
| #561 | Add needs-human escalation protocol | ❌ closed unmerged | superseded by #562 | No merged evidence artifact from this PR. | Must not be cited as merged implementation/evidence. | superseded |
| #562 | Add needs-human escalation protocol (docs-only) | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001.md`; `docs/evals/runs/alpha-solver-escalation-needs-human-protocol-001/` | Records docs-only protocol guidance for needs-human outcomes. | Does not prove runtime escalation, `/v1/solve` behavior, or human-review operations. | completed |
| #563 | Add higher-headroom Value Read case set (design-only) | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001.md`; `docs/evals/HIGHER_HEADROOM_VALUE_READ_CASE_SET.md` | Adds higher-headroom synthetic Value Read candidate cases. | Does not score outputs, prove lift, or establish benchmark success. | completed |
| #564 | Add prompt-contract simulation methodology | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-prompt-contract-simulation-methodology-001/` | Records methodology for prompt-contract simulation. | Does not execute a simulation, call providers, or prove value. | completed |
| #565 | Add local Ollama singlepath lab lane | ✅ merged 2026-06-15 | `.specs/ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001.md`; `docs/evals/runs/alpha-solver-local-model-lab-ollama-singlepath-001/` | Records a local-only Ollama singlepath lab scaffold. | Does not run Ollama, run a local model, validate a provider, expose an API, or prove readiness. | completed |
| #566 | Post-565 Value Read simulation packet refresh | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-value-read-simulation-packet-refresh-post-565-001/` | Refreshes the packet lane for post-565 infrastructure. | Does not prove value, run providers/models, or score outputs. | completed |
| #567 | Value Read packet follow-up / pre-run state | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-value-read-simulation-packet-refresh-post-565-001/` | Commits the packet state inspected by the manual-run artifact. | Does not itself prove value or readiness. | completed |
| #568 | Manual Value Read simulation run artifact - stopped | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-value-read-simulation-packet-refresh-post-565-001/manual-run-artifact-2026-06-15.md` | Records `VALUE_READ_BLOCKED`: stopped before output generation and scoring; no Alpha/baseline outputs, blind scores, or discrimination-delta. | Does not claim Alpha value, superiority, provider/local/runtime behavior, endpoint/dashboard/public API behavior, Google Sheets mutation, external ledger mutation, MVP validation, or readiness. | blocked evidence |
| #569 | Record PR #568 as VALUE_READ_BLOCKED and update MVP scorecard + docs; select controlled execution next lane | ✅ merged 2026-06-15 | `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Refreshes source-of-truth docs for the blocked Value Read state after #568. | Does not create Value Read success, provider/runtime readiness, or Sheet synchronization evidence. | completed |
| #570 | Add post-#568 founder memo refresh | ✅ merged 2026-06-15 | founder memo documentation | Refreshes narrative positioning for the blocked Value Read state. | Does not prove value, readiness, or superiority. | completed |
| #571 | docs: add v1 solve exposure gate packet (BLOCKED) | ✅ merged 2026-06-15 | `docs/evals/runs/14-v1-solve-exposure-gate/README.md` | Records `/v1/solve` public exposure as `BLOCKED` pending auth, tenancy, logging, redaction, rate-limit, CORS/ingress, monitoring, incident-response, rollback, and authorization closure. | Does not expose `/v1/solve` or prove runtime/public/security/privacy readiness. | blocked evidence |
| #572 | Add local Ollama singlepath operator helper | ✅ merged 2026-06-15 | `scripts/run_local_ollama_singlepath_operator.sh`; local-lab packet docs | Adds an operator helper for the local-only Ollama lane. | Helper existence is not a successful local model run, quality proof, benchmark, or readiness evidence. | completed |
| #573 | Record blocked local Ollama singlepath attempt | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-local-model-lab-ollama-singlepath-001/local-run-artifact-2026-06-15.md` | Records exact `gemma3:4b` preflight success followed by failed-closed timeout/backend error; no local model answer was generated. | Does not prove local model quality, local Ollama validation, Value Read success, runtime readiness, or Alpha superiority. | blocked evidence |
| #574 | Add pi.dev harness feasibility research note | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-pi-dev-harness-feasibility-018/README.md` | Records `BORROW_PATTERNS_ONLY_NO_INTEGRATION` for Pi.dev harness research. | Does not install, run, or integrate Pi.dev; does not authorize providers, package installs, runtime exposure, or readiness claims. | completed |
| #576 | Add Alpha-native local operator harness design note | closed unmerged / superseded by #577 | superseded by #577 | No merged evidence artifact from #576. | Must not be cited as the merged completion artifact for this lane. | superseded |
| #577 | Add Alpha-native local operator harness design note | ✅ merged 2026-06-15 | `docs/evals/runs/alpha-solver-local-operator-harness-design-note-001/` | Docs-only Alpha-native local operator harness design note. | Does not prove implementation, runtime behavior, UI readiness, provider behavior, local model behavior, Pi.dev integration, Value Read success, benchmark success, production readiness, public readiness, security/privacy completion, or Alpha superiority. | completed |
| post-577 lane | docs: prepare post-577 Value Read execution authorization decision | completed | `docs/evals/runs/alpha-solver-value-read-execution-authorization-decision-post-577-001/` | Docs-only authorization-decision packet for operator review before the manual pilot was authorized. | Does not itself perform output generation, scoring, unblinding, provider calls, local model runs, runtime endpoints, dashboard/public API exposure, Google Sheets mutation, benchmarks, readiness claims, value claims, provider claims, local-model claims, security/privacy claims, or Alpha-superiority claims. | completed |
| post-578 lane | docs: run manual Value Read output-generation pilot post-578 | completed | `docs/evals/runs/alpha-solver-value-read-manual-output-generation-pilot-post-578-001/` | Generates raw Alpha-style and raw plain-baseline outputs for 10 committed synthetic Value Read cases as manual no-provider prompt-contract simulation documentation artifacts only. | Does not score, fill blind scores, unblind, interpret, call providers, run local models, use runtime endpoints, expose dashboard/public API, mutate Google Sheets, prove value/readiness/provider/local-model behavior, or show Alpha superiority. | completed |
| post-579 lane | docs: construct blind scoring packet post-579 | completed | `docs/evals/runs/alpha-solver-value-read-blind-scoring-packet-construction-post-579-001/` | Constructs a blinded scorer packet for the 10-case post-578 manual no-provider raw-output pilot and freezes blank scoring dimensions for a future separately authorized scoring review. | Does not score, fill blind scores, unblind, interpret, call providers, run local models, use runtime endpoints, expose dashboard/public API, mutate Google Sheets, prove value/readiness/provider/local-model behavior, or show Alpha superiority. The unblinding map is not committed. | completed |
| post-blind-packet lane | docs: prepare Value Read scoring review authorization | completed | `docs/evals/runs/alpha-solver-value-read-scoring-review-authorization-post-blind-packet-001/` | Prepares exact future operator scoring authorization language, a blank score-output template using frozen rubric dimensions, score-review protocol, stop conditions, non-actions, non-claims, and selected-next review state. | Does not score, fill blind scores, unblind, interpret, call providers, run local models, use runtime endpoints, expose dashboard/public API, mutate Google Sheets, prove value/readiness/provider/local-model behavior, or show Alpha superiority. | completed |
| post-581 lane | docs: score blinded Value Read packet post-581 | completed | `docs/evals/runs/alpha-solver-value-read-blind-scoring-pass-post-581-001/` | Records the scoring-only blinded review pass with case-level scores, notes, contested-score flags, scorer identity/tool, scoring method, scoring timestamp, and score-lock confirmation. | Does not unblind, perform final interpretation, call providers, run local models, use runtime endpoints, expose dashboard/public API, mutate Google Sheets, prove value/readiness/provider/local-model behavior, prove benchmark results, or show Alpha superiority. | completed |
| scorecard-after-score lane | docs: update MVP scorecard after Value Read score state | completed | `docs/evals/runs/alpha-solver-mvp-scorecard-after-value-read-score-001/` | Records that locked blind scores now exist for scorecard score-state tracking, and that final score interpretation remains blocked pending separate operator authorization. | Does not change scores, unblind, reveal source identities, perform final interpretation, call providers, run local models, use runtime endpoints, expose dashboard/public API, mutate Google Sheets, prove value/readiness/provider/local-model behavior, prove benchmark results, or show Alpha superiority. | completed |
| #584 | docs: add next-release selector after Value Read (block selection) | merged | `docs/evals/runs/alpha-solver-next-release-selector-after-value-read-001/` | Records docs-only next-release selector verdict `NEXT_RELEASE_SELECTION_BLOCKED_PENDING_VALUE_READ_UNBLINDING_AND_FINAL_INTERPRETATION`; selects no implementation lane because locked blind scores remain blinded and uninterpreted. | Does not authorize unblinding, final interpretation, providers, local models, runtime work, dashboard/public API work, `/v1/solve`, Google Sheets, dependencies, routing, council behavior, benchmark work, readiness/value/provider/local-model/security/privacy/production/public/partnership/Pi.dev integration claims, or Alpha superiority. | completed selector / blocked selection |
| authorization-preparation lane | docs: prepare Value Read unblinding and final interpretation authorization | completed | `docs/evals/runs/alpha-solver-value-read-unblinding-final-interpretation-authorization-001/` | Prepared exact future operator authorization language, unblinding/source-identity review protocol, final interpretation protocol, score-lock preservation rules, source-identity map handling rules, stop conditions, non-actions, non-claims, and a review-only selected next state. | Did not unblind, reveal source identities, create final interpretation, change scores, inspect raw Alpha/baseline outputs, access or commit an identity map, call providers, run local models, expose runtime/dashboard/public API behavior, expose `/v1/solve`, mutate Google Sheets, add dependencies, implement a release lane, or make value/readiness/benchmark/provider/local-model/production/public/security/privacy/partnership/Pi.dev integration/Alpha-superiority claims. | completed authorization preparation |
| unblinding-final-interpretation lane | docs: interpret Value Read blind scores after unblinding | completed source-of-truth sync | `docs/evals/runs/alpha-solver-value-read-unblinding-final-interpretation-pass-001/` | Completes the authorized source-identity review using the operator-provided map and creates a bounded final interpretation. Locked scores were not changed; final interpretation exists; claims remain bounded to the manual no-provider prompt-contract simulation; no release implementation lane is selected. | Does not change scores, inspect raw Alpha/baseline outputs, call providers, run local models, expose runtime/dashboard/public API behavior, expose `/v1/solve`, mutate Google Sheets, add dependencies, implement a release lane, or make readiness/broad-value/benchmark/provider/local-model/production/public/security/privacy/partnership/Pi.dev integration/Alpha-superiority claims. | completed interpretation / review-only selected next |
| #587 | Add discrimination task bank feasibility packet | ✅ merged 2026-06-16 | `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/` | Records a docs-only discrimination task-bank asset feasibility packet with verdict `FEASIBLE_WITH_GUARDED_NEXT_STEP`. | Does not execute tasks, generate outputs, score responses, call providers, run local models, modify runtime behavior, expose dashboards/public APIs, call `/v1/solve`, update Google Sheets, prove benchmark readiness, value, readiness, or superiority. | completed preservation-only feasibility |
| #588 | Add claim-safe demo evidence feasibility packet | ✅ merged 2026-06-16 | `docs/evals/runs/alpha-solver-demo-evidence-packet-to-demo-001/` | Records a docs-only claim-safe demo evidence packet feasibility packet with verdict `FEASIBLE_WITH_STRICT_EVIDENCE_BOUNDARIES`. | Does not create product proof, runtime demo, provider/local-model validation, API readiness, Sheet synchronization, readiness, superiority, traction, buyer validation, or external-use approval. | completed preservation-only feasibility |
| group-sync lane | docs: sync source of truth after parallel feasibility group | completed | `docs/evals/runs/alpha-solver-parallel-feasibility-group-sync-001/` | Records that PR #581, #587, and #588 are merged; no open PR is editing source-of-truth docs; deferred follow-up choices require one operator decision state. | Does not create new feasibility content, change scores, perform source-map work, inspect raw outputs, call providers, run local models, expose runtime/dashboard/public API behavior, expose `/v1/solve`, mutate Google Sheets, add dependencies, implement a release lane, or make value/readiness/superiority claims. | completed preservation-only sync |
| selector-after-final-interpretation lane | docs: select next release lane after Value Read interpretation | completed | `docs/evals/runs/alpha-solver-next-release-selector-after-final-interpretation-001/` | Completes a docs-only selector after the Value Read final interpretation and parallel feasibility group sync; selects exactly one next lane, `ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001`, for operator review. | Does not create or implement the selected lane, change scores, inspect raw outputs, call providers, run local models, expose runtime/dashboard/public API behavior, expose `/v1/solve`, mutate Google Sheets, add dependencies, or make readiness/broad-value/benchmark/provider/local-model/production/public/security/privacy/partnership/Pi.dev integration/Alpha-superiority claims. | completed selector / selected next state |
| #591 | Add substantive derivation check gate | ✅ merged | `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records `ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001` as a completed docs-first review-only gate packet and sets selected next state to `OPERATOR_REVIEW_REQUIRED_AFTER_SUBSTANTIVE_DERIVATION_CHECK_001`. | Does not implement runtime behavior, call providers/local models, expose APIs, mutate Sheets, change scores, inspect raw outputs, create source-map work, add dependencies, implement release behavior, or prove quality/readiness/value/superiority. | completed gate / review-only selected next |
| #592 | Standardize derivation copying label | ✅ merged | `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/derivation-vs-echo-criteria.md`; `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/test-plan.md` | Preserves `unsupported_copying` as the canonical copying label in the derivation-check packet. | Does not add fixtures, execute task-bank work, inspect raw outputs, call providers/local models, change scores, expose APIs, or make readiness/value/benchmark/provider/local-model/production/public/security/privacy/partnership/Pi.dev integration/Alpha-superiority claims. | completed label cleanup |
| #595 | Add discrimination task-bank cheap test packet | ✅ merged | `docs/evals/runs/alpha-solver-discrimination-task-bank-first-cheap-test-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001` as a completed docs-only first cheap-test packet with five representative taxonomy task cards and records `OPERATOR_REVIEW_REQUIRED_AFTER_DISCRIMINATION_TASK_BANK_FIRST_CHEAP_TEST_001` as a prior selected next state. | Does not execute the task bank, generate Alpha outputs, generate baseline outputs, inspect raw outputs, score outputs, change scores, unblind, perform source-map work, call providers/local models/runtime endpoints/dashboard/public APIs/`/v1/solve`/Google Sheets, add dependencies, implement release behavior, or make broad value/readiness/benchmark/provider/local-model/security/privacy/production/public/partnership/Pi.dev integration/Alpha-superiority claims. | completed packet / review-only selected next |
| #598 | docs: import local and OpenAI smoke results | merged PR #598 | `docs/evals/runs/alpha-solver-local-openai-smoke-results-import-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Imports Operator-provided, redacted smoke-only results: local/Ollama passed using `qwen2.5:3b`, and OpenAI passed using `gpt-4.1-mini-2025-04-14`. | Does not create behavior evidence, quality evidence, readiness evidence, benchmark evidence, production/public evidence, provider-quality evidence, local-model-quality evidence, or Alpha-superiority evidence. | completed evidence import / review-only selected next |
| PR pending | docs: record partial local MVP manual review | completed pending PR | `docs/evals/runs/alpha-solver-local-mvp-manual-review-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records operator-provided screenshot-only partial manual review evidence for `ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001` with verdict `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST` and selected next state `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001`. | Does not claim full manual review pass, execute providers/local models/tools/pilot, generate or score outputs, expose `/v1/solve`, mutate Sheets, modify runtime/router/console/config/tests, or claim readiness, benchmark validation, provider/local-model/tool quality, security/privacy completion, autonomous execution readiness, or Alpha superiority. | completed partial manual review / prior review-only selected next |
| PR pending | docs: authorize routed-vs-plain pilot protocol | completed pending PR | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-authorization-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001` as a docs-only authorization packet for a future routed-vs-plain output-collection lane with task scope, identities, execution permission boundaries, route metadata, blinding, scoring gate, stop conditions, non-actions, and non-claims. | Does not execute the pilot, call providers, run hosted/local models, execute tools, browse, generate outputs, score, unblind, inspect raw prior outputs, mutate Sheets, add dependencies, expose `/v1/solve`, or make readiness/benchmark/quality/production/public/Alpha-superiority claims. | completed authorization / review-only selected next |
| #599 | tools: add local OpenAI test console | merged PR #599 | `tools/operator_test_console.py`; `tests/test_operator_test_console.py`; `docs/evals/runs/alpha-solver-local-openai-test-console-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Adds a local-only Operator smoke test console that reuses the existing smoke runner path for local/Ollama and OpenAI smoke checks. | Does not create behavior evidence, quality evidence, readiness evidence, benchmark evidence, production/public evidence, security/privacy completion evidence, provider-quality evidence, local-model-quality evidence, or Alpha-superiority evidence. | completed console implementation / review-only selected next |
| #600 | tools: refine local OpenAI test console UX and redaction | merged PR #600 | `tools/operator_test_console.py`; `tests/test_operator_test_console.py`; `docs/evals/runs/alpha-solver-local-openai-test-console-ux-reduction-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Preserves submitted form state after console runs and avoids over-redacting safe numeric usage token counts. | Does not create behavior evidence, quality evidence, readiness evidence, benchmark evidence, production/public evidence, security/privacy completion evidence, provider-quality evidence, local-model-quality evidence, or Alpha-superiority evidence. | completed UX/redaction refinement / prior review-only selected next |

| #601 | alpha: add model catalog routing preview | merged PR #601 | `alpha/model_catalog.py`; `alpha/model_router.py`; `configs/model_catalog.json`; `tests/test_model_catalog.py`; `tests/test_model_router.py`; `docs/evals/runs/alpha-solver-model-catalog-routing-preview-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Adds configurable backend model catalog metadata and deterministic routing preview. | Does not call providers, run local models, expose `/v1/solve`, mutate Sheets, generate eval outputs, score outputs, unblind, add dependencies, build UI, or make quality/readiness/benchmark/production/public/security/privacy/Alpha-superiority claims. | completed backend implementation / review-only selected next |

| #614 | docs: record routed-vs-plain manual pilot outputs | merged PR #614 | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-outputs-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records one manual plain output, one manual routed Alpha output, and one route metadata record for each `RVP-001` through `RVP-012`. | Does not run Alpha runtime, invoke `/v1/solve`, call providers, run hosted/local models, execute tools, browse, use current external research, mutate Sheets, add dependencies, score, unblind, or make readiness, benchmark, quality, production/public, security/privacy, autonomous-readiness, or Alpha-superiority claims. | completed manual output collection / review-only selected next |
| #619 pending | docs: construct routed-vs-plain blinded scorer packet | completed in PR #619 pending merge | `docs/evals/runs/alpha-solver-routed-vs-plain-blinded-scorer-packet-construction-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Constructs a source-neutral scorer-facing blinded packet for all 12 routed-vs-plain tasks with blank scoring/preference/rationale fields and no committed A/B identity key. | Does not score, fill scores, lock scores, unblind, interpret, commit a source map, run Alpha runtime, invoke `/v1/solve`, call providers, run hosted/local models, execute tools, browse, mutate Sheets, add dependencies, expose dashboard/public API, deploy, or claim readiness/benchmark/quality/production/public/security/privacy/autonomous-readiness/Alpha-superiority. | completed packet construction / review-only selected next |

| PR pending | console: surface expanded route metadata | completed pending PR | `tools/operator_test_console.py`; `tests/test_operator_test_console.py`; `docs/evals/runs/alpha-solver-test-console-routing-metadata-display-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Surfaces expanded metadata-only model route fields and existing tool recommendation preview fields in the local-only Operator console. | Does not run providers, hosted/local models, Ollama, tools, web/current research, runtime GitHub calls, `/v1/solve`, Sheets, scoring, unblinding, or claim readiness/value/quality/superiority. | completed product-foundation lane / prior review-only selected next |
| PR pending | console: continue target-parity route UI build | completed pending PR | `tools/operator_test_console.py`; `tests/test_operator_test_console.py`; `docs/evals/runs/alpha-solver-console-target-parity-product-pass-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Adds five-step route-flow, task-interpretation, model-route, tool-route, manual-override, and evidence-boundary cards to the local-only console. Selected next state is `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001`. | Does not run providers, hosted/local models, Ollama, tools, web/current research, runtime GitHub calls, `/v1/solve`, Sheets, scoring, unblinding, deployment, or make readiness/value/quality/superiority claims. | completed product-foundation lane / deferred review selected next |
| PR pending | docs: prepare console routing metadata operator review packet | completed pending PR | `docs/evals/runs/alpha-solver-test-console-routing-metadata-operator-review-packet-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-METADATA-OPERATOR-REVIEW-PACKET-001` as a docs/test-support packet for future manual operator review of local-console route-preview understandability and evidence-boundary safety; selected next state is `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_METADATA_OPERATOR_REVIEW_PACKET_001`. | Does not run the console, perform operator review, run Alpha runtime, invoke `/v1/solve`, call providers, run hosted/local models, run Ollama, execute tools, browse, mutate Sheets, score, unblind, inspect source maps, deploy, or make readiness/value/quality/superiority claims. | completed packet / review-only selected next |
| PR pending | catalog: expand model routing metadata | completed pending PR | `configs/model_catalog.json`; `alpha/model_catalog.py`; `alpha/model_router.py`; `tests/test_model_catalog.py`; `tests/test_model_router.py`; `docs/evals/runs/alpha-solver-model-catalog-routing-metadata-expansion-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records `ALPHA-SOLVER-MODEL-CATALOG-ROUTING-METADATA-EXPANSION-001` as a product-foundation static catalog metadata and deterministic no-call route preview lane. | Does not run Alpha runtime, invoke `/v1/solve`, call providers, run hosted/local models, execute tools, browse, mutate Sheets, score, unblind, inspect A/B keys/source maps, or claim readiness, value, benchmark success, provider/local-model/tool quality, production/public readiness, security/privacy completion, autonomous readiness, or Alpha superiority. | completed product-foundation lane / review-only selected next |

## Current selected next state

`OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001` is the selected next state. The prior selected next state was `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_METADATA_OPERATOR_REVIEW_PACKET_001`. This is a deferred-review state after the console target-parity product pass lane `ALPHA-SOLVER-CONSOLE-TARGET-PARITY-PRODUCT-PASS-001`. Operator review remains deferred pending another narrow local-console HTML/diagram target-parity build or gap-closure lane. It does not run the console, perform the operator review, run Alpha runtime, invoke `/v1/solve`, call providers, run hosted/local models, run Ollama, execute tools, browse, use current external research, mutate Sheets, add dependencies, score, unblind, inspect A/B keys or source maps, interpret final results, or make readiness, value, benchmark, quality, production/public, security/privacy, autonomous-readiness, or Alpha-superiority claims. The preceding test console routing metadata operator review packet lane remains historical docs/test-support context only; it is not the current selected state.

`ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001`, `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001`, and `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-METADATA-DISPLAY-001` remain completed historical lanes. They are not the current selected state.

The current selected state records only that review remains deferred pending another narrow local-console target-parity build or gap-closure lane. It authorizes no source-map work, unblinding, raw source-output inspection for scoring, dashboard or public API work, `/v1/solve` exposure, Google Sheets mutation, console execution by Codex, provider/local-model/tool/web execution, council behavior, benchmark work, release behavior, readiness claim, broad value claim, provider claim, local-model claim, security/privacy claim, production/public claim, demo external-use approval, discrimination-task execution/scoring, partnership/Pi.dev integration claim, or Alpha-superiority claim.

## Evidence boundary

The current deferred-review state supports only bounded statements that the repository contains a local-console target-parity product pass and that operator review remains deferred pending another narrow HTML/diagram target-parity build or gap-closure lane. It does not include completed operator-review results, console-run evidence, provider output, hosted-model output, local-model output, Ollama output, tool output, web/current-research output, score output, unblinding output, final interpretation, an A/B identity key, source-arm mapping, Google Sheets mutation, dependency changes, runtime validation, `/v1/solve` evidence, dashboard/public API evidence, readiness evidence, benchmark evidence, quality evidence, value evidence, security/privacy completion, autonomous-readiness evidence, or Alpha-superiority evidence.

Historical lanes remain preserved as historical context only, including Value Read packet construction/scoring/interpretation lanes, gate/helper/static-checking lanes, feasibility lanes, local/OpenAI smoke-runner and smoke-result import lanes, model/tool catalog metadata lanes, and routed-vs-plain pilot authorization/output-collection lanes. Those historical artifacts do not override the current selected state, which is `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001`.

## ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001

- Artifact: `tools/operator_smoke_runner.py`
- Packet: `docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/`
- Evidence type: operator smoke-runner implementation and runbook only.
- Smoke execution status: not run by merged PR #597.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`.
- Boundary: does not prove provider quality, local model quality, readiness, benchmark success, production readiness, public readiness, security/privacy completion, buyer validation, traction, partnership/Pi.dev integration, or Alpha superiority.

## ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RESULTS-IMPORT-001

| Field | Value |
|-------|-------|
| Status | completed docs-only evidence import |
| Packet | `docs/evals/runs/alpha-solver-local-openai-smoke-results-import-001/` |
| Local/Ollama smoke | passed using `qwen2.5:3b` |
| OpenAI smoke | passed using `gpt-4.1-mini-2025-04-14` |
| Evidence boundary | smoke-only result import |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RESULTS_IMPORT_001` |

This entry records Operator-provided, redacted smoke-only evidence. It does not create behavior evidence, quality evidence, readiness evidence, benchmark evidence, production/public evidence, provider-quality evidence, local-model-quality evidence, or Alpha-superiority evidence.


## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001

| Field | Value |
|-------|-------|
| Lane ID | `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-001` |
| Purpose | local-only operator smoke testing console |
| Packet | `docs/evals/runs/alpha-solver-local-openai-test-console-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001` |
| Evidence boundary | console implementation only, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim |


## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001

| Field | Value |
|-------|-------|
| Lane ID | `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UX-REDUCTION-001` |
| Purpose | preserve submitted form state after console runs and avoid over-redacting safe usage token counts |
| Packet | `docs/evals/runs/alpha-solver-local-openai-test-console-ux-reduction-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UX_REDUCTION_001` |
| Evidence boundary | UX/redaction refinement only, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim |

## ALPHA-SOLVER-MODEL-CATALOG-ROUTING-PREVIEW-001

- Artifact: `alpha/model_catalog.py`, `alpha/model_router.py`, and `configs/model_catalog.json`
- Packet: `docs/evals/runs/alpha-solver-model-catalog-routing-preview-001/`
- Purpose: add configurable model catalog and deterministic routing preview backend.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_PREVIEW_001`.
- Evidence boundary: routing preview only, no provider/local-model calls, no quality/readiness/benchmark/production/public/security/privacy/Alpha-superiority claim.

## ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001

- Artifact: `alpha/tool_catalog.py`, `alpha/tool_router.py`, and `configs/tool_catalog.json`
- Packet: `docs/evals/runs/alpha-solver-tool-catalog-routing-registry-001/`
- Purpose: add metadata-only tool catalog and deterministic recommendation preview for Python/computation, web/current research, GitHub/code, docs/files, spreadsheets, PDF/file parsing, browser/computer use, specialized math tools, and future provider-specific tools.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_TOOL_CATALOG_ROUTING_REGISTRY_001`.
- Evidence boundary: recommendation preview only, no tool execution, no browsing, no provider/local-model calls, no runtime GitHub calls, no file or Sheet mutation, no readiness/quality/security/privacy/production/public/provider/local-model/tool-quality/Alpha-superiority claim.


## ALPHA-SOLVER-MODEL-CATALOG-EXPANSION-COST-TIERS-001

- Status: completed backend metadata implementation / review-only selected next.
- Changed files: `alpha/model_catalog.py`; `alpha/model_router.py`; `configs/model_catalog.json`; `tests/test_model_catalog.py`; `tests/test_model_router.py`; `docs/evals/runs/alpha-solver-model-catalog-expansion-cost-tiers-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md`.
- Evidence value: expands metadata-only model catalog fields and deterministic routing preview warnings/fallbacks.
- Boundary: does not call providers, run local models, pull models, add dependencies, expose `/v1/solve`, mutate Sheets, benchmark, validate model quality, or make readiness/quality/provider/local-model/Alpha-superiority claims.

## ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001

| Field | Value |
|-------|-------|
| Lane ID | `ALPHA-SOLVER-LOCAL-OPENAI-TEST-CONSOLE-UI-POLISH-001` |
| Purpose | improve local-only console usability with model dropdowns, prompt counter, friendly result display, and copyable sanitized JSON |
| Packet | `docs/evals/runs/alpha-solver-local-openai-test-console-ui-polish-001/` |
| Builds on baseline | `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_EXPANSION_COST_TIERS_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001` |
| Evidence boundary | UI polish only, no model catalog or tool catalog logic change, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim |

## ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001

| Field | Value |
|-------|-------|
| Lane ID | `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001` |
| Purpose | wire the local-only Operator console to metadata-only model/tool route preview before separate smoke execution |
| Packet | `docs/evals/runs/alpha-solver-test-console-routing-preview-integration-001/` |
| Builds on baseline | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UI_POLISH_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001` |
| Evidence boundary | preview-only UI/backend integration, no provider/local-model execution, no tool execution, no quality/readiness/benchmark/public/production/security/privacy/Alpha-superiority claim |


## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001

| Field | Value |
|-------|-------|
| Evidence artifact | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-packet-001/` |
| Evidence type | docs-only static pilot packet |
| Latest completed lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-PACKET-001` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001` |
| Evidence value | Provides static task cards, route-value rubric, plain-model comparison protocol, blank result capture template, operator runbook, stop conditions, non-actions, and non-claims for later operator review. |
| Boundary | Does not execute the pilot, call providers, run hosted models, run local models, execute tools, browse, generate Alpha outputs, generate baseline outputs, score outputs, change scores, unblind, inspect raw Alpha or baseline outputs, perform source-map work, mutate Google Sheets, add dependencies, expose `/v1/solve`, expose dashboard/public API behavior, or make readiness, benchmark, production, public, security/privacy, provider, local-model, tool-quality, or Alpha-superiority claims. |


## ALPHA-SOLVER-MVP-CUTOVER-REVIEW-001

| Field | Value |
|-------|-------|
| Status | completed docs-only STOP / go-no-go review |
| Packet | `docs/evals/runs/alpha-solver-mvp-cutover-review-001/` |
| Verdict | `LOCAL_OPERATOR_MVP_CANDIDATE_READY_FOR_MANUAL_REVIEW` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_PACKET_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` |
| Boundary | Local operator manual-review candidate only; no provider/local-model/tool/pilot execution, output generation, scoring, unblinding, raw-output inspection, source-map work, dependency addition, Google Sheets mutation, `/v1/solve` exposure, dashboard/public API exposure, deployment, production/public readiness, benchmark, provider/local-model/tool-quality, security/privacy completion, autonomous-readiness, or Alpha-superiority claim. |

## ALPHA-SOLVER-LOCAL-MVP-MANUAL-REVIEW-001

| Field | Value |
|-------|-------|
| Status | completed partial docs-only manual review |
| Packet | `docs/evals/runs/alpha-solver-local-mvp-manual-review-001/` |
| Verdict | `LOCAL_MVP_MANUAL_REVIEW_PARTIAL_NEEDS_OPERATOR_TEST` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_MVP_CUTOVER_REVIEW_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` |
| Evidence value | Records operator-provided screenshot-only observations of the local console at `http://127.0.0.1:8765`, including visible local-only console elements and initial false execution authorization indicators. |
| Boundary | Does not claim full manual review pass, execute providers/local models/tools/pilot, generate or score outputs, expose `/v1/solve`, mutate Sheets, modify runtime/router/console/config/tests, or claim readiness, benchmark validation, provider/local-model/tool quality, security/privacy completion, autonomous execution readiness, or Alpha superiority. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-AUTHORIZATION-001

| Field | Value |
|-------|-------|
| Status | completed docs-only authorization packet |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-authorization-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_MVP_PARTIAL_MANUAL_REVIEW_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001` |
| Evidence value | Defines future output-collection protocol, task scope, identities, execution permissions, task-id preservation, route metadata capture, blinding, scoring gate, stop conditions, and evidence boundaries. |
| Boundary | No pilot execution, provider/local/model/tool/web execution, output generation, scoring, unblinding, raw prior-output inspection, Sheets mutation, dependency addition, `/v1/solve` exposure, or readiness/benchmark/quality/superiority claim. |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001

| Field | Value |
|-------|-------|
| Status | completed output collection preparation packet |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-output-collection-prep-001/` |
| Task IDs | `RVP-001` through `RVP-012` preserved exactly |
| Output pairs | none recorded; blank fields only |
| Route metadata | blank route metadata fields provided for all 12 task IDs, including route reasons |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_AUTHORIZATION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001` |
| Evidence boundary | Manual no-provider prompt-contract simulation only; not Alpha runtime, `/v1/solve`, provider, hosted-model, local-model, tool, web/current research, scoring, unblinding, benchmark, readiness, quality, security/privacy completion, autonomous-readiness, or Alpha-superiority evidence. |

| PR pending | docs: record routed-vs-plain pilot output collection prep | completed pending PR | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-output-collection-prep-001/`; `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` | Records `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUT-COLLECTION-PREP-001` as a completed output collection preparation packet with blank capture templates for RVP-001 through RVP-012 and a runbook for later operator-provided or separately authorized collection. | Does not run Alpha runtime, invoke `/v1/solve`, call providers, run hosted/local models, execute tools, browse, use current external research, mutate Sheets, add dependencies, score, unblind, or claim readiness/benchmark/quality/production/public/security/privacy/autonomous-readiness/Alpha-superiority. | completed collection prep / review-only selected next |

## ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001

| Field | Value |
| --- | --- |
| Evidence artifact | `docs/evals/runs/alpha-solver-routed-vs-plain-blinded-scorer-packet-construction-001/` |
| Evidence type | docs-only blinded scorer packet construction |
| Latest completed lane | `ALPHA-SOLVER-ROUTED-VS-PLAIN-BLINDED-SCORER-PACKET-CONSTRUCTION-001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001` |
| Boundary | No scoring, score locking, unblinding, source-map commit, runtime/provider/local-model/tool/web execution, readiness, benchmark, quality, or Alpha-superiority claim. |


## ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-AUTHORIZATION-001

| Field | Value |
|-------|-------|
| Status | completed docs-only authorization/prep packet |
| Packet | `docs/evals/runs/alpha-solver-routed-vs-plain-blind-scoring-pass-authorization-001/` |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLINDED_SCORER_PACKET_CONSTRUCTION_001` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_AUTHORIZATION_001` |
| Evidence value | Prepares operator review materials for a future blind scoring pass using the PR #619 scorer-facing packet; includes authorization language, scoring protocol, blank score-entry template, score-lock protocol, custody rules, stop conditions, non-actions, non-claims, and checks documentation. |
| Boundary | No scoring, score filling, winner selection, aggregate computation, unblinding, interpretation, A/B key inspection or commit, source-map inspection or commit, source artifact inspection for scoring, runtime/provider/local-model/tool/web execution, Sheets mutation, dependencies, deployment, readiness, benchmark, value, or Alpha-superiority claim. |


## ALPHA-SOLVER-ROUTED-VS-PLAIN-BLIND-SCORING-PASS-001

| Field | Value |
|---|---|
| Evidence packet | `docs/evals/runs/alpha-solver-routed-vs-plain-blind-scoring-pass-001/` |
| Evidence type | Locked blind scoring pass for the routed-vs-plain scorer-facing packet. |
| Task count | 12 tasks scored: `RVP-001` through `RVP-012`. |
| Score lock | `docs/evals/runs/alpha-solver-routed-vs-plain-blind-scoring-pass-001/score-lock-confirmation.md` |
| Selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_BLIND_SCORING_PASS_001` |
| Boundary | No unblinding, source identity review, source-map review, A/B key inspection, source artifact inspection, route metadata inspection, runtime/provider/local-model/tool/web execution, Google Sheets mutation, final interpretation, or readiness/value/benchmark/production/public/provider/local-model/tool/security/privacy/autonomous-readiness/Alpha-superiority claim. |


## Console target-parity selected next state - 2026-06-18

`OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001` is the selected next state after `ALPHA-SOLVER-CONSOLE-TARGET-PARITY-PRODUCT-PASS-001`. Operator review remains deferred pending another narrow HTML/diagram target-parity build or gap-closure lane.
