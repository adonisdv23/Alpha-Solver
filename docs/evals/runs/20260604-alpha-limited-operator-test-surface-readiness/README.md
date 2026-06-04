# Limited Alpha Operator Test Surface Readiness Review

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-READINESS-001`

Status: docs-only surface-readiness review complete; no operator-test results imported.

## Purpose

Determine the correct execution surface label for the limited Alpha operator test before any operator-test results are imported, scored, summarized, or treated as pass/fail evidence.

This lane responds to the local manual preview concern: `/dashboard/expert-preview` was attempted in local mode, but the plain and Alpha preview panes appeared to echo the submitted prompt rather than produce substantive answers. Those screenshots and observations are not Alpha pass/fail results and are not imported here.

This review preserves the already-approved limited operator-test packet scope from PR #273: a portable Alpha behavior-contract manual test. It does not convert that packet into a product/runtime-surface test.

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

Keep two tracks separate:

1. Portable-contract manual simulation track: valid for manually testing the portable Alpha behavior contract when correctly labeled as simulation/manual portable-contract evidence only. This aligns with the current operator-test packet. It is not product/runtime evidence, `/v1/solve` evidence, provider evidence, benchmark validation, MVP validation, production-readiness evidence, or broad Alpha-superiority evidence.
2. Product/runtime execution-surface track: a separate future track needed only if the project wants product/runtime operator evidence. The current local supervised preview is valid only as a UI/local smoke surface and remains blocked/invalid for behavior testing if it merely echoes prompts or produces deterministic placeholder/offline output.

The current operator packet should not be changed into a product/runtime operator test unless a separate approved lane changes that scope.

## Recommended next lane

Recommended next lane: `ALPHA-LIMITED-OPERATOR-TEST-PROMPT-CONTRACT-SIMULATION-001`.

This recommendation preserves the original PR #273 packet scope: manual portable-contract operator testing. `ALPHA-LIMITED-OPERATOR-TEST-SURFACE-FIX-001` remains an optional future lane only if Adonis explicitly wants product/runtime surface evidence.
