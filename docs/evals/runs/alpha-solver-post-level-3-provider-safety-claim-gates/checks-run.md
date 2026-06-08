# Checks Run

Lane:
`ALPHA-SOLVER-POST-LEVEL-3-PROVIDER-SAFETY-CLAIM-GATES-PACKET-001`

Required checks for this packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-provider-safety-claim-gates`
- `rg "NO_FURTHER_PROVIDER_SAFETY_CLAIM_GATES_LANES_SELECTED|ALPHA-SOLVER-POST-LEVEL-3-PROVIDER-SAFETY-CLAIM-GATES-FIX-001|provider claims|fallback readiness|hosted readiness|provider readiness|blocked claims|does not authorize|does not call providers|Level 7 controls" docs/evals/runs/alpha-solver-post-level-3-provider-safety-claim-gates`

These checks do not call providers, run models, run benchmarks, expose `/v1/solve`, expose dashboards, configure credentials, add fallback, perform billing work, or promote evidence.
