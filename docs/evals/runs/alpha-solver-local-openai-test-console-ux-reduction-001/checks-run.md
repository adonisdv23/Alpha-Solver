# Checks run

| Command | Result | Notes |
|---------|--------|-------|
| `python -m pytest -q tests/test_operator_test_console.py` | Pass | Focused console UX and redaction tests passed. |
| `python -m pytest -q tests/test_operator_smoke_runner.py` | Pass | Existing smoke runner tests passed without running providers. |
| `python -m pytest -q` | Pass | Full suite passed with existing skips for live OpenAI, web adapter, and packaging build environment. |
| `make check-local-llm-orchestration-guardrails` | Pass | Local LLM evidence-boundary, doc-path, and packet-consistency guardrails passed. |
| `git diff --check` | Pass | No whitespace errors. |
| `python scripts/check_narrative_claim_safety.py <changed markdown files>` | Pass | Narrative claim-safety linter scanned changed Markdown files. This is not a completeness claim. |
| source-of-truth consistency check for `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_TEST_CONSOLE_UX_REDUCTION_001` | Pass | Checked `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, `docs/EVIDENCE_INDEX.md`, and packet `selected-next-state.md`. |
| changed-line secret-safety check | Pass | Checked added lines for API key marker values, authorization header literal, bearer header literal, raw provider request body wording, and provider dashboard detail wording. |
| focused UX/redaction assertions | Pass | Confirmed numeric usage token counters remain visible, secret-like fields remain redacted, and OpenAI/local form state remains selected after submit rendering. |
