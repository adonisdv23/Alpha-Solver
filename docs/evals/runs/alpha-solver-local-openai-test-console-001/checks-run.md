# Checks run

| Check | Result | Notes |
|-------|--------|-------|
| `python -m pytest -q tests/test_operator_test_console.py` | Pass | Focused console tests passed with deprecation warnings from FastAPI/Starlette. |
| `python -m pytest -q tests/test_operator_smoke_runner.py` | Pass | Existing smoke-runner tests passed. |
| `python -m pytest -q` | Pass | Full suite passed with 3 skips and deprecation warnings. |
| `make check-local-llm-orchestration-guardrails` | Pass | Evidence-boundary, doc-path/link, and packet-consistency checks passed. |
| `git diff --check` | Pass | No whitespace errors reported. |
| `python scripts/check_narrative_claim_safety.py <changed markdown files>` | Pass | Narrative claim-safety lint passed for changed Markdown files. |
| Source-of-truth consistency check for `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_001` | Pass | Confirmed in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, `docs/EVIDENCE_INDEX.md`, and packet `selected-next-state.md`. |
| Secret-safety pattern check over changed files | Pass | Confirmed no checked API key value, forbidden auth-header names, forbidden bearer-token markers, unsanitized provider payload phrase, hosted account detail phrase, or local machine identifier pattern appears in changed files. |
