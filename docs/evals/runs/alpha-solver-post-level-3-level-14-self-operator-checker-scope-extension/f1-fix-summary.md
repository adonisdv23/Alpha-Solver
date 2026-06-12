# F-1 fix summary

F-1 identified that the static evidence-boundary and doc-path checkers did not automatically cover the `alpha-solver-post-*` Self Operator packet family or the Council audit evidence bundle.

This lane fixes that shared root cause by adding default checker scope for `docs/evals/runs/alpha-solver-post-*` packet docs, preserving legacy local-LLM scope, and adding focused tests that prove the new paths are included and enforced. The evidence-boundary checker uses explicit claim-boundary language rather than generic nearby words such as standalone `before`, `no`, or `not` as sufficient suppression.

This is not a runtime, provider, model, API, dashboard, deployment, billing, credential, secret, `/v1/solve`, or final-status CLI change.
