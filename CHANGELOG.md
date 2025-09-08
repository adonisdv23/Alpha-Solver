# Changelog

## [Unreleased]
### Fixed
- Remove duplicate entrypoint module; normalize imports to a single `_tree_of_thought` API.

### Docs
- Clarified `score_threshold` vs `low_conf_threshold` and documented SAFE-OUT output schema.

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
