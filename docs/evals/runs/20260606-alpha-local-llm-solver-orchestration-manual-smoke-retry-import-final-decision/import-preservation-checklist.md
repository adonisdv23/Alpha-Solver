# Import Preservation Checklist

## Scope controls

- [x] Docs-only changes under `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-import-final-decision/`.
- [x] Source code changes absent.
- [x] Test code changes absent.
- [x] Runtime changes absent.
- [x] Provider changes absent.
- [x] Dashboard changes absent.
- [x] `/v1/solve` changes absent.
- [x] Backlog workbook changes absent.
- [x] Google Sheets update absent.

## Execution controls

- [x] Local model call by this import lane absent.
- [x] Hosted provider call by this import lane absent.
- [x] Smoke rerun absent.
- [x] Output reconstruction absent.
- [x] Artifact interpretation used only repo-preserved artifacts.

## Decision controls

- [x] Exactly one final decision is recorded: `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_FAIL_REQUIRES_FIX`.
- [x] Exactly one selected next lane is recorded: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CLARIFY-ASSUMPTION-HIGH-RISK-NONEXPOSURE-FIX-001`.
- [x] Evidence-boundary language remains narrow.
- [x] Exit status `0` is not treated as proof that expected smoke behavior passed.
