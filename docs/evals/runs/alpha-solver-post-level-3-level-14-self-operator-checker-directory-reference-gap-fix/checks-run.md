# Checks run

Final commands and results are recorded here after implementation:

- `git status --short` — pass.
- `git diff --name-only` — pass; changed files remained inside the allowed file surface.
- `git diff --check` — pass.
- `python -m pytest -q tests/test_self_operator_static_guardrails.py` — pass.
- `python scripts/check_local_llm_doc_paths.py` — pass.
- `python scripts/check_local_llm_evidence_boundaries.py` — pass.
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-directory-reference-gap-fix` — pass.
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle` — pass.
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension` — pass.
- Focused `rg` scan — pass; hits are checker/test/doc references to the repaired behavior or intentional exemption documentation.
- Forbidden-claim `rg` scan — pass; no forbidden claim remains in this packet.
