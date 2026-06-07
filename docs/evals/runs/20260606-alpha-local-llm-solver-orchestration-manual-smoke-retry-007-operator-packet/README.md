# Manual Smoke Retry 007 Operator Packet

Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-MANUAL-SMOKE-RETRY-007-OPERATOR-PACKET-001`

Selected retry lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-MANUAL-SMOKE-RETRY-007`

This docs-only packet prepares the exact operator-facing command and inspection checklist for manual smoke retry 007 after the diagnostic-router reset.

## Prerequisites

- PR #356 is squashed, merged, closed, and recorded in GS.
- PR #356 selected `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-MANUAL-SMOKE-RETRY-007`.
- Adonis is back at the local Mac with Ollama reachable at the loopback endpoint below.

## Local operator assumptions

- Repo path: `/Users/games/Documents/Alpha-Solver`
- Endpoint: `http://127.0.0.1:11434/api/chat`
- Model: `qwen2.5:3b`
- Timeout: `60`
- Retry 007 source artifact path: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset/`

## Packet contents

1. [exact-mac-command.md](exact-mac-command.md)
2. [expected-outcomes.md](expected-outcomes.md)
3. [diagnostic-inspection-checklist.md](diagnostic-inspection-checklist.md)
4. [source-artifact-preservation-plan.md](source-artifact-preservation-plan.md)
5. [evidence-boundary.md](evidence-boundary.md)
6. [blocked-work.md](blocked-work.md)
7. [selected-next-lane.md](selected-next-lane.md)

## Scope

This packet is preparation only. It does not run the smoke, call a local model, call hosted providers, create retry 007 source artifacts, import results, interpret retry 007, update Google Sheets, change runtime behavior, change tests, or make readiness or validation claims.
