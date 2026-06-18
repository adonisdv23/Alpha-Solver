# Checks run

## Automated checks

- `git diff --check` — passed with no whitespace errors.
- `python -m py_compile tools/operator_test_console.py tests/test_operator_test_console.py` — passed.
- `pytest -q tests/test_operator_test_console.py` — passed: 46 passed; warnings were deprecation warnings from FastAPI/Starlette test dependencies.
- `pytest -q tests/test_model_router.py tests/test_tool_router.py` — passed: 36 passed.
- `python scripts/check_narrative_claim_safety.py docs/CURRENT_STATE.md docs/LANE_REGISTRY.md docs/EVIDENCE_INDEX.md docs/evals/runs/alpha-solver-test-console-routing-metadata-display-001/*.md` — passed: 15 files scanned; this is not a completeness claim.
- `python -m pytest -q` — passed: full repository test suite passed with 3 skipped tests and dependency/runtime deprecation warnings; skipped tests were live OpenAI smoke, web-adapter-disabled deck smoke, and packaging build environment coverage.

## Required lane checks

- Targeted console route-preview display tests passed via `pytest -q tests/test_operator_test_console.py`.
- Targeted model route-preview tests passed via `pytest -q tests/test_model_router.py tests/test_tool_router.py`.
- Targeted tool route-preview tests passed via `pytest -q tests/test_model_router.py tests/test_tool_router.py`.
- Narrative claim-safety check on changed Markdown files passed via the command above.
- No provider/local-model/network/tool/web/runtime-GitHub calls in tests: reviewed changed route-preview tests; preview tests monkeypatch smoke paths to fail if called and assert preview authorization flags remain false.
- Source-of-truth consistency check for `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_METADATA_DISPLAY_001`: `rg -n "OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_METADATA_DISPLAY_001|ALPHA-SOLVER-TEST-CONSOLE-ROUTING-METADATA-DISPLAY-001" docs/CURRENT_STATE.md docs/LANE_REGISTRY.md docs/EVIDENCE_INDEX.md docs/evals/runs/alpha-solver-test-console-routing-metadata-display-001` found the lane and selected next state in the source-of-truth docs and packet.
- Changed-line secret-safety check: `git diff --unified=0 | python -c 'import sys,re; data="\n".join(l for l in sys.stdin if l.startswith("+") and not l.startswith("+++")); pats=["OPENAI_API_KEY=","api_key=","sk-","Bearer ","password=","secret="]; hits=[p for p in pats if p.lower() in data.lower()]; print("secret_hits=", hits); raise SystemExit(1 if hits else 0)'` printed `secret_hits= []`.
- Required-file packet completeness check: local Python check confirmed no missing files among `README.md`, `implementation-summary.md`, `operator-ui-contract.md`, `route-preview-display-contract.md`, `tool-preview-display-contract.md`, `operator-facing-boundary.md`, `defects-and-caveats.md`, `non-actions.md`, `non-claims.md`, `checks-run.md`, `selected-next-state.md`, and `selected-next-action.md`.
