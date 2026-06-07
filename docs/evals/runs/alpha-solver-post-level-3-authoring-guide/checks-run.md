# Checks Run

This guide is docs-only. Checks should confirm authoring-guide consistency and guardrail compatibility without running local model inference, Ollama, validation, smoke, hosted providers, `/v1/solve`, dashboard routes, provider fallback, hosted fallback, benchmarks, billing work, evidence promotion, Google Sheets updates, or backlog workbook updates.

## Required checks for this PR

- `git status --short`
- `git diff --name-only`
- `git diff --name-only --cached`
- `git diff --check`
- `git diff --check --cached`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_evidence_boundaries.py`
- `python scripts/check_local_llm_doc_paths.py`
- `python scripts/check_local_llm_packet_consistency.py`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-authoring-guide`
- `rg "NO_FURTHER_RELEASE_READINESS_AUTHORING_GUIDE_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-RELEASE-READINESS-AUTHORING-GUIDE-FIX-001|check-local-llm-orchestration-guardrails|checks-run|selected-next|blocker fallback|evidence boundary" docs/evals/runs/alpha-solver-post-level-3-authoring-guide`
- `git diff --name-only -- 'docs/evals/runs/**/source-artifact/**'`
- `git diff --name-only --cached -- 'docs/evals/runs/**/source-artifact/**'`
- `git diff --name-only -- alpha service cli scripts tests Makefile .github/workflows/ci.yml`
- `git diff --name-only --cached -- alpha service cli scripts tests Makefile .github/workflows/ci.yml`

## Interpretation boundary

Passing checks only confirms static documentation consistency within checker scope. It does not establish release readiness, model quality, provider readiness, dashboard readiness, `/v1/solve` readiness, billing readiness, benchmark evidence, MVP readiness, or production readiness.

## Results recorded for this packet

- PASS: `git status --short` showed only new staged files under `docs/evals/runs/alpha-solver-post-level-3-authoring-guide/`.
- PASS: `git diff --name-only` produced no output after staging, confirming no unstaged tracked-file changes.
- PASS: `git diff --name-only --cached` showed only new authoring-guide files.
- PASS: `git diff --check` reported no unstaged whitespace errors.
- PASS: `git diff --check --cached` reported no staged whitespace errors.
- PASS: `make check-local-llm-orchestration-guardrails` passed.
- PASS: `python scripts/check_local_llm_evidence_boundaries.py` passed.
- PASS: `python scripts/check_local_llm_doc_paths.py` passed.
- PASS: `python scripts/check_local_llm_packet_consistency.py` passed.
- PASS: `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-authoring-guide` passed and reported `1 packet directories scanned`, confirming the new authoring-guide packet was checked explicitly by path.
- PASS: `rg "NO_FURTHER_RELEASE_READINESS_AUTHORING_GUIDE_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-RELEASE-READINESS-AUTHORING-GUIDE-FIX-001|check-local-llm-orchestration-guardrails|checks-run|selected-next|blocker fallback|evidence boundary" docs/evals/runs/alpha-solver-post-level-3-authoring-guide` found the selected-next action, blocker fallback lane, guardrail command, checks-run references, and boundary terms.
- PASS: `git diff --name-only -- 'docs/evals/runs/**/source-artifact/**'` produced no output, confirming no unstaged preserved source artifact files changed.
- PASS: `git diff --name-only --cached -- 'docs/evals/runs/**/source-artifact/**'` produced no output, confirming no staged preserved source artifact files changed.
- PASS: `git diff --name-only -- alpha service cli scripts tests Makefile .github/workflows/ci.yml` produced no output, confirming no unstaged runtime/provider/dashboard/API/checker/test/Makefile/CI files changed.
- PASS: `git diff --name-only --cached -- alpha service cli scripts tests Makefile .github/workflows/ci.yml` produced no output, confirming no staged runtime/provider/dashboard/API/checker/test/Makefile/CI files changed.

These results are not authoritative decisions. Authoritative selected-next and fallback state live in `selected-next-action.md`, `blocker-fallback-lane.md`, and `README.md`.
