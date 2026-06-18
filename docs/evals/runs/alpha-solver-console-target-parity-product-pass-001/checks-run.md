# Checks run

| Check | Result | Notes |
| --- | --- | --- |
| `git diff --check` | Pass | No whitespace errors. |
| `python -m py_compile tools/operator_test_console.py tests/test_operator_test_console.py` | Pass | Changed Python files compile. |
| `pytest -q tests/test_operator_test_console.py` | Pass | 50 passed; warnings were FastAPI/Starlette deprecation warnings from test dependencies. |
| `python - <<'PY' ... required packet file completeness check ... PY` | Pass | All required packet files are present. |
| `python - <<'PY' ... source-of-truth selected-next-state consistency check ... PY` | Pass | `OPERATOR_REVIEW_DEFERRED_PENDING_HTML_DIAGRAM_TARGET_PARITY_001` appears in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md`. |
| `git diff -U0 -- '*.md' | rg -n "^\\+.*(is ready|proves|readiness proof|quality proof|is superior|benchmark success|production ready|public ready)"` | Pass | No changed Markdown line makes the blocked narrative claims checked by this scan. |
| `git diff -U0 | rg -n "^\\+.*((?i)sk-[a-z0-9]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})"` | Pass | No high-confidence secret patterns found on changed lines. |
| `git diff -U0 tests tools | rg -n "^\\+.*(requests\\.|urllib|urlopen|/v1/solve|subprocess|os.system)"` | Pass | No added test/tool lines introduce provider, local-model, network, tool, web, runtime GitHub, file mutation, or `/v1/solve` calls. Existing monkeypatch references remain non-executing assertions. |
