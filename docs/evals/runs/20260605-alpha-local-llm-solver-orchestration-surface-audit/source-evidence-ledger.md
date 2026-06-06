# Source Evidence Ledger

## Inspected source files

- `alpha/local_llm/provider_adapter.py`
- `alpha_solver_portable.py`
- `alpha_solver_entry.py`
- `alpha-solver-v91-python.py`
- `service/app.py`
- `alpha/core/runner.py`
- `alpha/reasoning/react_lite.py`
- `alpha/reasoning/cot.py`
- `alpha/reasoning/cot_self_validate.py`
- `alpha/webapp/routes/expert_preview.py`
- `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`
- `docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-retry-track-closeout/`
- `alpha_solver_v225_p2_experts.py` inspected only because this lane requires treating it inactive unless proven non-stub and approved.

## Evidence facts

### Local runtime adapter

- `LocalLLMRuntimeConfig.from_env` requires explicit local enablement, rejects hosted provider keys, validates endpoint/model/timeout, and builds `OllamaLocalHTTPBackend` only for `provider_mode=local_llm`.
- `validate_ollama_local_endpoint` accepts only loopback/localhost HTTP endpoint values without userinfo and rejects non-local endpoints before transport.
- `build_local_llm_adapter_request` loads the portable contract, separates system and user messages, and records `behavior_evidence=false`, `no_real_provider_call=true`, and `real_provider_call_enabled=false` metadata.
- `OllamaLocalHTTPBackend.generate` builds the payload, requires an injected/default transport, maps timeout/connection/malformed failures to adapter errors, and parses the response.
- `urllib_ollama_json_transport` validates local endpoint and finite timeout and posts JSON to the provided local endpoint with redirects disabled.
- `run_configured_local_llm_runtime` is intentionally not wired to `/v1/solve` or dashboard preview.

### Solver orchestration surfaces

- `alpha_solver_entry._tree_of_thought` loads the v91 implementation and adds gate evaluation through `evaluate_gates`.
- `alpha-solver-v91-python.py` `_tree_of_thought` builds configuration, instantiates `AlphaSolver`, calls `solver.solve`, stores diagnostics/config, runs accessibility checks, emits run summary, and returns an envelope-like dict.
- `PortableAlphaSolver.solve` runs ToT, routing, expert selection, SAFE-OUT, shortlist construction, diagnostics, and `SolverEnvelope` validation.
- `PortableToTSolver` is explicitly documented as a deterministic Tree-of-Thought stub.
- `PortableSafeOut` has deterministic CoT fallback and route notes for low confidence.

### API, provider, and dashboard surfaces

- `service.app.solve` exposes `/v1/solve`; when OpenAI mode is enabled, it uses model-set resolution, provider request building, expert route handling, telemetry/accounting, and provider error handling.
- `service.app` expert route performs a non-trivial two-pass flow: Step 1 preview JSON, parse/default assumptions, Step 2 final answer prompt, then mode selection and response assembly.
- `service.app` local non-OpenAI branch routes to `run_react_lite` for `strategy=react` or `_tree_of_thought` otherwise; it does not call `run_configured_local_llm_runtime`.
- `alpha.webapp.routes.expert_preview` is an authenticated/supervised preview route that calls `/v1/solve` twice, once plain and once expert, guarded for live OpenAI preview and carrying non-readiness disclaimers.

### Reasoning and governance surfaces

- `alpha.core.runner.run_reasoning` can run ReAct-lite or CoT and apply CoT self-validation.
- `alpha.core.runner` plan execution functions apply budget/circuit-breaker/audit/policy governance.
- `alpha.reasoning.react_lite` implements a deterministic arithmetic ReAct-style loop with safe-out halt results for regex mismatch or validation failure.
- `alpha.reasoning.cot` implements deterministic CoT fallback output.
- `alpha.reasoning.cot_self_validate` implements tiny arithmetic and regex shape validation.

### Spec and closeout boundaries

- `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` requires default-off optional local LLM mode, local/loopback endpoints, no provider keys, finite timeout, no hosted fallback, `behavior_evidence=false`, and blocks `/v1/solve` plus dashboard preview until later authorization.
- The closeout folder records terminal next action `STOP-HERE-LOCAL-LLM-RUNTIME-TRACK-CLOSED`, a bounded local loopback smoke result, and explicit non-claims for local quality, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, and Alpha superiority.
