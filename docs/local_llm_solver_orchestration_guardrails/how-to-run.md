# How to Run the Guardrail Suite

## Normal command

Run the aggregate suite from the repository root:

```bash
make check-local-llm-orchestration-guardrails
```

The target runs all three guardrail checkers:

```bash
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

## Manual fallback commands

Use direct commands only when isolating a failure class:

```bash
python scripts/check_local_llm_evidence_boundaries.py
```

```bash
python scripts/check_local_llm_doc_paths.py
```

```bash
python scripts/check_local_llm_packet_consistency.py
```

## Recommended operator flow

1. Run `make check-local-llm-orchestration-guardrails` first.
2. If it fails, read the checker name in the failure output.
3. Run the matching direct checker command only if you need a smaller diagnostic loop.
4. Fix the authoritative documentation artifact that the checker reports.
5. Re-run the aggregate target.
6. Do not fix a failure by weakening the checker.
7. Do not fix a failure by moving claims into logs or checks-run files.
8. Do not infer missing packet fields from memory; use authoritative packet files and source-of-truth docs.

## Evidence boundary

These commands are deterministic documentation checks. They do not run local model inference, start Ollama, call hosted providers, expose `/v1/solve`, expose dashboard routes, add provider fallback, add hosted fallback, run benchmarks, perform billing work, update Google Sheets or backlog workbooks, or promote evidence.
