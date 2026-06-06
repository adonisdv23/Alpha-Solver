# Unused Built Surface Map

## Classification vocabulary

- `implemented code`: source code exists and contains executable logic for the surface.
- `docs/spec only`: the surface is described in docs or specs but not implemented in inspected code.
- `stub/minimal`: code exists but is intentionally narrow, placeholder-like, deterministic, or not a full orchestration implementation.
- `inactive/unapproved`: code may exist, but the current local LLM lane does not approve or use it.
- `unknown`: inspection did not prove an implementation state.

## Surface map

| Surface | Current local LLM path use | Classification | Evidence summary | Direct quality impact estimate |
| --- | --- | --- | --- | --- |
| Tree-of-Thought entrypoint | Bypassed | implemented code | `alpha_solver_entry._tree_of_thought` wraps the v91 entrypoint and adds gate decisions; `alpha-solver-v91-python.py` runs ToT through `AlphaSolver.solve`; portable ToT exists as a deterministic stub/fallback shape. | high |
| Gate decision logic | Bypassed | implemented code | `alpha_solver_entry._tree_of_thought` calls `evaluate_gates`; expert route mode logic also uses `evaluate_gates` for block/clarify decisions. | high |
| Expert route two-pass | Bypassed | implemented code, provider-scoped | `/v1/solve` has expert step-one preview prompt, step-two answer prompt, parse/default assumptions, and two provider calls for non-trivial expert requests when OpenAI mode is enabled. | high |
| Clarify/block/answer_with_assumptions modes | Bypassed | implemented code, provider-scoped | Expert route chooses `block`, `clarify`, `answer_with_assumptions`, or `direct`; deterministic clarify questions and block/clarify messages exist. | high |
| ReAct-lite | Bypassed | implemented code, narrow | `run_react_lite` handles simple arithmetic with deterministic parse/compute/self-check trace; `/v1/solve` can select it through `strategy == "react"` in local non-OpenAI mode. | medium |
| CoT self-validation | Bypassed | implemented code, narrow | `run_reasoning` can call `validate_answer` and correct simple arithmetic mismatches when confidence is below threshold. | medium |
| Plan runner and governance gates | Bypassed | implemented code, product/review surface | `Runner`, `run_plan`, `execute_plan`, and `run_cli` execute plan steps with budget, circuit-breaker, audit, policy, and governance checks. | product/review only |
| `/v1/solve` lifecycle | Bypassed by local LLM runtime path | implemented code, blocked for local LLM | FastAPI route handles hosted OpenAI provider mode, expert route, local deterministic ToT/ReAct fallback, metrics, and errors, but local LLM spec blocks `/v1/solve` exposure until a later lane. | product/review only until approved |
| Provider/model-set routing | Bypassed and blocked for local LLM fallback | implemented code, hosted-provider scoped | `_get_model_set`, `ModelSetResolver`, `OpenAIProviderClient`, provider requests, telemetry, and accounting are present for explicit OpenAI mode. | product/review only for local lane |
| Dashboard expert preview | Bypassed and blocked for local LLM | implemented code, supervised preview | Dashboard route renders plain vs expert panes, calls `/v1/solve`, applies OpenAI live preview guard and request cap, and carries non-claim disclaimer. | product/review only until approved |
| Portable SolverEnvelope orchestration | Bypassed | implemented code with portable fallback/stub components | `PortableAlphaSolver.solve` runs ToT, router, expert selector, SAFE-OUT, shortlist, diagnostics, and envelope validation. | high |
| Portable ToT implementation | Bypassed | stub/minimal | `PortableToTSolver` is documented as a deterministic ToT stub that mirrors envelope shape and budget events. | low-to-medium as-is; high if replaced with local-LLM ToT-lite calls |
| `alpha_solver_v225_p2_experts.py` | Bypassed | stub/minimal and inactive/unapproved | Inspected file contains pass-only expert classes and a minimal `AlphaSolver.solve` returning `Processed: ...`; no approval was found in this lane. | low; treat inactive |
