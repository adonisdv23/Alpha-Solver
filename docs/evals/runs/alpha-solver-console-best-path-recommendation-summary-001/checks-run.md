# Checks run

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` | Pass | No whitespace errors. |
| `pytest -q tests/test_operator_test_console.py -k 'best_path or route_preview or target_parity or evidence_card'` | Pass | 14 passed; warnings were Python/FastAPI/Starlette deprecation warnings. Covers targeted console UI/rendering, best-path summary, route-preview, fail-closed, metadata-only, and no-execution preview checks. |
| `pytest -q tests/test_operator_test_console.py` | Pass | 58 passed; warnings were Python/FastAPI/Starlette deprecation warnings. |
| `python -m py_compile tools/operator_test_console.py tests/test_operator_test_console.py` | Pass | Changed Python files compile. |
| `python -m pytest -q` | Pass | Full suite passed with 3 skipped tests and deprecation warnings. Skips: live OpenAI smoke requires opt-in/API key; deck smoke disabled in test environment; packaging build module missing/build failed. |
| `python - <<'PY' ... narrative claim-safety check ... PY` | Pass | Changed Markdown records non-actions/non-claims and does not add readiness/value/quality/superiority assertions. |
| `python - <<'PY' ... no provider/local-model/network/tool/web/runtime-GitHub calls in preview tests ... PY` | Pass | Preview tests keep execution paths monkeypatched/fail-if-called and do not authorize preview execution. |
| `python - <<'PY' ... source-of-truth consistency check ... PY` | Pass | `ALPHA-SOLVER-CONSOLE-BEST-PATH-RECOMMENDATION-SUMMARY-001` and `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001` are present in source-of-truth docs. |
| `python - <<'PY' ... changed-line secret-safety check ... PY` | Pass | Added lines do not contain detected API-key, password, or token-like secret values. |
| `python - <<'PY' ... required-file packet completeness check ... PY` | Pass | Required evidence packet files are present. |

Initial targeted console test run failed while implementation returned no preview object; the return path was fixed before the final passing checks above.
