# Checks Run

This file records checks for the docs-only Level 5 quality evaluation design packet.

## Required checks

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-5-quality-evaluation-design`
- `rg "ALPHA-SOLVER-POST-LEVEL-3-LEVEL-5-QUALITY-EVALUATION-DESIGN-PACKET-001|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-6-PRODUCT-SURFACE-DESIGN-PACKET-001|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-5-QUALITY-EVALUATION-DESIGN-FIX-001|benchmark|quality evidence|local model quality|Alpha superiority|MVP readiness|production readiness" docs/evals/runs/alpha-solver-post-level-3-level-5-quality-evaluation-design`

## Boundary of checks

These checks are documentation and static checker commands only. They do not run local model inference, start Ollama, rerun validation, rerun smoke, call hosted providers, expose `/v1/solve`, expose dashboard routes, add provider fallback, add hosted fallback, run benchmarks, score outputs, perform billing work, update Google Sheets or backlog workbooks, or promote evidence.
