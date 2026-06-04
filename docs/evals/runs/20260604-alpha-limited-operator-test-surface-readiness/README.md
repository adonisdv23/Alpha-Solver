# Limited Alpha Operator Test Surface Readiness Review

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-READINESS-001`

Status: docs-only surface-readiness review complete; no operator-test results imported.

## Purpose

Determine the correct execution surface for the limited Alpha operator test before any operator-test results are imported, scored, summarized, or treated as pass/fail evidence.

This lane responds to the local manual preview concern: `/dashboard/expert-preview` was attempted in local mode, but the plain and Alpha preview panes appeared to echo the submitted prompt rather than produce substantive answers. Those screenshots and observations are not Alpha pass/fail results and are not imported here.

## Source files reviewed

- `alpha/webapp/routes/expert_preview.py`
- `.specs/UI-PREVIEW-LOCAL-SMOKE-001.md`
- `service/app.py`
- `alpha_solver_portable.py`
- `alpha_solver_entry.py`
- `alpha-solver-v91-python.py`
- `docs/evals/runs/20260604-alpha-limited-operator-test/README.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-packet.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-task-set.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-claim-boundaries.md`
- `docs/evals/runs/20260604-alpha-limited-operator-test/operator-test-preservation-checklist.md`
- `docs/evals/runs/20260604-alpha-brevity-control-refinement/README.md`

## Summary decision

The current local supervised preview is valid only as a UI/local smoke surface. It is not a valid behavior-testing surface for the limited operator test if it merely echoes prompts or produces deterministic placeholder/offline output.

The limited operator test should not be run on the current local `/dashboard/expert-preview` surface as behavior evidence. ChatGPT project-thread testing may be used only as prompt-contract/manual simulation evidence, not product/runtime evidence. A valid product-level operator test requires a separately approved product surface that is proven to consume the intended Alpha behavior contract and can produce substantive answers under authorized execution conditions.

## Recommended next lane

Recommended next lane: `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-FIX-001`.

This is recommended because the current local preview is blocked for behavior testing, ChatGPT-thread testing is not product/runtime evidence, and live provider or runtime wiring work would require separate authorization before any product-level operator-test execution.
