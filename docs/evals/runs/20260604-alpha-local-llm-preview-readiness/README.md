# Alpha Local LLM Preview Readiness

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: docs-only readiness spike.

## Purpose

Determine whether Alpha Solver could support a future local LLM preview path, likely Ollama-style or OpenAI-compatible local endpoint style, that consumes the intended portable Alpha behavior contract from `alpha_solver_portable.py` while avoiding the current smoke-only prompt-echo failure mode and preserving clean evidence boundaries.

## Source files reviewed

- `alpha_solver_portable.py`
- `alpha_solver_entry.py`
- `alpha-solver-v91-python.py`
- `service/app.py`
- `alpha/webapp/routes/expert_preview.py`
- `.specs/UI-PREVIEW-LOCAL-SMOKE-001.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-surface-readiness/README.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-surface-readiness/blocked-surface-record.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-surface-readiness/surface-readiness-review.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-surface-readiness/surface-decision-matrix.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test-surface-readiness/next-surface-options.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test/README.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-packet.md`
- `docs/evals/runs/20260604-alpha-operator-test-batch-c-runtime-firewall/README.md`
- `alpha/providers/base.py`
- `alpha/providers/openai.py`
- `service/models/modelset_registry.py`
- `service/models/modelset_resolver.py`
- `service/config/model_sets.yaml`
- `.env.example`

Repository search terms included: `MODEL_PROVIDER`, `provider`, `adapter`, `modelset`, `OpenAI`, `Anthropic`, `local`, `ollama`, `base_url`, `chat/completions`, `generate`, `alpha_solver_portable`, `alpha_solver_entry`, and `_tree_of_thought`.

## Files added

- `README.md`
- `local-llm-readiness-review.md`
- `current-runtime-path-trace.md`
- `portable-contract-consumption-gap.md`
- `ollama-provider-option.md`
- `local-llm-surface-options.md`
- `implementation-scope-proposal.md`
- `local-llm-evidence-boundaries.md`
- `local-llm-readiness-checklist.md`
- `recommended-next-lane.md`

## Summary decision

Local LLM preview support appears feasible in principle because the repo already has typed provider request/result structures, an injectable provider-client seam, model-set resolution, and a supervised preview route that can call the shared solve function. It is not ready as-is: `MODEL_PROVIDER=local` currently preserves deterministic local/offline smoke behavior through the v91 `_tree_of_thought` path rather than loading `alpha_solver_portable.py`, and `/dashboard/expert-preview` does not prove portable-contract execution today. A future lane should first prove portable-contract consumption through a narrowly isolated local-LLM provider or preview wrapper before any product/runtime evidence can be accepted.

## No-results / no-implementation boundary

This packet is docs-only. It does not implement local LLM support, add an Ollama adapter, call Ollama, call OpenAI, call Anthropic, call any provider, run `/v1/solve` as evidence, execute operator tests, generate model outputs, import operator results, score or rescore anything, update Google Sheets, start Batch C, or change runtime/provider/model/routing behavior.
