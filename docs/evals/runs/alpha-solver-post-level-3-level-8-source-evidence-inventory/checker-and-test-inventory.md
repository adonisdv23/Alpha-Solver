# Checker and Test Inventory

## Guardrail and checker scripts Level 8 should review

| Path | Purpose in Level 8 inventory |
| --- | --- |
| `Makefile` | Defines `check-local-llm-orchestration-guardrails`, which chains local evidence-boundary, doc-path, and packet-consistency checks. |
| `scripts/check_local_llm_evidence_boundaries.py` | Static evidence-boundary guardrail for local LLM orchestration docs. |
| `scripts/check_local_llm_doc_paths.py` | Static doc path/link guardrail for local LLM orchestration docs. |
| `scripts/check_local_llm_packet_consistency.py` | Static packet consistency checker for selected-next state, blocker fallback lanes, boundary files, accepted decisions, and no-further-lane continuity. |
| `tests/test_local_llm_packet_consistency.py` | Unit coverage for packet consistency behavior. |
| `docs/local_llm_solver_orchestration_guardrails/checker-inventory.md` | Human-readable inventory of local orchestration guardrail checkers. |
| `docs/local_llm_solver_orchestration_guardrails/how-to-run.md` | Human-readable instructions for running local orchestration guardrails. |
| `docs/local_llm_solver_orchestration_guardrails/common-fixes.md` | Human-readable repair notes for static guardrail failures. |
| `docs/local_llm_solver_orchestration_guardrails/non-actions.md` | Guardrail documentation boundary and non-actions. |

## Required checks for this packet

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-8-source-evidence-inventory`
- Confirm changed files are only under `docs/evals/runs/alpha-solver-post-level-3-level-8-source-evidence-inventory/`.

## Checker boundary

The checker scripts are static documentation guardrails. They do not run local models, call Ollama, call hosted providers, exercise `/v1/solve`, exercise dashboard routes, deploy, benchmark, bill, or promote evidence.
