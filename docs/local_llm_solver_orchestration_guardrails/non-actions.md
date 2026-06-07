# Non-Actions and Evidence Boundary

This runbook is documentation only. It records how to operate the guardrail checker suite and how to triage failures without weakening the guardrails.

## Explicit non-actions

This lane does not:

- Modify `Makefile`.
- Modify `.github/workflows/ci.yml`.
- Modify checker scripts.
- Modify tests.
- Modify runtime behavior.
- Modify local LLM provider adapter behavior.
- Modify operator CLI behavior.
- Modify preserved source artifacts.
- Modify Level 2 or Level 3 closeout packets.
- Modify `docs/evals/runs/alpha-solver-post-level-3-release-readiness-ladder/`.
- Run local model inference.
- Run Ollama.
- Call hosted providers.
- Expose or call `/v1/solve`.
- Expose or call dashboard routes.
- Add provider fallback.
- Add hosted fallback.
- Run benchmarks.
- Perform billing work.
- Update Google Sheets or backlog workbooks.
- Promote evidence.

## Boundary for unsupported claims

This runbook does not prove runtime readiness, model quality, provider behavior, billing behavior, dashboard behavior, `/v1/solve` behavior, or benchmark outcomes. If those claims are needed, they require separate scoped evidence lanes and must not be inferred from this guardrail runbook.
