# Checks Run

Required checks for this packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-8-self-operator-operator-ux-acceptance`
- Confirm changed files are only under `docs/evals/runs/alpha-solver-post-level-3-level-8-self-operator-operator-ux-acceptance/`.

This file records the expected check set; the final PR response records the observed results from the working tree.
