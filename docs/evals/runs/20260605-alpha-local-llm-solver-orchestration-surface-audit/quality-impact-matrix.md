# Quality Impact Matrix

## Interpretation boundary

Impact estimates are implementation-surface estimates only. They are not local model quality evidence, benchmark evidence, runtime evidence, or Alpha superiority evidence.

| Implemented surface | Estimated direct response-quality impact | Why it could affect response quality if integrated later | Current blocker |
| --- | --- | --- | --- |
| Local expert two-pass | high | Adds a first pass for considerations, assumptions, and confidence, then uses those fields to shape a final answer that preserves requested deliverable format. | Currently implemented in hosted `/v1/solve` expert route, not local LLM path. |
| Local orchestration envelope | high | Would wrap model output with solution, confidence, safe-out state, route explanation, shortlist, diagnostics, metadata, and validation structure. | Current local path returns adapter result only, not `SolverEnvelope`. |
| Local confidence/clarify/block gates | high | Would prevent low-confidence output from being presented as direct answer, ask clarifying questions where appropriate, and block unsafe/unsupported final answers. | Existing gates are in v91 wrapper and hosted expert route; local LLM adapter has only fail-closed transport/output guards. |
| Local ToT-lite | high | Could ask the local model for multiple candidate paths or structured refinements before selecting/finalizing. | Existing ToT is deterministic/v91/portable and not wired to the local LLM adapter. |
| ReAct-lite | medium | Deterministic arithmetic ReAct can improve simple calculation handling and traceability for a narrow class of prompts. | Not connected to local LLM adapter; `/v1/solve` strategy routing only. |
| CoT self-validation | medium | Can validate and correct simple arithmetic-style CoT answers under narrow conditions. | Used by `run_reasoning`, not current local adapter runtime. |
| Plan runner and governance gates | product/review only | Useful for execution governance, audit logs, budgets, and policy dry-run, but not directly answer-quality shaping for a chat response. | Separate plan execution surface, not local runtime response path. |
| `/v1/solve` exposure | product/review only | Provides API lifecycle, metrics, routing, and error handling, but should expose local LLM only after orchestration smoke passes. | Explicitly blocked by local LLM spec and prior closeout. |
| Provider/model-set routing | product/review only | Hosted provider model selection does not improve the pure local path unless a separate explicit hybrid lane authorizes fallback/routing. | Provider fallback is prohibited for local mode. |
| Dashboard expert preview | product/review only | Helps operator review plain vs expert outputs, but should not be a first quality integration for local runtime. | Explicitly blocked until local orchestration implementation and smoke pass. |
