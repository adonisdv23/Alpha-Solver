# Integration Risk Matrix

| Integration candidate | Risk level | Main risks | Risk controls for later lane |
| --- | --- | --- | --- |
| Local expert two-pass | medium | Prompt recursion, local latency, malformed first-pass JSON, confidence overclaiming, accidental provider routing. | Use local adapter only, require bounded parser fallback, preserve `behavior_evidence=false`, no hosted fallback, focused smoke. |
| Local orchestration envelope | medium | Confusing adapter non-evidence result with behavior evidence; widening SolverEnvelope behavior without spec approval. | Keep new local envelope schema narrow, record provenance, validate no `/v1/solve` or dashboard exposure during implementation. |
| Local confidence/clarify/block gates | medium | Miscalibrated local confidence, excessive clarify/block, unsupported certainty. | Start with deterministic thresholds and explicit modes; test low-confidence, missing-confidence, empty-answer, and prompt-echo cases. |
| Local ToT-lite | medium-high | Extra local calls increase latency and failure surface; candidate selection can overclaim. | Limit depth/width, require fail-closed per candidate, cap timeouts, keep non-evidence labels until quality lane. |
| `/v1/solve` exposure later | high | Public API semantics, routing, observability, billing/provider separation, and readiness claims. | Keep blocked until local orchestration implementation and smoke pass; use a separate exposure lane. |
| Dashboard exposure later | high | Operator UI can be mistaken for readiness or quality validation; possible provider/preview guard confusion. | Keep blocked until local orchestration implementation and smoke pass; preserve disclaimers and caps in separate lane. |
| Provider fallback/hybrid routing | high | Silent hosted fallback would violate the local LLM contract and confuse provenance. | Keep blocked unless a separate explicit hybrid lane authorizes fallback triggers, opt-in, labels, credentials, and tests. |
| Plan runner/governance integration | medium-high | Broadens scope into plan execution, policy, budgets, files, and audit artifacts. | Defer until response orchestration is stable; do not include in first local LLM implementation. |
