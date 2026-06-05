# Local LLM Post-Smoke Decision Framework

Lane ID: `ALPHA-LOCAL-LLM-POST-SMOKE-DECISION-FRAMEWORK-001`

Status: docs-only decision framework prepared before any smoke result is imported or interpreted.

## Purpose

This directory defines the allowed post-smoke decision framework for a future local LLM smoke result import lane. It is a framework only.

No smoke result is imported, summarized, inferred, or interpreted here. This lane does not inspect raw smoke artifacts, sanitized smoke imports, operator output, model output, endpoint responses, logs, or missing smoke results.

## Source files reviewed

This framework is bounded by the current local LLM packet, locality hardening, review, authorization, adapter seam, and offline tests:

- `docs/evals/runs/20260605-alpha-local-llm-endpoint-locality-hardening/`
- `docs/evals/runs/20260605-alpha-local-llm-endpoint-locality-review-gate/`
- `docs/evals/runs/20260605-alpha-local-llm-smoke-authorization-refresh/`
- `docs/evals/runs/20260605-alpha-local-llm-smoke-test-packet/`
- `alpha/local_llm/provider_adapter.py`
- `tests/test_local_llm_provider_adapter.py`

## Files in this framework

- `README.md`
- `decision-framework.md`
- `outcome-branches.md`
- `success-criteria.md`
- `failure-classification.md`
- `blocked-claims.md`
- `evidence-boundary.md`
- `framework-preservation-checklist.md`
- `recommended-next-lane.md`

## Decision rule

A later actual decision lane must select exactly one next lane based on imported evidence. If imported evidence appears to match more than one branch, the later decision must choose the narrowest branch that resolves the immediate blocker and must not merge branches into a broader readiness claim.

## Recommended next lane

`ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001`

This next lane must not run until smoke execution evidence exists.
