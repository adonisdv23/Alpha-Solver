# Checker scope before/after inventory

Lane ID: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-CHECKER-SCOPE-EXTENSION-001`

## Before edits

| Checker file | Current packet roots scanned | alpha-solver-post-* included? | Council bundle included? | Gap |
|---|---|---|---|---|
| `scripts/check_local_llm_evidence_boundaries.py` | `docs/local_llm_solver_orchestration*` and `docs/evals/runs/*local-llm-solver-orchestration*` text docs, excluding source artifacts. | No. | No, except only if manually scanned outside default scope. | Self Operator post-Level packet family and Council audit evidence bundle were not in default automated evidence-boundary scope. |
| `scripts/check_local_llm_doc_paths.py` | `docs/local_llm_solver_orchestration_operator_guide`, `docs/evals/runs/local-llm-solver-orchestration-index`, and Level 3 local-LLM closeout/import-final-decision docs, excluding source artifacts. | No. | No, except only if manually scanned outside default scope. | Self Operator post-Level packet references were not in default automated doc-path scope. |

## After edits

| Checker file | Current packet roots scanned | alpha-solver-post-* included? | Council bundle included? | Gap |
|---|---|---|---|---|
| `scripts/check_local_llm_evidence_boundaries.py` | Existing local-LLM docs plus every text doc under `docs/evals/runs/alpha-solver-post-*`, excluding source artifacts. | Yes. | Yes, through the `alpha-solver-post-*` packet prefix and explicit Council bundle constant. | Closed for default evidence-boundary scanning of current and future post-Level packet docs. |
| `scripts/check_local_llm_doc_paths.py` | Existing local-LLM doc roots plus every text doc under `docs/evals/runs/alpha-solver-post-*`, excluding source artifacts. | Yes. | Yes, through the `alpha-solver-post-*` packet prefix and required Council bundle source-of-truth path. | Closed for default doc-path scanning of current and future post-Level packet docs. |

## Notes

- The extension is checker/test/docs-only.
- Product runtime, provider behavior, hosted models, local models, external APIs, browser automation, deployment, billing, credentials, secrets, dashboards, `/v1/solve`, and final-status CLI behavior were not changed.
- Prior evidence packets were not edited.
