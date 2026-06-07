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

Use the full local LLM solver orchestration guardrail-suite target when it is available on the branch:

```bash
make check-local-llm-orchestration-guardrails
```

That aggregate target runs all three guardrail checkers:

```bash
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

Keep the direct checker commands as fallback or manual alternatives when a branch does not yet contain the aggregate target, when triaging one checker at a time, or when a review asks for direct script evidence. Running the aggregate target or the direct static commands does not start the release-readiness ladder.

## Suggested focused validation order

1. Run `git status --short` to confirm the working tree scope.
2. Run `git diff --name-only` and verify only the guardrail runbook docs changed.
3. Run `git diff --check` before checker execution.
4. Run the three direct checker commands above.
5. Run focused `rg` checks for checker names, selected-next state, blocker fallback lane, blocked claim terms, and explicit non-actions.

These steps preserve the evidence boundary because they inspect docs and static packet metadata only.
