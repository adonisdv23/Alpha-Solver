# Changelog

## [Unreleased]
### Added
- Multi-branch Tree-of-Thought with deterministic beam expansion and logging.
- Progressive Complexity Router with deterministic escalation and observability.
- Agents v12 scaffold and configuration flags.
- Deterministic benchmark suite comparing CoT, single-path ToT, multi-branch ToT and routed ToT.
- JSONL events for `tot_layer`, `tot_candidate`, and `router_escalate`.
- Deterministic agents v12 behaviors (decomposer/checker/calculator).
- SAFE-OUT v1.2 with reasons, evidence and recovery notes.
- Config defaults and loader with env/CLI layering.
- Telemetry schema v1 with validation helper and tiny web viz.
- Pluggable path scorers with registry and composite weights.
- Persistent JSON cache for Tree-of-Thought.
- Lightweight accounting of expansions and simulated tokens.

### Changed
- `_tree_of_thought` entrypoint now surfaces router and agent diagnostics and exposes new flags.
- AlphaSolver v2.2.6 P3 moved to `alpha.solver.observability` and is wrapped by the single `alpha-solver-v91-python` entrypoint.
- Diagnostics now include scorer details, config snapshot and accounting summary.

### Documentation
- Synced the Operator & Technology Manual baseline refresh from PR #182 and the final post-placeholder-cleanup refresh from PR #187.
- Recorded PR #183's initial `LIVE-SMOKE-OPENAI-001` contract and PR #185's alignment of that spec with the implemented skipped-by-default live smoke.
- Captured PR #186's health/readiness and rate-limit placeholder truth cleanup, keeping `NEW-HEALTH-001` and `NEW-RATE-001` as future/placeholder targets rather than implemented richer dependency checks or Redis-backed rate limiting.

### Tests
- Recorded PR #184's skipped-by-default live OpenAI smoke test for FastAPI `/v1/solve` and the registered `live` / `openai` pytest markers; default pytest/CI remains credential-free and network-free, operator verification may still be pending, and any gated pass proves only that credentialed environment at that time.

## [2025-09-09]
### Added
- SAFE-OUT v1.1 state machine with structured recovery and phased JSONL logging.
### Changed
- `_tree_of_thought` entrypoint returns phases and enriched notes while preserving existing keys.

## [2025-09-07]
### Added
- SAFE-OUT policy (low-confidence fallback) with JSON `safe_out_decision` logging.
- Public `_tree_of_thought(...)` returns routed policy output.

### Changed
- ToT v1 deterministic pipeline (branching, scoring, selection, pruning).

## [1.0.0b1]
- Initial packaging metadata and console entry point.
- Added release workflow attaching build artifacts to GitHub Releases.
