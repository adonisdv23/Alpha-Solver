# Checks Run

## Results

| Check | Result | Notes |
|-------|--------|-------|
| `make check-local-llm-orchestration-guardrails` | Pass | Reproduced the failed CI guardrail suite after adding `selected-next-action.md`; evidence-boundary, doc-path/link, and packet-consistency checks passed. |
| `python -m pytest -q` | Pass | Reproduced the failed full test suite; all tests passed with 3 skips and deprecation warnings. |
| `git diff --check` | Pass | No whitespace errors. |
| `python scripts/check_narrative_claim_safety.py $( (git diff --name-only -- '*.md'; git ls-files --others --exclude-standard -- '*.md') \\| sort -u )` | Pass | Narrative claim-safety linter scanned changed Markdown files. This is not a completeness claim. |
| `python - <<'PY' ... PY` source-of-truth consistency check | Pass | Confirmed `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RESULTS_IMPORT_001` appears in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, `docs/EVIDENCE_INDEX.md`, and this packet selected-next-state file. |
| `python - <<'PY' ... PY` secret-safety check on changed files | Pass | Confirmed no concrete API key value, authorization header, bearer token value, raw provider request JSON body, provider-console URL or artifact, or local machine identifier appears in changed files. |
