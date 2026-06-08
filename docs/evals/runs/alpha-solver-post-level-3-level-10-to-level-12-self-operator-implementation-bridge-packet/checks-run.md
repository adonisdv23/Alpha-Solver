# Checks run

| Check | Result | Notes |
| --- | --- | --- |
| `git status --short` | Passed | Reported only the new bridge packet directory as untracked before staging: `?? docs/evals/runs/alpha-solver-post-level-3-level-10-to-level-12-self-operator-implementation-bridge-packet/`. |
| `git diff --name-only` | Passed | No tracked-file diff was present before staging because this docs-only packet was a new untracked directory. |
| `git diff --check` | Passed | No whitespace errors reported. |
| `make check-local-llm-orchestration-guardrails` | Passed | Evidence-boundary, doc path/link, and packet consistency guardrails passed. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-10-to-level-12-self-operator-implementation-bridge-packet` | Passed | New packet consistency passed for one packet directory. |
| `rg -n "stop if explicit operator confirmation is missing|provider calls|source-artifact mutation|evidence promotion|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-ARTIFACT-SCHEMA-CODE-SCAFFOLD-001" docs/evals/runs/alpha-solver-post-level-3-level-10-to-level-12-self-operator-implementation-bridge-packet` | Passed | Focused text check found required stop condition, forbidden surfaces, and selected next lane token. |
