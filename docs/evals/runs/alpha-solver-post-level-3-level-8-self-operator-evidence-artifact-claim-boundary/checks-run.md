# Checks Run

The following checks are required for this docs-only packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-8-self-operator-evidence-artifact-claim-boundary`
- Confirm changed files are only under `docs/evals/runs/alpha-solver-post-level-3-level-8-self-operator-evidence-artifact-claim-boundary/`.

Results are recorded in the PR summary rather than as generated logs in this packet.
