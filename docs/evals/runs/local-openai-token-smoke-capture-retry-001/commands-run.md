# Commands run

| # | Command | Exit code | Purpose |
|---:|---|---:|---|
| 1 | `pwd && find .. -name AGENTS.md -print && git status --short --branch && git remote -v` | 0 | Confirm workspace, instructions, and local Git state. |
| 2 | `cat AGENTS.md && git remote -v && git status --short --branch` | 0 | Inspect repo-level instructions and local branch status. |
| 3 | `git branch --show-current; git log --oneline -5` | 0 | Inspect current branch and recent prerequisite commits. |
| 4 | `for n in 502 503 504 505 506 507 508; do curl -fsSL https://api.github.com/repos/adonisdv23/Alpha-Solver/pulls/$n | python -c 'import sys,json; d=json.load(sys.stdin); print("state",d.get("state")); print("merged_at",d.get("merged_at")); print("title",d.get("title")); print("merge_commit_sha",d.get("merge_commit_sha"))'; done` | 0 | Verify live GitHub PR state for PRs #502-#508 without secrets. |
| 5 | `paths=(docs/evals/runs/alpha-solver-openai-free-token-eval-smoke-harness-plan-001 docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001 docs/evals/runs/openai-data-sharing-operator-verification-001 docs/evals/runs/local-openai-token-smoke-capture-001 docs/evals/runs/openai-synthetic-smoke-prompt-fixture-001 docs/evals/runs/openai-data-sharing-operator-attestation-001 docs/evals/runs/openai-packet-checker-scope-001); for p in "${paths[@]}"; do [ -d "$p" ] && echo "OK $p" || echo "MISSING $p"; done` | 0 | Verify required packet directories exist locally. |
| 6 | `rg -n "SMOKE-001|GO|NO-GO|second|billing|cost|OPENAI|api key|data-sharing|redaction" <prerequisite_packets>` | 0 | Inspect fixture, attestation, checker, and blocked-lane context. |
| 7 | `python - <<'PY' ... os.environ.get(...) ... PY` | 0 | Check presence/absence of relevant OpenAI environment variables without printing values. |

No command printed an API key, credential, secret, private billing detail, raw provider log, or private operator note.
