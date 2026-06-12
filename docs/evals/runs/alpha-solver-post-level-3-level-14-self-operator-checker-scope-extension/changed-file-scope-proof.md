# Changed-file scope proof

| File surface | Change | Why in scope |
|---|---|---|
| `scripts/check_local_llm_evidence_boundaries.py` | Extend relevant-doc detection to `docs/evals/runs/alpha-solver-post-*`; add explicit Council bundle constant; tune boundary-context recognition for existing post-Level governance docs. | Required checker tooling surface for F-1. |
| `scripts/check_local_llm_doc_paths.py` | Extend scan set and reference detection to `docs/evals/runs/alpha-solver-post-*`; add Council bundle to required source-of-truth paths; ignore glob/shell patterns and normalize line-suffixed references. | Required checker tooling surface for F-1. |
| `tests/test_self_operator_static_guardrails.py` | Add focused tests for post-packet inclusion, Council bundle inclusion, legacy coverage preservation, forbidden readiness term detection, and doc-path enforcement. | Required focused test surface for checker behavior. |
| `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-scope-extension/*.md` | Add the lane documentation packet. | Required docs packet for the F-1 fix lane. |

No prior evidence packet files were changed.
