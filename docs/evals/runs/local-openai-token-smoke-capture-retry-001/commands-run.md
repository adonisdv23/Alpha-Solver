# Commands run

| # | Command | Exit code | Purpose |
|---:|---|---:|---|
| 1 | `pwd && find .. -name AGENTS.md -print && git status --short --branch && git remote -v` | 0 | Confirm workspace, instructions, and local Git state. |
| 2 | `cat AGENTS.md && git remote -v && git status --short --branch` | 0 | Inspect repo-level instructions and local branch status. |
| 3 | `git branch --show-current; git log --oneline -5` | 0 | Inspect current branch and recent prerequisite commits. |
| 4 | `curl -fsSL https://api.github.com/repos/adonisdv23/Alpha-Solver/pulls/<PR_NUMBER>` | 0 | Verify live GitHub PR state for PRs #502-#508 without secrets. |
| 5 | `for p in <required_packet_dirs>; do [ -d "$p" ] && echo "OK $p" || echo "MISSING $p"; done` | 0 | Verify required packet directories exist locally. |
| 6 | `rg -n "SMOKE-001|GO|NO-GO|second|billing|cost|OPENAI|api key|data-sharing|redaction" <prerequisite_packets>` | 0 | Inspect fixture, attestation, checker, and blocked-lane context. |
| 7 | `python - <<'PY' ... os.environ.get(...) ... PY` | 0 | Check presence/absence of relevant OpenAI environment variables without printing values. |

No command printed an API key, credential, secret, private billing detail, raw provider log, or private operator note.
