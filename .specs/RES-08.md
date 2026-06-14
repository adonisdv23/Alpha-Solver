# CODE SPEC — RES-08 · Budget Simulator + Evidence Pack (RES)

> Reconstructed by lane `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` from committed code and tests only. This file replaces a non-authoritative contaminated MCP-005 body. Do not infer implementation quality from this reconstruction.

## Goal

Simulate token costs and package sanitized evidence artifacts with hashes, metrics, and zipped files.

## Acceptance Criteria

- Cost simulation computes per-item tokens/cost/latency and totals from configured provider/model pricing.
- Budget simulator parity/caps/what-if CLI behavior follows tests.
- Evidence pack writes manifest, metrics, simulation JSONL, and evidence.zip.
- Manifest contains counts and SHA-256 hashes; JSONL rows are sorted and sanitized.
- Simulation is deterministic and performance meets tested bounds.

## Design

- Source of truth for this reconstruction is limited to the committed implementation and test targets listed in `## Reconstruction Sources`.
- Runtime behavior is represented by the implementation files in `## Code Targets`; expected observable behavior is represented by the listed tests.
- No provider calls, tokens, external services, or runtime code changes are required by this spec reconstruction.
- MCP-005 remains the canonical source for MCP error taxonomy names and semantics wherever error classes are referenced.
- Unspecified behavior is not reconstructed; it remains unknown or requires an operator decision.

## Tests

Run the focused tests listed in `## Code Targets` for this spec. These tests define the reconstructed acceptance boundary and should be kept focused on the committed behavior summarized above.

## Reconstruction Note

This spec was reconstructed on 2026-06-14 by reading the contaminated spec's `## Code Targets` section and the committed source/test files named there. The prior MCP-005 Error Taxonomy body was treated as non-authoritative contamination and was not used to infer this feature's intent. Unknown: authoritative external pricing source is not defined; committed config is the source.

## Reconstruction Sources

- `service/budget/simulator.py`
- `service/evidence/collector.py`
- `config/cost_models.yaml`
- `tests/test_budget_simulator.py`
- `tests/test_evidence_pack.py`

## Code Targets

service/budget/simulator.py; service/evidence/collector.py; config/cost_models.yaml; tests/test_budget_simulator.py; tests/test_evidence_pack.py
