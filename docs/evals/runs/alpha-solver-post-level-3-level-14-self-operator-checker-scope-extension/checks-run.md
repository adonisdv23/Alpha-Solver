# Checks run

Commands run for this lane:

```bash
git status --short
git diff --name-only
git diff --check
python -m pytest -q tests/test_self_operator_static_guardrails.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle
rg -n "\\bbefore\\b|radius=12|referenced local LLM repo path does not exist|referenced local LLM/post-Level repo path does not exist|production readiness|MVP readiness|benchmark evidence" scripts/check_local_llm_evidence_boundaries.py scripts/check_local_llm_doc_paths.py tests/test_self_operator_static_guardrails.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension
```

The focused test file was `tests/test_self_operator_static_guardrails.py` because it is the existing Self Operator static guardrail test file.

The focused code scan was reviewed to confirm there is no standalone `\bbefore\b` boundary-language pattern, no `radius=12` context window, and no stale `referenced local LLM repo path does not exist` message. It also shows the updated local LLM/post-Level missing-reference message and the intentional readiness/evidence terms used by the checker and regression fixtures.
