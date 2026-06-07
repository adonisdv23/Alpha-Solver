# Checks Run

This file records the validation commands for the docs-only guardrail runbook lane.

## Required commands

```bash
git status --short
```

```bash
git diff --name-only
```

```bash
git diff --check
```

```bash
make check-local-llm-orchestration-guardrails
```

```bash
python scripts/check_local_llm_evidence_boundaries.py
```

```bash
python scripts/check_local_llm_doc_paths.py
```

```bash
python scripts/check_local_llm_packet_consistency.py
```

```bash
rg "check-local-llm-orchestration-guardrails|check_local_llm_evidence_boundaries.py|check_local_llm_doc_paths.py|check_local_llm_packet_consistency.py|NO_FURTHER_GUARDRAIL_RUNBOOK_LANES_SELECTED|ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-FIX-001" docs/local_llm_solver_orchestration_guardrails
```

```bash
git diff --name-only | grep -v '^docs/local_llm_solver_orchestration_guardrails/' && exit 1 || true
```

## Evidence boundary

The commands above are documentation and static checker commands only. They do not run local model inference, start Ollama, call hosted providers, expose `/v1/solve`, expose dashboard routes, add provider fallback, add hosted fallback, run benchmarks, perform billing work, update Google Sheets or backlog workbooks, or promote evidence.
