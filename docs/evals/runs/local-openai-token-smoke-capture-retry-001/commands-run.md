# Commands run

## Command 1

Exit code: `0`

Purpose: Confirm workspace, instructions, and local Git state.

```bash
pwd && find .. -name AGENTS.md -print && git status --short --branch && git remote -v
```

## Command 2

Exit code: `0`

Purpose: Inspect repo-level instructions and local branch status.

```bash
cat AGENTS.md && git remote -v && git status --short --branch
```

## Command 3

Exit code: `0`

Purpose: Inspect current branch and recent prerequisite commits.

```bash
git branch --show-current; git log --oneline -5
```

## Command 4

Exit code: `0`

Purpose: Verify live GitHub PR state for the literal PR range #502 through #508 without secrets.

```bash
for n in 502 503 504 505 506 507 508; do echo "--- PR #$n"; curl -fsSL https://api.github.com/repos/adonisdv23/Alpha-Solver/pulls/$n | python -c 'import sys,json; d=json.load(sys.stdin); print("state",d.get("state")); print("merged_at",d.get("merged_at")); print("title",d.get("title")); print("merge_commit_sha",d.get("merge_commit_sha"))'; done
```

## Command 5

Exit code: `0`

Purpose: Verify the literal required packet directory list exists locally.

```bash
paths=(docs/evals/runs/alpha-solver-openai-free-token-eval-smoke-harness-plan-001 docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001 docs/evals/runs/openai-data-sharing-operator-verification-001 docs/evals/runs/local-openai-token-smoke-capture-001 docs/evals/runs/openai-synthetic-smoke-prompt-fixture-001 docs/evals/runs/openai-data-sharing-operator-attestation-001 docs/evals/runs/openai-packet-checker-scope-001); for p in "${paths[@]}"; do [ -d "$p" ] && echo "OK $p" || echo "MISSING $p"; done
```

## Command 6

Exit code: `0`

Purpose: Inspect fixture, attestation, checker, and blocked-lane context.

```bash
rg -n "SMOKE-001|GO|NO-GO|second|billing|cost|OPENAI|api key|data-sharing|redaction" docs/evals/runs/alpha-solver-openai-free-token-eval-smoke-harness-plan-001 docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-def-002-def-003-evidence-boundary-001 docs/evals/runs/openai-data-sharing-operator-verification-001 docs/evals/runs/local-openai-token-smoke-capture-001 docs/evals/runs/openai-synthetic-smoke-prompt-fixture-001 docs/evals/runs/openai-data-sharing-operator-attestation-001 docs/evals/runs/openai-packet-checker-scope-001
```

## Command 7

Exit code: `0`

Purpose: Check presence/absence of relevant OpenAI environment variables without printing values.

```bash
python - <<'PY'
import os
names=['OPENAI_API_KEY','OPENAI_PROJECT','OPENAI_ORG_ID']
for n in names:
 print(f'{n}={"present" if os.environ.get(n) else "absent"}')
PY
```

## Command 8

Exit code: `0`

Purpose: Run the local LLM/OpenAI doc path and link check.

```bash
python scripts/check_local_llm_doc_paths.py
```

## Command 9

Exit code: `0`

Purpose: Run the local LLM evidence-boundary static check.

```bash
python scripts/check_local_llm_evidence_boundaries.py
```

## Command 10

Exit code: `0`

Purpose: Run the local LLM packet consistency check.

```bash
python scripts/check_local_llm_packet_consistency.py
```

No command printed an API key, credential, secret, private billing detail, raw provider log, or private operator note.
