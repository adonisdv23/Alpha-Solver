# Checks run

Commands run for this lane:

```bash
git status --short
git diff --name-only
python -m pytest -q tests/test_self_operator_static_guardrails.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle
git diff --check
```

The focused test file was `tests/test_self_operator_static_guardrails.py` because it is the existing Self Operator static guardrail test file.
