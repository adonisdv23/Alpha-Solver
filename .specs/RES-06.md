# CODE SPEC — RES-06 · Scenario Pack & Showcase (record/replay + rubric) (RES)

> Reconstructed by lane `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` from committed code and tests only. This file replaces a non-authoritative contaminated MCP-005 body. Do not infer implementation quality from this reconstruction.

## Goal

Load scenario packs, execute steps through adapters, judge with rubric, summarize pass rates, and replay recorded events.

## Acceptance Criteria

- Pack contains at least 30 scenarios.
- Single scenario runs pass expected steps with adapter values.
- Rubric supports equals, contains, regex, type, and approximate expectations.
- Record/replay preserves verdicts for 10 events.
- Summaries include total, passed, pass_rate, and route_explain fields.

## Design

- Source of truth for this reconstruction is limited to the committed implementation and test targets listed in `## Reconstruction Sources`.
- Runtime behavior is represented by the implementation files in `## Code Targets`; expected observable behavior is represented by the listed tests.
- No provider calls, tokens, external services, or runtime code changes are required by this spec reconstruction.
- MCP-005 remains the canonical source for MCP error taxonomy names and semantics wherever error classes are referenced.
- Unspecified behavior is not reconstructed; it remains unknown or requires an operator decision.

## Tests

Run the focused tests listed in `## Code Targets` for this spec. These tests define the reconstructed acceptance boundary and should be kept focused on the committed behavior summarized above.

## Reconstruction Note

This spec was reconstructed on 2026-06-14 by reading the contaminated spec's `## Code Targets` section and the committed source/test files named there. The prior MCP-005 Error Taxonomy body was treated as non-authoritative contamination and was not used to infer this feature's intent. Unknown: showcase UI or demo script outside pack/runner is not defined.

## Reconstruction Sources

- `service/scenarios/runner.py`
- `service/scenarios/rubric.py`
- `scenarios/pack.yaml`
- `tests/test_scenarios.py`

## Code Targets

service/scenarios/runner.py; service/scenarios/rubric.py; scenarios/pack.yaml; tests/test_scenarios.py
