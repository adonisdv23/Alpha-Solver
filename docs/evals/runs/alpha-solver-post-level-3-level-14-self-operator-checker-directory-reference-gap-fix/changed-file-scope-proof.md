# Changed-file scope proof

| File | Change made | Why needed | Evidence source | Boundary preserved |
|---|---|---|---|---|
| `scripts/check_local_llm_doc_paths.py` | Preserve checked suffix-less local-LLM and post-Level directory references for missing-path reporting; normalize trailing slash for existence; add intentional missing-reference exemption. | Fix N-1/F-1 successor checker gap without touching product code. | Fable N-1 audit finding and local preflight inspection of checker functions. | No runtime, provider, API, dashboard, or evidence-boundary checker behavior changed. |
| `tests/test_self_operator_static_guardrails.py` | Add focused tests for missing post-Level directories, missing legacy local-LLM directories, trailing slash, tmp-root forwarding, unresolved glob patterns, and intentional historical/non-action exemptions. | Prove the checker behavior change and prevent regression. | Required lane test matrix. | Tests use inert tmp_path docs and do not run models/providers or mutate prior evidence. |
| `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-checker-directory-reference-gap-fix/` | Add this packet documenting scope, checks, boundaries, and non-actions. | AUDIT-005 requires a dedicated documentation packet. | AUDIT-005 decision boundary and lane instructions. | Prior evidence packets and Council bundle files are not modified. |
