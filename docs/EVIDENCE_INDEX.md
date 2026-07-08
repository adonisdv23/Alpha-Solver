# Evidence Index - post-676 north-star roadmap reset

> Source-of-truth evidence ledger. Verification date **2026-07-08** after `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001`.

## How to read evidence value

Entries in this file are design, documentation, gate, helper, static-checking, methodology, blocked-attempt, or research evidence unless explicitly stated otherwise. They do not create broad value, readiness, benchmark, production, security/privacy, public exposure, or Alpha-superiority evidence.

## Current selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001` is the selected next state.

This is an operator-review-required product-direction selection state after `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001`. It does not run the console, select B012, select B013, perform product-direction selection for the operator, run Alpha runtime, expose `/v1/solve`, score, unblind, interpret final results, mutate external ledgers, add dependencies, deploy, or make broad project claims.

The prior console HTML/diagram target-parity selected state `OPERATOR_REVIEW_REQUIRED_AFTER_CONSOLE_HTML_DIAGRAM_TARGET_PARITY_GAP_CLOSURE_001` remains historical context only. It is not the current selected state.

`ALPHA-SOLVER-GATE-SUBSTANTIVE-DERIVATION-CHECK-001`, `ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-FIRST-CHEAP-TEST-001`, `ALPHA-SOLVER-TEST-CONSOLE-ROUTING-METADATA-DISPLAY-001`, and the post-#663 through post-#676 Operator Console lanes remain completed historical or adjacent/supporting lanes. They are not the current selected state unless separately selected by a future operator decision.

## PR table

| PR | Title | Merged / status | Primary artifact | Evidence value | Non-claims | Lifecycle |
|----|-------|-----------------|------------------|----------------|------------|-----------|
| post-#676 reset | `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001` | current branch | `.specs/AS-POST-676-NORTH-STAR-ROADMAP-RESET-001.md`; `docs/evals/runs/as-post-676-north-star-roadmap-reset-001/` | Records operator-review-required source-truth reset after the Operator Console sequence; reclassifies B012/B013-style cockpit work as deferred pending product-direction selection. | No runtime execution, `/v1/solve` exposure, scoring, unblinding, final interpretation, broad readiness/value claim, or Alpha-superiority claim. | current review gate |
| #557-#564 | Early gate, confidence, escalation, headroom, and methodology lanes | merged | `.specs/`; `docs/evals/` | Records source-truth material for no-echo, false-premise, hidden-constraint, claim safety, confidence, needs-human, higher-headroom, and prompt-contract methodology. | Does not prove model quality, provider behavior, benchmark success, or broad value. | completed docs/gate context |
| #565-#574 | Local lab, Value Read blocked state, `/v1/solve` gate, local helper, blocked local attempt, and Pi.dev feasibility | merged | source-truth docs and run packets | Records bounded local/scaffold/gate/blocked-attempt/research evidence after the post-#568 Value Read state. | Does not prove local/runtime readiness, provider validation, public exposure, or Alpha superiority. | completed or blocked evidence |
| #577-post-581 | Value Read manual pilot, blind packet, scoring authorization, and scoring pass | completed | Value Read packet folders under `docs/evals/runs/` | Records manual no-provider raw-output pilot, blind scorer packet, scoring authorization, and score-lock state. | Does not authorize unblinding, final interpretation, release implementation, or broad value/readiness claims. | completed docs/evidence chain |
| #584 | Next-release selector after Value Read | merged | `docs/evals/runs/alpha-solver-next-release-selector-after-value-read-001/` | Records blocked next-release selection pending Value Read unblinding and final interpretation. | Does not authorize implementation, unblinding, final interpretation, runtime work, public exposure, benchmark work, or Alpha superiority. | completed selector / blocked selection |
| post-unblinding lanes | Unblinding/final interpretation and follow-up selectors | completed | Value Read and selector packets | Records bounded source-identity review, final interpretation, and later selector/gate material. | Does not change locked scores or create broad readiness/value claims. | historical context |
| #587-#588 | Discrimination task bank and demo evidence feasibility | merged | feasibility packets | Records feasibility findings with strict evidence boundaries. | Does not execute tasks, generate outputs, run a demo, or prove product value. | completed preservation-only feasibility |
| #591-#595 | Substantive derivation gate and first cheap-test packet | merged | derivation and discrimination task-bank packets | Records docs-first derivation/no-echo gate material and representative task cards. | Does not execute task-bank work or generate/scored outputs. | completed packet / review-only selected next |
| #598-#601 | Smoke result import, local smoke console, and model catalog routing preview | merged | smoke/test-console/model-catalog artifacts | Imports redacted smoke-only results and adds support surfaces. | Does not create behavior quality, production, or broad readiness evidence. | completed support/evidence lanes |
| #614-#619 | Routed-vs-plain pilot outputs and scorer packet | completed/pending historical entries | routed-vs-plain packet folders | Records manual outputs and scorer-facing packet preparation. | Does not score, unblind, run Alpha runtime, or make quality/readiness/superiority claims. | historical context |
| console/catalog sequence before #676 | local-console route-preview and target-parity support | completed historical entries | `tools/operator_test_console.py`; packets; source-truth docs | Adds metadata-only route preview, target-parity cards, best-path summary, and operator review packet context. | Does not run tools, score, unblind, or claim readiness/value/quality/superiority. | historical support context |

## Evidence boundary

The current operator-review-required state supports only bounded statements that the repository contains a post-#676 north-star roadmap reset and that operator review is required before the next product direction is selected.

It does not include completed operator-review results, console-run evidence, provider output, hosted-model output, local-model output, Ollama output, tool output, web/current-research output, score output, unblinding output, final interpretation, an A/B identity key, source-arm mapping, Google Sheets mutation, dependency changes, runtime validation, `/v1/solve` evidence, dashboard/public API evidence, readiness evidence, benchmark evidence, quality evidence, value evidence, security/privacy completion, autonomous-readiness evidence, or Alpha-superiority evidence.

Historical lanes remain preserved as historical context only. Those historical artifacts do not override the current selected state, which is `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`.

## ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001

- Artifact: `tools/operator_smoke_runner.py`
- Packet: `docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/`
- Evidence type: operator smoke-runner implementation and runbook only.
- Smoke execution status: not run by merged PR #597.
- Prior selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`.
- Boundary: smoke-runner implementation only; not quality, readiness, production, public, or Alpha-superiority evidence.

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
