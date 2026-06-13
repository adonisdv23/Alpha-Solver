# Checker Scope Before / After

## Before

- `scripts/check_local_llm_doc_paths.py` scanned local LLM docs and `alpha-solver-post-*` packets, but did not explicitly include OpenAI packet families in `is_scanned_doc` or reference marker detection.
- `scripts/check_local_llm_evidence_boundaries.py` scanned local LLM docs and `alpha-solver-post-*` packets, but did not explicitly include OpenAI packet families in `is_relevant_doc`.
- `scripts/check_local_llm_packet_consistency.py` discovered packet directories by marker list that omitted `openai-*`, `local-openai-*`, and `alpha-solver-openai-*` packet families.

## After

- `scripts/check_local_llm_doc_paths.py` includes `docs/evals/runs/openai-*`, `docs/evals/runs/local-openai-*`, and `docs/evals/runs/alpha-solver-openai-*` in default scanning and checked-reference detection.
- `scripts/check_local_llm_evidence_boundaries.py` includes those OpenAI packet families in relevant docs.
- `scripts/check_local_llm_packet_consistency.py` includes those OpenAI packet families in packet directory discovery.
- Existing local LLM and `alpha-solver-post-*` scope remains in place.
- Source-artifact exclusions remain in place.

## Applicability note

All three checkers are applicable to the required OpenAI packet directories after this change. No checker was intentionally excluded from any required packet.
