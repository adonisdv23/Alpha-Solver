# EVAL-ANSWER-QUALITY-PLAN-001: MVP Answer Quality Eval Plan

Status: Stage 0 planning only. This document does not implement an eval runner, make live OpenAI calls, change runtime behavior, or claim Alpha Solver is better than a direct model call.

## Decision summary

- FastAPI `/v1/solve` OpenAI mode is currently a thin provider execution path, not reasoning orchestration. It builds one `ProviderRequest` from the sanitized query and optional caller-supplied system prompt, carries `route`/`strategy` as metadata, calls the provider client once, and returns the provider text with telemetry/accounting metadata.
- Local/default `/v1/solve` runs Alpha Solver local reasoning (`react` or `_tree_of_thought`) and does not call a live model on that path.
- The current fair MVP comparison is not "Alpha Solver is a smarter model." The near-term value hypothesis is that Alpha Solver can be a disciplined operator wrapper around the same frontier model.
- The next lane should be a combined minimal-treatment-with-instrument lane: `EVAL-ANSWER-QUALITY-001`, implementing a real gated prediction-producer that reuses `alpha/eval` conventions and compares raw OpenAI against OpenAI plus Alpha Solver operator discipline. It should not be another open-ended planning lane.

## Scope and files inspected

Primary code paths inspected:

- `service/app.py`
- `alpha_solver_entry.py`
- `alpha-solver-v91-python.py`
- `alpha_solver_portable.py`
- `alpha/providers/base.py`
- `alpha/providers/openai.py`
- `alpha/providers/fake.py`
- `alpha/providers/telemetry.py`
- `alpha/providers/accounting.py`
- `alpha/providers/safeout.py`
- `tests/test_api_endpoints.py`
- `tests/providers/test_openai_live_smoke.py`

Eval, scenario, benchmark, and quality infrastructure inspected:

- `alpha/eval/harness.py`
- `alpha/eval/scorers.py`
- `alpha/core/benchmark.py`
- `scripts/eval_small.py`
- `scripts/benchmark_tot.py`
- `tests/test_benchmark.py`
- `datasets/mvp_golden.jsonl`
- `config/quality_gate.yaml`
- `service/scenarios/rubric.py`
- `service/scenarios/runner.py`
- `service/prompts/quality/evaluator.py`
- `data/scenarios/decks/`
- `docs/QUALITY_GATES.md`
- `docs/SCENARIO_DECKS.md`
- `docs/TEST_DATASETS.md`
- `service/models/modelset_resolver.py`
- `docs/RUNTIME_READINESS.md`

## Current behavior verified

### 1. `/v1/solve` OpenAI mode: pass-through, not reasoning-orchestrated

Evidence:

- OpenAI mode is enabled only by `MODEL_PROVIDER=openai`.
- `_build_provider_request(...)` sets `prompt=query`, optional `system=params["system"]`, model-set parameters, temperature/seed fields, and metadata including `route`, `model_set`, and `tenant`.
- In the OpenAI branch, `/v1/solve` obtains a provider client, emits a start event, calls `provider_client.execute(provider_request)`, emits completion/accounting events, and returns `_provider_success_response(...)`.
- The OpenAI branch does not call `_tree_of_thought`, `run_react_lite`, agents, router orchestration, source-hierarchy checks, or a structured reasoning loop before provider execution.
- The provider client formats the request as an OpenAI Responses API payload with `model`, `input`, and `max_output_tokens`; `_responses_input(...)` includes only an optional system message and the user prompt.
- Tests confirm the branch can be exercised with `FakeProviderClient`, returning normalized provider text and treating `route` as telemetry/accounting metadata.

Conclusion: OpenAI `/v1/solve` mode should be described as a provider pass-through with safety/telemetry/accounting wrapping, not as live Alpha Solver reasoning orchestration.

### 2. Local Alpha Solver reasoning: local/offline, no live model call found on this path

Evidence:

- If OpenAI provider mode is not enabled, `/v1/solve` runs either `run_react_lite(...)` for `strategy == "react"` or `_tree_of_thought(query, **params)` otherwise.
- `alpha_solver_entry._tree_of_thought(...)` delegates to the imported v91 `_tree_of_thought(...)`, then applies deterministic gates through `evaluate_gates(...)`.
- `alpha-solver-v91-python.py` constructs an `AlphaSolver`, loads local config, optional local cache, and invokes `solver.solve(...)` with deterministic reasoning configuration.
- The local-mode API test installs a provider factory that would fail if used, then verifies local mode returns the local solver output and emits no provider telemetry/accounting.

Conclusion: the local/default path represents Alpha Solver local/offline reasoning. It is useful for deterministic discipline and envelope behavior, but it is not evidence that Alpha Solver improves live OpenAI answer quality.

### 3. Current code-path map

| Role | Current path | Fair interpretation |
| --- | --- | --- |
| Direct OpenAI baseline | Not implemented as a first-class eval producer. The nearest reusable primitive is `OpenAIProviderClient.execute(ProviderRequest(...))`. | Needs a gated Phase 1 prediction-producer that calls the same model with a raw/comparable prompt. |
| Alpha Solver `/v1/solve` OpenAI mode | `POST /v1/solve` with `MODEL_PROVIDER=openai`, flowing through `_build_provider_request(...)` and `provider_client.execute(...)`. | Provider pass-through with request shaping, optional caller system prompt, SAFE-OUT normalization on failure, telemetry, and accounting. |
| Alpha Solver local/offline reasoning | Default `/v1/solve` branch, `alpha_solver_entry._tree_of_thought(...)`, `run_react_lite(...)`, and the v91 solver path. | Deterministic/local reasoning path; not connected to a live frontier model. |

## Existing eval/scenario/benchmark infrastructure

Reuse these pieces rather than creating a parallel eval framework:

- `alpha/eval/harness.py` loads JSONL rows, reads `prediction` and `target`, runs named scorer functions, and writes summary/router-compare artifacts from the CLI entrypoint.
- `alpha/eval/scorers.py` provides exact match and token F1 scorers.
- `datasets/mvp_golden.jsonl` is a tiny pre-baked dataset with `input`, `target`, and `prediction` fields; it is a smoke fixture, not an Alpha Solver-native answer-quality suite.
- `config/quality_gate.yaml` defines current thresholds (`min_accuracy`, latency, cost, and `primary_metric`).
- `docs/QUALITY_GATES.md` documents the lightweight eval/gate flow using `alpha.cli.main eval run` and `gate check`.
- `service/scenarios/rubric.py` provides deterministic judging for `equals`, `contains`, `regex`, `type`, and approximate numeric expectations.
- `service/scenarios/runner.py` executes scenario steps through adapters and judges outputs using the rubric.
- `service/prompts/quality/evaluator.py` provides heuristic response scoring and comparison for correctness, brevity, structure, and safety.
- `data/scenarios/decks/*.jsonl` and `docs/SCENARIO_DECKS.md` provide JSONL deck conventions, IDs, intents, prompts, expected routes, notes, and expectations metadata.
- `alpha/core/benchmark.py` measures elapsed time and memory for a supplied callable over query strings and writes benchmark JSON/Markdown.
- `scripts/benchmark_tot.py` is a local ToT smoke benchmark; `scripts/eval_small.py` is only a placeholder that prints a deterministic message.
- `docs/RUNTIME_READINESS.md` correctly frames OpenAI provider execution as explicit opt-in, with default local/offline workflows requiring no provider credentials.

## Reuse boundary and evidence warnings

Reuse:

- JSONL/dataset conventions from `alpha/eval` and scenario decks.
- `alpha/eval` scoring/reporting conventions where task outputs can be represented as `prediction` vs `target`.
- `service/scenarios/rubric.py` for gold-anchored checks such as required finding IDs, classification labels, route/lane labels, and forbidden/required claims.
- `service/prompts/quality/evaluator.py` only as a secondary heuristic for structure, brevity, and safety; it should not replace gold labels.
- `config/quality_gate.yaml` thresholds where applicable; if Phase 1 adds a metric that does not map to existing fields, document the reason and pre-register a temporary threshold.
- `OpenAIProviderClient`/`ProviderRequest` as low-level execution primitives under explicit live gating.

Do not reuse as real comparison evidence:

- `alpha/eval/harness.py --compare-baseline` token savings or latency numbers. That branch simulates baseline tokens as `100`, optimized tokens as `70`, and latency lists around fixed constants, so it is not a measurement of raw OpenAI vs Alpha Solver.
- Pre-baked `prediction` fields in existing JSONL smoke data as evidence that a live system produced the answer.
- `/v1/solve` OpenAI pass-through parity as evidence that Alpha Solver's concept failed. Parity is the expected null result when the treatment variable is only a thin wrapper or metadata.
- Optional live-smoke success as answer-quality evidence. It proves only a credentialed environment path worked at that time.

## Phase 1 value-add hypothesis

Phase 1 should test this mechanism-level hypothesis:

> Given the same OpenAI model and comparable generation settings, adding Alpha Solver operator discipline through structured system framing, source-hierarchy rules, SAFE-OUT framing, lane-selection constraints, runtime overclaim checks, prompt-safety rules, and PR/backlog workflow constraints improves gold-anchored performance on Alpha Solver-native tasks compared with a raw direct OpenAI baseline.

This is a prompt-level treatment unless a future code lane actually wires Tree-of-Thought, agents, routers, source hierarchy handling, or other reasoning orchestration into `/v1/solve` OpenAI mode.

Subjective "which answer feels better" scoring should be secondary because it is weakly reproducible, easy to bias, and can reward style over constraint preservation. The primary MVP signal should be gold-anchored correctness on explicit labels, contradictions, required fields, forbidden claims, and policy/scope decisions.

## Gold-anchored Alpha Solver-native task categories

Phase 1 case sets should focus on tasks where Alpha Solver's operator discipline is supposed to matter:

1. Source hierarchy conflict detection: identify which instruction/source wins when repo instructions, specs, docs, user requests, and generated claims conflict.
2. Runtime overclaim detection: label claims such as "live tested," "production ready," or "budget enforced" as supported/unsupported from supplied evidence.
3. Lane selection: choose implement, inspect/spec, go/no-go, live-gated eval, or no-op lane from a constrained set.
4. Scope violation detection: identify forbidden runtime changes, backlog workbook edits, live calls, provider behavior changes, or production-hosting work.
5. Backlog impact classification: map task ID, status change, source-of-truth files, and next action from provided evidence.
6. PR review structure compliance: check whether output contains required sections, test lines, source citations, squash description, and no prohibited claims.
7. Prompt safety and constraint preservation: detect leakage of secrets/PII, forbidden logging, missing redactions, or ignored constraints.
8. Docs/spec/runtime-readiness contradiction detection: identify contradictions between runtime-readiness claims and source files/specs.

Recommended minimum: at least 10 unambiguous cases per category for an initial smoke signal, and at least 25 per category before treating the result as a meaningful MVP value signal. Each case should include a gold label or rubric expectation that can be adjudicated without knowing which system produced the answer.

## Minimal Phase 1 component needed

Add a real prediction-producer, not a parallel eval framework. It should:

- Be explicitly live-gated and never run by default CI.
- Invoke two arms under the same model/settings:
  - baseline: direct raw OpenAI call through provider primitives;
  - treatment: OpenAI call with Alpha Solver structured operator prompt/source-hierarchy/SAFE-OUT/workflow framing.
- Save redacted outputs as JSONL rows compatible with the existing scorer/rubric conventions, then feed those rows into `alpha/eval` and/or scenario-rubric scoring.
- Record actual token usage, latency, model, model_set, temperature, max_tokens, seed support, treatment version, dataset version, and cost estimate when available.
- Include a result disclaimer: results are evidence, not proof, and may vary with model snapshots, prompts, case selection, and live-provider conditions.
- For repeatability checks, rerun the same gated prediction producer multiple times with preserved per-run artifacts and an aggregate summary; this measures run-to-run variability and must not be framed as proof of superiority.

## Required Phase 1 rigor

### 1. Controlled-baseline spec

- Same model.
- Same temperature.
- Same seed if the provider endpoint supports it; otherwise record that seed was requested but not sent/supported.
- Same max_tokens.
- Same comparable system framing except for the isolated treatment variable.
- Same input case order and deterministic shuffling seed.
- Same redaction and artifact policy for both arms.

### 2. Pre-registered success criteria

- Define the margin that counts as better before running the live eval.
- Start from `config/quality_gate.yaml` where metrics map cleanly: for example, exact/gold accuracy should meet or exceed the configured `min_accuracy` if the case set is mature enough.
- For the initial small MVP signal, pre-register both absolute and relative criteria, such as treatment accuracy >= baseline accuracy + an agreed margin on gold tasks, no regression in safety/constraint violations, and cost/latency within a declared ceiling.
- If a task-specific metric does not map to the current quality-gate keys, document that exception in the result artifact rather than silently inventing proof.

### 3. Case-set rigor

- Define a minimum case count per task type before running. Use at least 10 per category for a smoke signal and at least 25 per category for a stronger MVP signal.
- Require unambiguous gold answers: labels, required facts, expected winning source, forbidden claims, or structured fields.
- Require a disagreement rule: two maintainers or reviewers resolve contested gold labels before results are interpreted; unresolved cases are excluded and logged with a reason.
- Keep generic trivia out of the primary set.

### 4. Artifact safety

- Redact saved outputs where needed.
- Do not save secrets, raw API keys, authorization headers, or sensitive prompt content.
- Do not log provider raw request/response bodies unless a future explicit redaction spec allows it.
- Results files must include a disclaimer that results are evidence, not proof.

### 5. Cost ceiling

- Live OpenAI-connected evaluation must require an explicit opt-in flag and a pre-run cost ceiling.
- Suggested initial ceiling: no more than USD 5.00 total estimated provider cost for the first Phase 1 smoke run, or a lower operator-specified value.
- Abort before running if the expected case count, max_tokens, and model pricing cannot fit the ceiling.

### 6. Null hypothesis

- For the current `/v1/solve` OpenAI provider path, parity with direct OpenAI is expected because it is pass-through.
- Parity should not be treated as proof that the Alpha Solver concept failed.
- A meaningful treatment must isolate an actual Alpha Solver mechanism, even if the first mechanism is only structured operator prompting.

## What Stage 1 can fairly measure now

With the minimal prediction-producer, Stage 1 can fairly measure:

- Gold-anchored task accuracy for raw OpenAI vs Alpha Solver prompt-level treatment.
- Constraint preservation failures by category.
- Source-hierarchy decision correctness.
- Runtime overclaim and contradiction detection correctness.
- PR/backlog/lane classification correctness.
- Actual provider token usage, latency, and estimated cost for the live runs that were explicitly gated.
- Secondary structure/safety/brevity scores where the heuristic evaluator is appropriate.

## What cannot be fairly measured yet

Do not claim these yet:

- That Alpha Solver's current `/v1/solve` OpenAI mode performs live Tree-of-Thought, router, agents, source-hierarchy enforcement, or structured reasoning orchestration.
- That local/offline deterministic reasoning improves live OpenAI answer quality.
- That simulated `compare_baseline` token or latency deltas are real efficiency gains.
- That a live-smoke pass proves answer-quality value.
- That parity between direct OpenAI and pass-through `/v1/solve` disproves the MVP thesis.
- That production readiness, budget enforcement, fallback, hosting, or observability maturity proves answer quality.

## Recommendation

Choose `EVAL-ANSWER-QUALITY-001` as a combined minimal-treatment-with-instrument lane.

Rationale:

- Instrument-first alone would measure the current pass-through path and likely produce expected parity without testing the operator-wrapper value hypothesis.
- Provider reasoning orchestration is a larger product lane and should not be started before confirming that a cheaper prompt-level operator treatment produces any signal.
- A combined minimal lane can add one gated prediction-producer, one Alpha Solver treatment prompt contract, one small gold-anchored case set, and scorer/rubric integration while preserving local/offline defaults.

Fastest non-fake MVP value signal:

1. Freeze 80-200 gold-anchored Alpha Solver-native cases across the categories above.
2. Implement a live-gated prediction-producer that generates baseline and treatment predictions with the same model/settings.
3. Feed the resulting JSONL into existing `alpha/eval`/rubric scoring.
4. Publish a result artifact with actual token/latency/cost metadata, redaction/disclaimer, and pre-registered thresholds.
5. Make a go/no-go decision: either implement deeper provider reasoning orchestration or redesign the MVP thesis.

## Backlog impact

- ID: `EVAL-ANSWER-QUALITY-PLAN-001`
- Status change: Stage 0 planning/spec document completed; no runtime implementation.
- PR number: TBD
- Source-of-truth files: `docs/evals/ANSWER_QUALITY_EVAL_PLAN.md`
- Next action: implement `EVAL-ANSWER-QUALITY-001` as a gated minimal-treatment-with-instrument prediction-producer, or make a go/no-go decision that Alpha Solver's MVP thesis needs redesign.
