# Commands run

| # | Command | Exit code | Purpose |
|---|---|---:|---|
| 1 | `pwd && find .. -name AGENTS.md -print` | 0 | Confirm repository path and instruction files. |
| 2 | `git status --short --branch` | 0 | Confirm current branch/worktree state before edits. |
| 3 | `cat AGENTS.md && gh pr view ...` | 127 | Read repo instructions; `gh` was unavailable, so live verification used GitHub API next. |
| 4 | `python - <<'PY' ... urllib.request.urlopen('https://api.github.com/repos/adonisdv23/Alpha-Solver/pulls/{n}') ... PY` | 0 | Read-only GitHub verification for PR #497, #499, and #500. |
| 5 | `find docs/evals/runs -maxdepth 1 -type d | sort | tail -30 && rg -n "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-EXECUTION-EVIDENCE-004|selected next lane|candidate" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003 -S` | 0 | Verify prior packet existence and selected next lane. |
| 6 | `rg -n "approval_record|expected_safety_block|run_local_dry_run_wrapper|approval" alpha scripts tests docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-003 -S` | 0 | Locate relevant local code and schemas. |
| 7 | `sed -n '1,220p' alpha/self_operator/dry_run.py; sed -n '1,380p' alpha/self_operator/execution_gate.py; sed -n '90,150p' alpha/self_operator/approval.py; sed -n ... candidate-task.json` | 0 | Inspect wrapper, gate, approval validation, and prior candidate. |
| 8 | `sed -n '90,280p' alpha/self_operator/acceptance_interpretation.py; sed -n '740,850p' alpha/self_operator/acceptance_interpretation.py; sed -n '1,160p' scripts/interpret_self_operator_acceptance.py` | 0 | Inspect interpretation schema and CLI. |
| 9 | `rg -n "def validate_operator_decision|validation_errors|operator_decision" alpha/self_operator/acceptance_interpretation.py | head -40 && sed -n '280,380p' alpha/self_operator/acceptance_interpretation.py` | 0 | Inspect exact operator-review schema validation. |
| 10 | `mkdir -p .../execution-evidence-004/artifacts; python - <<'PY' ... write operator approval, candidate, review; run_local_dry_run_wrapper(...) ... PY` | 0 | Preserve artifacts and run local gate/wrapper. |
| 11 | `python scripts/import_self_operator_acceptance_results.py --packet-dir ... --output-dir ... --output-name result-import-summary.json; echo import_exit=$?; python scripts/interpret_self_operator_acceptance.py --import-summary ... --operator-decision ... --output ...; echo interpret_exit=$?` | 0 | Exercise result import and acceptance interpretation. |
| 12 | `python - <<'PY' ... sha256 packet files and inspect gate/interpretation outputs ... PY` | 0 | Inventory generated artifacts. |
| 13 | `cat > /tmp/write_docs.py <<'PY' ... PY; python /tmp/write_docs.py` | 0 | Write documentation packet files. |
| 14 | `python scripts/check_local_llm_doc_paths.py; echo doc_paths_exit=$?; python scripts/check_local_llm_evidence_boundaries.py; echo boundaries_exit=$?; python scripts/check_local_llm_packet_consistency.py; echo consistency_exit=$?; git status --short` | 0 | Run required offline validation checks and inspect worktree. |
