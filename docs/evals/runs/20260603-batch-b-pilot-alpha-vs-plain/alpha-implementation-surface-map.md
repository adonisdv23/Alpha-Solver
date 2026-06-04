# Alpha Implementation Surface Map

Status: implementation mapping only
Lane: `ALPHA-IMPLEMENTATION-SURFACE-MAP-001`
Phase: `OUTPUT-DIFFERENTIATION-PHASE-001`

This artifact is planning and mapping only. It does not implement runtime behavior, change routing, call providers, run capture, rescore outputs, update Sheets, or start Batch C. It does not change `/v1/solve`, provider behavior, model configuration, scoring rubrics, or existing scored artifacts.

## Purpose

Mapping question: if the operator later approves implementation of Alpha brevity, answer-structure, claim-boundary, or selective-engagement behavior, which repo surfaces would likely be affected and what risks/tests should be considered?

This map is intended to make future implementation safer by separating likely seams from protected surfaces. It is not an authorization to implement those seams.

## Evidence basis

Committed artifacts inspected for this map:

- A3-1 artifacts: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`.
- Batch B artifacts: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/`.
- Batch B interpretation review: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/interpretation-review.md`.
- Post-interpretation decision artifacts: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/post-interpretation-decision.md` and `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/decision-next-lanes.md`.
- Brevity-control planning spec, present on this branch: `.specs/ALPHA-BREVITY-CONTROL-001.md`.
- Lift-vs-polish diagnostic plan, present on this branch: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/lift-vs-polish-diagnostic-plan.md` and `lift-vs-polish-diagnostic-matrix.csv`.
- Selective engagement plan, present on this branch: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/selective-expert-engagement-plan.md` and `selective-expert-engagement-matrix.csv`.
- Claim-boundary calibration packet, present on this branch: `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/claim-boundary-calibration-plan.md`, the claim-boundary risk taxonomy CSV, and `claim-boundary-scenario-bank.md`.
- Eval controls: `docs/evals/LIFT_DECISION_RULE.md`, `docs/evals/RESPONSE_QUALITY_RUBRIC.md`, `docs/evals/BLIND_SCORING_PROCEDURE.md`, `docs/evals/ARTIFACT_PRESERVATION.md`, and `docs/evals/templates/comparison_score_table_template.csv`.
- Entrypoint/behavior-contract references: `alpha_solver_portable.py`, `alpha-solver-v91-python.py`, `alpha_solver_entry.py`, and `docs/ENTRYPOINTS.md`.
- Runtime/routing/provider/model/eval/test surfaces inspected without modification: `service/app.py`, `alpha/solver/observability.py`, `alpha/reasoning/tot.py`, `alpha/policy/safe_out.py`, `alpha/policy/safe_out_sm.py`, `alpha/providers/safeout.py`, `alpha/providers/openai.py`, `service/models/modelset_registry.py`, `service/models/modelset_resolver.py`, `service/config/model_sets.yaml`, `alpha/core/router.py`, `alpha/routing/router_v12.py`, `alpha/adapters/prompts.py`, `service/prompts/renderer.py`, `service/prompts/selector.py`, and focused tests under `tests/`.

Preserved evidence facts:

- A3-1: Plain = 237, Alpha = 228, Alpha delta = -9, and Plain won all four limited comparisons.
- Batch B: Plain = 405, Alpha = 455, Alpha delta = +50, Alpha wins = 8, Plain wins = 4, ties = 0.
- A3-1 favored plain in a limited four-comparison run.
- Batch B favored Alpha in a limited 12-comparison pilot.
- The combined evidence suggests prompt-set-dependent behavior.
- Alpha's strongest value areas include claim-boundary discipline, evidence hygiene, hidden-constraint/risk handling, unsafe instruction cleanup, artifact discipline, and protocol framing.
- Alpha's clearest negative signal is brevity/control: `d12_brevity` Plain 26, Alpha 16, Alpha delta -10.
- The current planning decision authorizes planning only, not runtime implementation.

## Current behavior-contract classification

| File | Classification | Why | Future touch guidance | Risk level |
| --- | --- | --- | --- | --- |
| `alpha_solver_portable.py` | Active contract | Repo instructions and `docs/ENTRYPOINTS.md` identify it as the portable standalone behavior contract. The file contains LLM-facing protocol text, pipeline requirements, SAFE-OUT expectations, route concepts, expert roster, SolverEnvelope-shaped output, and a standalone solver path. | Future behavior changes may need to update this file only when the operator explicitly approves portable behavior-contract changes. For this lane it is protected. | High |
| `alpha-solver-v91-python.py` | Architecture reference / modular compatibility entrypoint | It imports modular repo components such as `alpha.solver.observability.AlphaSolver` and `alpha.config.loader.load_config`, then exposes `_tree_of_thought` and `AlphaSolver`. It is not standalone. | Future implementation should avoid this file unless entrypoint compatibility or config forwarding must change. Do not use it for prompt-only changes without a specific spec. | High |
| `alpha_solver_entry.py` | Runtime import bridge / compatibility wrapper | It dynamically loads `alpha-solver-v91-python.py`, re-exports `AlphaSolver`, and adds deterministic gate evaluation around `_tree_of_thought`. | Future changes should usually protect it. Touch only if approved behavior requires changing bridge-level gates or public import behavior. | High |
| `alpha_solver_cli.py` | CLI surface over compatibility entrypoint | It provides root command-line access to the compatibility path. | Usually protected for behavior changes unless a future implementation explicitly includes CLI output formatting. | Medium |
| `cli/alpha_solver_cli.py` | Command workflow CLI | It supports repo workflows such as run, replay, gates, finops, and traces. | Usually test/smoke surface rather than behavior-contract source. | Medium |
| `docs/ENTRYPOINTS.md` | Docs-only entrypoint role reference | It defines role boundaries among portable, modular/reference, bridge, and CLI files. | A future docs-only contract clarification could touch it; runtime behavior should not. | Low |

No other inspected file should be treated as a replacement for `alpha_solver_portable.py` as the portable standalone behavior contract.

## Runtime surface inventory

| Surface | File path | Role | Brevity/control relation | Answer-structure relation | Claim-boundary relation | Selective-engagement relation | Future change or protected? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Portable behavior contract | `alpha_solver_portable.py` | Standalone spec monolith and LLM-facing protocol. | High: current strict envelope and expert-section expectations can create length pressure. | High: defines required response sections. | High: includes SAFE-OUT and protocol discipline. | Medium: includes expert roster and route concepts. | Change only with explicit behavior-contract approval; otherwise protected. |
| Modular/reference entrypoint | `alpha-solver-v91-python.py` | Loads config and invokes modular solver. | Low direct relation; config/defaults can indirectly affect output shape. | Medium via envelope returned by solver. | Medium via SAFE-OUT/gates passed through downstream. | Medium via routing flags and agent flags. | Protected until implementation requires entrypoint-level config or compatibility change. |
| Import bridge | `alpha_solver_entry.py` | Re-exports solver and applies gate evaluation around the reference path. | Low. | Low. | Medium through low-confidence and clarify gate decisions. | Medium if future gate design were approved, but that could become hidden routing. | Protected. |
| FastAPI solve route | `service/app.py` | Defines `/v1/solve`, provider path, expert path, provider success body, provider error body, and expert answer helpers. | High for provider-backed answers because provider text is currently passed through, and expert answer fallback can add structure. | High because `_expert_response`, `_primary_expert_answer`, and success bodies shape output. | High because provider SAFE-OUT and expert clarify/block paths must preserve safe wording. | High because `_expert_complexity`, `_mode_from_confidence`, and expert path are live selection surfaces. | Protected for this lane. Future changes require explicit authorization and focused tests. |
| Provider request builder | `service/app.py` | Builds provider call request from query/context/model set. | Low direct relation. | Low. | Medium if system prompt or metadata policy changed later. | Medium if strategy/context becomes a selection signal. | Protected; do not add prompt orchestration here without approval. |
| Expert prompts | `service/app.py` | Constructs expert preview and answer prompts for the provider path. | Medium; prompt wording can influence verbosity. | High; prompts request JSON preview and final answer behavior. | Medium; assumptions and confidence handling influence claim boundaries. | High; expert-step path is already a selection surface. | Protected until selective engagement and answer-structure plans are approved. |
| Expert answer assembly | `service/app.py` | Converts provider answer, assumptions, mode, and fallback text into final expert response. | High; plausible future seam for answer-first and concise caveats. | High; plausible future seam for stable sections. | High; plausible future seam for safe wording. | Medium; must not become hidden routing. | Candidate future seam, but not authorized now. |
| Modular solver wrapper | `alpha/solver/observability.py` | Wraps Tree-of-Thought solver, routing, SAFE-OUT fallback, diagnostics, and envelope assembly. | Medium; envelope defaults can affect visible output shape. | High; central modular SolverEnvelope assembly. | High; SAFE-OUT fallback and diagnostics are sensitive. | Medium; progressive router and agent flags connect here. | Protected unless a future minimal implementation explicitly targets modular envelope assembly. |
| Tree-of-Thought solver | `alpha/reasoning/tot.py` | Deterministic reasoning search and answer/confidence/path result. | Low direct relation; answer text is best-node content. | Medium; result keys feed envelope. | Medium; confidence thresholds influence safe handling downstream. | Low/medium through router parameter. | Protected for behavior changes not focused on reasoning internals. |
| SAFE-OUT state machine | `alpha/policy/safe_out.py`, `alpha/policy/safe_out_sm.py` | Policy fallback and state machine. | Low direct relation. | Medium because fallback shape must remain stable. | High: core safety boundary. | Low. | Protected unless an explicit SAFE-OUT spec exists. |
| Provider SAFE-OUT body | `alpha/providers/safeout.py` | Allowlist-built provider failure response. | Low. | Medium because provider failures expose a response body. | High: must not leak unsafe/provider details. | Low. | Protected. |
| Provider adapters | `alpha/providers/openai.py`, `alpha/providers/base.py`, `alpha/adapters/openai.py`, `alpha/adapters/base.py` | Provider boundary, normalized errors, usage/cost fields, and local adapter behavior. | Low direct relation. | Low/medium if provider answer wrapping changed. | High safety and integration risk. | High risk if used for orchestration. | Protected; do not touch for Alpha behavior shaping yet. |
| Model-set registry/config | `service/models/modelset_registry.py`, `service/models/modelset_resolver.py`, `service/config/model_sets.yaml` | Defines and resolves model-set choices. | None direct. | None direct. | None direct. | High risk if used as gate or mode selector. | Protected. |
| Routing modules | `alpha/core/router.py`, `alpha/router/progressive.py`, `alpha/router/agents_v12.py`, `alpha/routing/router_v12.py` | Route, prune, agent, and deterministic routing helpers. | Low direct relation. | Medium if answer mode became route-like. | Medium if route controls SAFE-OUT. | High; selective engagement must not be implemented as hidden routing without approval. | Protected. |
| Prompt adapters/decks | `alpha/adapters/prompts.py`, `service/prompts/renderer.py`, `service/prompts/selector.py`, `service/prompts/decks.yaml` | Deterministic prompt templates and deck selection. | Medium; future prompt wording can drive brevity. | Medium/high; deck templates can define answer shape. | Medium; safe caveat wording can be represented. | Medium; selector rules can become engagement gates. | Candidate only after prompt/protocol plan approval; selector rules protected. |
| Eval controls | `docs/evals/LIFT_DECISION_RULE.md`, `docs/evals/RESPONSE_QUALITY_RUBRIC.md`, `docs/evals/BLIND_SCORING_PROCEDURE.md`, `docs/evals/ARTIFACT_PRESERVATION.md` | Official evaluation control docs and rubrics. | Evaluation only. | Evaluation only. | Evaluation only. | Evaluation only. | Protected; do not change scoring rubric for implementation. |
| Official scored artifacts | A3-1 and Batch B run folders | Preserved evidence and official score records. | Evidence source only. | Evidence source only. | Evidence source only. | Evidence source only. | Protected; do not alter official artifacts. |
| Focused tests | `tests/test_api_endpoints.py`, `tests/providers/*`, `tests/reasoning/*`, `tests/policy/*`, `tests/test_eval_differentiation_run_001.py`, `tests/test_output_diff_measurement_hardening.py` | Existing regression, API, provider, policy, routing, and eval guard coverage. | Future offline golden tests should be added near behavior surfaces. | Future tests should lock answer shape without calling providers. | Future tests should lock safe wording and non-claims. | Future tests should prove planning-only or explicit gate behavior. | Test additions are likely safest first implementation step. |

## Protected surfaces

The following should remain untouched unless explicitly authorized in a future implementation spec:

- Provider adapters and provider failure handling: `alpha/providers/*`, `alpha/adapters/openai.py`, `alpha/adapters/base.py`, and provider execution helpers in `service/app.py`.
- Model configuration and model-set resolution: `service/config/model_sets.yaml`, `service/models/modelset_registry.py`, and `service/models/modelset_resolver.py`.
- Routing implementation: `alpha/core/router.py`, `alpha/router/progressive.py`, `alpha/router/agents_v12.py`, `alpha/routing/router_v12.py`, and route/gate behavior exposed through `alpha_solver_entry.py`.
- `/v1/solve` behavior: `service/app.py`, request/response bodies, expert path, direct provider path, and related API tests.
- Scoring rubric and eval controls: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`, `docs/evals/LIFT_DECISION_RULE.md`, `docs/evals/BLIND_SCORING_PROCEDURE.md`, and `docs/evals/ARTIFACT_PRESERVATION.md`.
- Existing scored artifacts: A3-1 and Batch B score tables, blinded sheets, run summaries, defects, evidence packets, and source packets.
- Capture scripts and run/capture docs; no new capture should be started from this map.
- Sheet integrations and external planning ledgers.
- Secrets and environment/config files, including `.env.example`, `scripts/check_env.py`, and service auth/token files.

## Candidate implementation seams

These are only mapped seams. They are not implemented here.

| Candidate seam | Possible use in a future approved implementation | Lower-risk conditions | Primary risk |
| --- | --- | --- | --- |
| Test harness only | Add offline golden cases for brevity, answer structure, and claim-boundary wording. | Uses static inputs/expected outputs; no provider calls; no official artifact edits. | Golden cases may overfit Batch B if too narrow. |
| Docs-only behavior contract wording | Clarify desired answer-first, concise-caveat, and no-invented-scaffolding expectations. | Updates docs/spec only; no runtime code. | Contract drift if not followed by tests. |
| Prompt/protocol text | Adjust portable contract or prompt deck wording to favor short-answer-first and proportional caveats. | Only after answer-structure and brevity specs merge. | Can alter runtime behavior broadly if live prompt paths are touched. |
| Answer assembly helper | Centralize response section order, concise caveats, and safe wording. | Offline deterministic unit tests first; one path at a time. | May affect `/v1/solve` response shape or break compatibility. |
| Safe wording helper | Normalize limited-evidence, no-validation, no-readiness, and no-superiority phrases. | Must preserve uncertainty and safety. | Could hide necessary caveats or weaken safety if too terse. |
| Response mode selector | Select compact, structured, or protocol response shapes. | Must be explicit, deterministic, and test-covered. | Could become hidden routing or selective engagement. |
| Formatting policy | Keep requested format before adding scaffold. | Golden cases for reviewer comment, rewrite, decision memo, and artifact note. | May remove useful structure from complex tasks. |
| Selective engagement gate prototype | Later decide when expert/interrogation behavior is appropriate. | Only after diagnostic plans define gate criteria and stop conditions. | High risk of routing/provider orchestration claims. |

## Future implementation options

| Option | Benefit | Risk | Files likely touched | Tests needed | Appropriate before diagnostics? | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Option A: docs-only behavior contract update | Clarifies target behavior without runtime change. | May create contract/runtime drift. | `docs/ENTRYPOINTS.md`, future approved spec docs, possibly `alpha_solver_portable.py` only if explicitly approved as a behavior-contract doc update. | Docs lint, `git diff --check`, non-claim scan. | Yes, if it stays docs/spec only. | Ready |
| Option B: prompt/protocol wording update | Directly targets verbosity, answer order, and caveat proportionality. | Can change broad output behavior and affect portable contract. | `alpha_solver_portable.py`, `service/prompts/decks.yaml`, prompt helper files, or expert prompt text in `service/app.py`. | Offline prompt rendering tests, golden answer-shape tests, no-live-provider guard checks. | Refine first; wait for answer-structure/brevity review. | Refine |
| Option C: answer assembly guardrails | Can enforce short-answer-first and no invented scaffold in deterministic assembly. | Could change API/CLI visible output shape. | `alpha/solver/observability.py`, future helper module, possibly `service/app.py` expert response helpers. | Unit/golden tests for answer order, concise caveats, SAFE-OUT preservation, API regression. | Not before implementation criteria are accepted. | Verify |
| Option D: response-mode selector helper | Separates concise, structured, and protocol outputs. | Could become hidden routing or broad selective engagement. | Future helper module, prompt selector, answer assembly path. | Mode-selection matrix tests, determinism tests, no provider/model/routing mutation tests. | No; needs diagnostic criteria. | Verify |
| Option E: selective engagement gate prototype | Could avoid over-designed Alpha behavior on concise tasks while preserving lift on complex tasks. | High risk: hidden routing, provider orchestration, or model-policy change. | Gate/helper module, tests only at first; do not touch provider/model/routing without authorization. | Static classification tests, holdout prompt tests, false-positive/false-negative analysis. | No. | Blocked |
| Option F: eval/test-only golden cases first | Creates safe baseline for future behavior changes. | May encode too many assumptions if cases are not representative. | New tests and fixtures only, not official scored artifacts. | Golden tests for brevity, claim boundaries, structure, selective engagement planning, and artifact preservation. | Yes. | Ready |

## Recommended minimal implementation path

Recommended default after planning lanes merge and are reviewed:

1. Implement test/golden coverage or behavior-contract wording first, without runtime behavior changes.
2. Then consider a minimal answer-structure/brevity behavior change in the narrowest approved seam, with no provider, model, routing, or `/v1/solve` changes unless explicitly authorized.
3. Preserve claim-boundary and evidence hygiene as non-negotiable acceptance criteria.
4. Keep selective engagement as planning until diagnostics clarify gate criteria and false-positive risks.
5. Do not touch providers, routing, model configuration, scoring rubrics, or official scored artifacts for the first behavior implementation.

## Test strategy map

Before any implementation, define and review offline tests for:

- Short-answer-first behavior: direct answer before process when the prompt asks for a concise decision, reviewer comment, rewrite, or next action.
- No-invented-scaffolding: do not add roles, timelines, owners, files, commands, metrics, acceptance criteria, or process stages not supplied or requested.
- Claim-boundary safe wording: preserve limited-evidence, pilot-only, no-validation, no-readiness, no-superiority, and no-causality boundaries.
- Artifact-preservation stop conditions: never rewrite official scored artifacts, raw evidence records, or source hierarchy in ways that change meaning.
- Source-hierarchy behavior: respect committed repo artifacts over planning ledgers or advisory commentary.
- Concise-caveat behavior: keep necessary caveats in one compact sentence when risk is low, but preserve full caveats for safety/evidence-sensitive tasks.
- Regression tests for lift dimensions: claim-boundary discipline, evidence hygiene, hidden-constraint/risk handling, unsafe instruction cleanup, artifact discipline, and protocol framing.
- Planning PR boundaries: no live-provider tests in planning PRs.

## Risk register

| Risk | Why it matters | Mitigation before implementation |
| --- | --- | --- |
| Accidentally changing provider behavior | Provider path is live integration surface and can affect cost, latency, failure modes, and user-visible answers. | Do not touch provider adapters or provider request/response helpers without explicit authorization and offline tests. |
| Accidentally changing routing | Routing changes could alter model path, solver path, or hidden engagement behavior. | Keep routing modules protected; separate response shape from route selection. |
| Overfitting to Batch B | Batch B is a limited 12-comparison pilot and A3-1 favored plain in a separate limited run. | Use holdout planning and diverse golden cases before implementation. |
| Reducing safety or evidence discipline | Brevity could remove important caveats, uncertainty, or artifact-preservation instructions. | Treat claim-boundary and safety tests as blockers. |
| Hiding necessary caveats | Shorter outputs may become overconfident. | Require concise-caveat tests and high-risk expansion rules. |
| Making outputs shorter but less useful | Brevity alone is not lift. | Test usefulness, directness, and requested-format fit together. |
| Making answer modes into hidden routing | A response-mode selector could behave like unapproved routing. | Keep selectors explicit, deterministic, and test-only until approved. |
| Changing eval artifacts or official scores | Would compromise evidence provenance. | Protect A3-1 and Batch B artifacts; create new fixtures elsewhere for future tests. |
| Claiming readiness too early | Current decision authorizes planning only. | Repeat strict non-claims and require operator approval before implementation. |

## Relationship to active lanes

- `ALPHA-BREVITY-CONTROL-001`: Supplies the clearest near-term behavior target, because Batch B showed `d12_brevity` Plain 26, Alpha 16, Alpha delta -10. This map treats brevity implementation as future work only.
- `ALPHA-ANSWER-STRUCTURE-V2-001`: Should define task aware answer shapes before runtime implementation. This map identifies candidate assembly and formatting surfaces but does not create the spec.
- `ALPHA-CLAIM-BOUNDARY-CALIBRATION-001`: Supplies safe wording and non-claim requirements. Future behavior must preserve limited-evidence boundaries.
- `ALPHA-SELECTIVE-EXPERT-ENGAGEMENT-PLANNING-001`: Should remain planning until gate criteria are clear. This map marks selective engagement as high risk because it can overlap routing and provider orchestration.
- `OUTPUT-DIFF-LIFT-VS-POLISH-DIAGNOSTIC-001`: Should clarify which Alpha benefits are substantive lift versus presentation polish before broad behavior changes.
- `OUTPUT-DIFF-COMPLEXITY-GRADIENT-HOLDOUT-PLAN-001`: Should provide a holdout plan before changes are judged against new prompt complexity levels.
- `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001`: Remains blocked until approved improvements exist; this map does not start the run.

## Not authorized

This lane does not authorize:

- runtime implementation;
- routing changes;
- provider orchestration;
- model/provider changes;
- live capture;
- rescoring;
- Batch C;
- production readiness;
- public validation claim.

## Recommended next operator decision

Use this map after the planning PRs merge to decide which minimal implementation path is least risky. Recommended default: do not implement until answer-structure, brevity, claim-boundary, and diagnostic planning artifacts are merged and reviewed.

## Non-claims

This artifact makes these strict non-claims:

- no MVP validation;
- no Alpha Solver superiority generally;
- no broad plain-provider inferiority;
- no answer-quality superiority generally;
- no production readiness;
- no broad runtime readiness;
- no benchmark success;
- no exact billing accuracy;
- no provider reasoning orchestration.
