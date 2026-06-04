# Post-Improvement Measurement Surface Decision

Status: planning/decision only
Lane: `OUTPUT-DIFF-POST-IMPROVEMENT-RUN-001`

This packet does not run capture, call providers, rescore outputs, create final prompts, change runtime behavior, change provider behavior, change model configuration, change routing, change `/v1/solve`, update Sheets, or start Batch C.

## Central measurement question

What surface can validly measure the PR #263 minimal behavior-contract change?

PR #263 updated the portable prompt/protocol contract in `alpha_solver_portable.py` by adding the minimal behavior contract and `minimal_behavior_contract_summary()`. The committed evidence inspected for this packet does not show matching changes to provider adapters, model configuration, routing, `/v1/solve`, scoring rubrics, scored artifacts, capture scripts, Sheets, or Batch C.

## Surface classification

| Surface | Role | PR #263 affects directly? | Existing capture can measure it? | Provider calls required? | Use authorized now? | Risk level |
|---|---|---:|---:|---:|---:|---|
| `alpha_solver_portable.py` | Standalone portable behavior contract and portable-spec prompt/protocol surface. | Yes. The minimal behavior contract lives here. | Not by the existing live-capture path unless the future packet explicitly loads this file as the Alpha behavior contract. | Future output-quality measurement would require approved provider capture; offline inspection does not. | Planning only now; no capture now. | Medium if measured with a frozen packet; high if assumed to affect runtime without evidence. |
| `minimal_behavior_contract_summary()` in `alpha_solver_portable.py` | Offline summary helper for the new minimal contract. | Yes. | Existing live capture does not target this helper. Offline tests can verify compliance surface only. | No for offline checks; yes for future output-quality measurement if compared through providers. | Offline/planning use only now. | Low for contract compliance; high if treated as answer-quality proof. |
| `alpha-solver-v91-python.py` | Modular/reference entrypoint for deterministic Tree-of-Thought behavior used through `alpha_solver_entry.py`. | No direct PR #263 change observed. | Existing `/v1/solve` local mode can exercise this path, not the portable prompt/protocol contract. | No for local mode; yes only when provider path is enabled elsewhere. | Inspect only now. | Medium because it is a different surface from the PR #263 portable contract. |
| `alpha_solver_entry.py` | Import bridge that loads `alpha-solver-v91-python.py` and exposes `_tree_of_thought()`/`get_solver()`. | No direct PR #263 change observed. | Existing `/v1/solve` local mode reaches this bridge, not `alpha_solver_portable.py`. | No for local mode. | Inspect only now. | Medium because measuring it would not measure the changed portable prompt/protocol surface. |
| `/v1/solve` in `service/app.py` | Runtime API endpoint; dispatches to provider path when provider mode is enabled, otherwise to local `react` or `_tree_of_thought()` path. | No direct PR #263 change observed. | Existing live-capture through `/v1/solve` would measure the service/provider/local runtime path, not the changed portable file, unless separately wired. | Yes for live provider capture; no for local deterministic calls. | Not authorized now. | High for post-improvement claims because the inspected endpoint does not consume `alpha_solver_portable.py`. |
| Existing capture workflow/docs | Eval capture and blind-scoring process for A3-1 and Batch B artifacts. | No direct PR #263 change observed. | It can preserve and score captured outputs, but it does not itself prove that Alpha output used the portable contract. | Yes for new live capture. | Not authorized now. | High if reused as proof without a frozen packet that binds the portable contract to the Alpha output surface. |
| Model-set/provider configuration | Runtime provider/model selection surface. | No direct PR #263 change observed. | Existing capture can measure configured provider/model behavior, not the portable contract by itself. | Yes for live provider capture. | Not authorized now. | High if model/provider drift is confused with the portable contract change. |
| Scoring rubric and scored artifacts | Evaluation artifact and scoring surface. | No direct PR #263 change observed. | They measure outputs after capture; they do not generate or wire the changed Alpha behavior. | No for reading artifacts; provider calls only for future capture. | Inspect only now. | Medium if score math is over-read as proof of a later change. |

## Decision

`CREATE FROZEN PROMPT PACKET FIRST`

The valid future measurement surface is the portable prompt/protocol surface, not the current `/v1/solve` surface, unless a future approved change wires `/v1/solve` to consume `alpha_solver_portable.py`. Because this PR is planning-only and must not create final holdout prompts, the next operator step should be a separate frozen prompt-packet or portable-surface diagnostic packet that explicitly states how the Alpha condition loads the portable contract.

## Reasoning

- Portable prompt/protocol behavior: PR #263 changed `alpha_solver_portable.py`, including the minimal behavior contract and summary helper. A valid post-improvement measurement must cause the Alpha condition to use that portable contract.
- Runtime API behavior: inspected `/v1/solve` imports `_tree_of_thought` from `alpha_solver_entry.py`, chooses provider mode only when the provider environment mode is enabled, and otherwise uses local `react` or `_tree_of_thought()` behavior. The inspected endpoint does not import or call `alpha_solver_portable.py`.
- Provider/model/routing behavior: PR #263 did not change provider adapters, model sets, routing, or selection behavior. A provider-backed `/v1/solve` capture would therefore risk measuring provider/model/runtime behavior rather than the portable contract change.
- Scoring/eval artifact behavior: A3-1 and Batch B artifacts are preserved evidence for prior pilots. They can inform design and score-math checks, but they cannot by themselves measure the later PR #263 behavior change.

## Measurement risk

- Measuring the wrong surface: a `/v1/solve` live-capture run should not be presented as measuring PR #263 unless the endpoint is proven to consume the portable contract.
- Reusing Batch B prompts as proof: Batch B prompts were heavily used in planning and implementation, so reuse alone would be weak post-improvement proof.
- Prompt contamination: final post-improvement prompt text should be created only in a separate approved packet with contamination controls.
- Over-reading offline tests as runtime behavior: offline tests verify contract compliance, not provider output quality or `/v1/solve` behavior.
- Broad validation claims: limited pilots and planning artifacts do not support MVP validation, broad Alpha superiority, broad plain-provider inferiority, answer-quality superiority generally, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration.
- Provider/model drift: future provider-backed measurement must record model/provider conditions without treating drift as the effect of PR #263.
- Unblinding or scorer-bias leakage: scorer-facing packets must remain blinded, and unblinding maps must remain operator-only until scoring is complete.

## Recommendation

Open a separate operator-approved lane, preferably `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`, to create a frozen prompt packet and capture instructions that explicitly load `alpha_solver_portable.py` as the Alpha portable behavior contract. Do not run capture or score outputs until that packet is approved and frozen.
