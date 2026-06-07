# How to Run the Guardrail Checkers

Run these commands from the repository root.

## Direct checker commands

```bash
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

The direct commands are deterministic, offline documentation checks. They should not start Ollama, call hosted providers, expose `/v1/solve`, expose dashboard routes, run benchmarks, or promote evidence.

## Aggregate Makefile coverage

The current `Makefile` contains an aggregate target for the evidence-boundary checker only:

```bash
make check-local-llm-evidence-boundaries
```

No current aggregate Makefile target was found for the docs path/link checker or the packet consistency checker, so run those checkers directly:

```bash
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

## Suggested focused validation order

1. Run `git status --short` to confirm the working tree scope.
2. Run `git diff --name-only` and verify only the guardrail runbook docs changed.
3. Run `git diff --check` before checker execution.
4. Run the three direct checker commands above.
5. Run focused `rg` checks for checker names, selected-next state, blocker fallback lane, blocked claim terms, and explicit non-actions.

These steps preserve the evidence boundary because they inspect docs and static packet metadata only.
