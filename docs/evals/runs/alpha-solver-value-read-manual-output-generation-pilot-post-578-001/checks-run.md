# Checks Run

| Command | Result | Notes |
| --- | --- | --- |
| `python - <<'PY' ... GitHub API verification for PR #578 and open PRs ... PY` | Passed | PR #578 was closed and merged at `2026-06-15T22:17:01Z`; open PR list was empty. |
| `git diff --check` | Passed | No whitespace errors. |
| `python scripts/check_narrative_claim_safety.py $(cat /tmp/changed_md.txt)` | Passed | Scanned every changed Markdown file; the raw quoted rewrite prompt uses an inline suppression rationale for the intentionally forbidden source wording. |
| `python scripts/check_local_llm_evidence_boundaries.py $(cat /tmp/changed_md.txt)` | Passed | No relevant local-LLM evidence-boundary files were scanned for these changed paths. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-value-read-manual-output-generation-pilot-post-578-001` | Passed | One packet directory scanned. |
| `python -m pytest -q` | Passed | Full test suite passed; three tests were skipped by existing environment gates. |
