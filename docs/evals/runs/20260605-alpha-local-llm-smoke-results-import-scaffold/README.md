# Local LLM Smoke Results Import Scaffold

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-SCAFFOLD-001`

Status: docs-only scaffold for a future sanitized local LLM smoke results import.

## Purpose

This directory defines the documents, field requirements, redaction rules, result classifications, reviewer checks, and preservation checks that a future import lane must use after a separately produced smoke execution evidence file exists.

This is a scaffold only. No smoke evidence is imported in this PR, no result row is created, and no smoke outcome is inferred.

## Source files reviewed

- `docs/evals/runs/20260605-alpha-local-llm-endpoint-locality-hardening/`
- `docs/evals/runs/20260605-alpha-local-llm-endpoint-locality-review-gate/`
- `docs/evals/runs/20260605-alpha-local-llm-smoke-authorization-refresh/`
- `docs/evals/runs/20260605-alpha-local-llm-smoke-test-packet/`
- `alpha/local_llm/provider_adapter.py`
- `tests/test_local_llm_provider_adapter.py`

## Scaffold contents

- `required-source-evidence.md` records the mandatory future evidence file and import-stop rule.
- `sanitized-import-template.md` provides a placeholder-only sanitized import structure.
- `smoke-result-log-template.md` provides a header-only log template with no result rows.
- `redaction-log-template.md` defines redaction checks for future imports.
- `import-reviewer-checklist.md` defines reviewer checks before any import is accepted.
- `evidence-boundary.md` preserves the narrow evidence boundary and non-claims.
- `scaffold-preservation-checklist.md` checks that this lane remains scaffold-only.
- `recommended-next-lane.md` selects exactly one recommended next lane.

## Required future source evidence

A future import must be blocked unless `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` exists and is available to the importer.

If `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` is missing, the import must stop.

## Required future evidence fields

A future source evidence file must include:

- lane ID
- prerequisite PR link
- exact command executed
- endpoint pattern
- exact model name, if approved for repo disclosure
- timeout seconds
- start timestamp
- end timestamp
- stdout
- stderr
- exit code
- raw artifact preservation notes
- executed / skipped / blocked status
- redaction notes
- evidence boundary
- non-claims

## Result classifications

Allowed classifications are: `not run`, `skipped`, `blocked`, `pass`, `fail`, `error`, `timeout`, `connection failure`, `endpoint locality rejection`, `malformed response`, `empty output`, `prompt echo`, and `system echo`.

## Evidence boundary

This lane is import-scaffold documentation only. It is not smoke execution evidence, local LLM behavior evidence, Ollama behavior evidence, hosted provider evidence, `/v1/solve` readiness evidence, dashboard preview readiness evidence, runtime readiness evidence, MVP validation, production readiness, Alpha quality evidence, Alpha superiority evidence, broad plain-provider inferiority evidence, Batch C readiness, benchmark success, exact billing evidence, or provider orchestration evidence.
