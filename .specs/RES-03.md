# CODE SPEC — RES-03 · Decision Rules & Scoring (RES)

> Reconstructed by lane `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` from committed code and tests only. This file replaces a non-authoritative contaminated MCP-005 body. Do not infer implementation quality from this reconstruction.

## Goal

Load/validate scoring weights, score/rank candidate plans deterministically, and explain score components.

## Acceptance Criteria

- Weights load and invalid shapes raise errors.
- Scoring is deterministic.
- Ranking chooses expected top plan in sample fixtures.
- Ties break deterministically by confidence, latency_ms, cost_tokens, then id.
- Explain includes score, configured components, and tiebreak chain.

## Design

- Source of truth for this reconstruction is limited to the committed implementation and test targets listed in `## Reconstruction Sources`.
- Runtime behavior is represented by the implementation files in `## Code Targets`; expected observable behavior is represented by the listed tests.
- No provider calls, tokens, external services, or runtime code changes are required by this spec reconstruction.
- MCP-005 remains the canonical source for MCP error taxonomy names and semantics wherever error classes are referenced.
- Unspecified behavior is not reconstructed; it remains unknown or requires an operator decision.

## Tests

Run the focused tests listed in `## Code Targets` for this spec. These tests define the reconstructed acceptance boundary and should be kept focused on the committed behavior summarized above.

## Reconstruction Note

This spec was reconstructed on 2026-06-14 by reading the contaminated spec's `## Code Targets` section and the committed source/test files named there. The prior MCP-005 Error Taxonomy body was treated as non-authoritative contamination and was not used to infer this feature's intent. Unknown: business-approved weight values beyond config fixture are not inferred.

## Reconstruction Sources

- `service/scoring/decision_rules.py`
- `config/decision_rules.yaml`
- `tests/test_decision_rules.py`

## Code Targets

service/scoring/decision_rules.py; config/decision_rules.yaml; tests/test_decision_rules.py
