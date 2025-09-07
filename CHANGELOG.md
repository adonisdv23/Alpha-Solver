# Changelog

## [Unreleased]
### Fixed
- Remove duplicate entrypoint module; normalize imports to a single `_tree_of_thought` API.

### Docs
- Clarified `score_threshold` vs `low_conf_threshold` and documented SAFE-OUT output schema.

## [2025-09-07]
### Added
- SAFE-OUT policy (low-confidence fallback) with JSON `safe_out_decision` logging.
- Public `_tree_of_thought(...)` returns routed policy output.

### Changed
- ToT v1 deterministic pipeline (branching, scoring, selection, pruning).

## [1.0.0b1]
- Initial packaging metadata and console entry point.
- Added release workflow attaching build artifacts to GitHub Releases.
