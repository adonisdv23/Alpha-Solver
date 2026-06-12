# Test coverage notes

Focused test file used: `tests/test_self_operator_static_guardrails.py`.

Reason: this existing file already contains Self Operator static guardrail tests, so extending it keeps the checker-scope assertions near related static safety coverage without creating a parallel test surface.

The added tests prove:

- `alpha-solver-post-*` packet paths are included by both checkers.
- The Council audit evidence bundle path is included by both checkers.
- Legacy local-LLM paths remain included.
- A controlled fixture containing a forbidden readiness term under an `alpha-solver-post-*` path is caught by the evidence-boundary checker.
- Generic nearby wording such as `before`, or generic `no`/`not` text several lines away, does not suppress forbidden readiness findings without explicit claim-boundary language.
- Explicit nearby claim-boundary wording such as `This does not claim production readiness` or `No readiness claim is made` may suppress the finding.
- A controlled fixture containing a missing checked doc path under an `alpha-solver-post-*` path is caught by the doc-path checker.
