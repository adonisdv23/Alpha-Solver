# Checks run

- `python -m pytest -q tests/test_model_catalog.py tests/test_model_router.py` passed, 16 tests.
- `python -m pytest -q tests/test_operator_smoke_runner.py` passed, 9 tests.
- `python -m pytest -q` passed with expected skips and deprecation warnings.
- `make check-local-llm-orchestration-guardrails` passed.
- `git diff --check` passed.
- `python scripts/check_narrative_claim_safety.py $(git diff --name-only -- '*.md')` passed for changed Markdown files.
- Source-of-truth consistency check passed for `OPERATOR_REVIEW_REQUIRED_AFTER_MODEL_CATALOG_ROUTING_PREVIEW_001` in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, `docs/EVIDENCE_INDEX.md`, and `selected-next-state.md`.
- Secret-safety check passed on added lines for forbidden secret and runtime-transcript markers.
