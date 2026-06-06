# Non-Active or Stubbed Surfaces

## Stub/minimal surfaces

- `alpha_solver_portable.py` `PortableToTSolver`: deterministic Tree-of-Thought stub that mirrors envelope shape and records budget events. It is useful as a contract reference, not proof of a local-LLM ToT implementation.
- `alpha.reasoning.cot.run_cot`: deterministic fallback guidance utility with fixed confidence and synthetic steps.
- `alpha.reasoning.cot_self_validate.validate_answer`: narrow deterministic validation helper focused on tiny arithmetic and regex shape checks.
- `alpha.reasoning.react_lite.run_react_lite`: narrow deterministic ReAct executor for simple arithmetic expressions.
- `alpha_solver_v225_p2_experts.py`: inactive for this lane. The inspected file contains pass-only expert classes plus a minimal `AlphaSolver` that returns a processed string and static low-confidence-like metadata. Treat it as inactive unless a later lane proves it is non-stub and explicitly approves it.

## Implemented but inactive for current local LLM runtime

- `alpha_solver_entry._tree_of_thought` and `alpha-solver-v91-python.py` `_tree_of_thought` are implemented entrypoints but not called by `run_configured_local_llm_runtime`.
- `service.app.solve` `/v1/solve` is implemented but blocked for current local LLM runtime exposure.
- `service.app` provider/model-set routing is implemented for explicit OpenAI mode but is not local LLM fallback.
- `alpha.webapp.routes.expert_preview` is implemented for supervised dashboard preview but is blocked for local LLM mode until a separate exposure lane.
- `alpha.core.runner` plan/governance execution is implemented but is not part of the local adapter response path.

## Unknowns

No inspected required surface is classified as `unknown`; however, this audit does not inspect every repository file and does not claim completeness beyond the requested source list plus `alpha_solver_v225_p2_experts.py`.
