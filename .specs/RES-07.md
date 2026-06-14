# CODE SPEC — RES-07 · Observability (route_explain + JSONL replay) (RES)

> Reconstructed by lane `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` from committed code and tests only. This file replaces a non-authoritative contaminated MCP-005 body. Do not infer implementation quality from this reconstruction.

## Goal

Write structured JSONL events with required route_explain fields, rotate logs, filter/replay events, and reconstruct requests.

## Acceptance Criteria

- Logger writes JSONL and rotates by size.
- Event envelope contains timestamp, pid, name, route_explain, payload, and meta.
- route_explain requires decision, confidence, and budget_verdict; only allowed optional policy/redaction fields pass through.
- Payload drops pii_raw.
- Replay iterates rotated files, filters nested fields, and reconstructs requests 10/10.

## Design

- Source of truth for this reconstruction is limited to the committed implementation and test targets listed in `## Reconstruction Sources`.
- Runtime behavior is represented by the implementation files in `## Code Targets`; expected observable behavior is represented by the listed tests.
- No provider calls, tokens, external services, or runtime code changes are required by this spec reconstruction.
- MCP-005 remains the canonical source for MCP error taxonomy names and semantics wherever error classes are referenced.
- Unspecified behavior is not reconstructed; it remains unknown or requires an operator decision.

## Tests

Run the focused tests listed in `## Code Targets` for this spec. These tests define the reconstructed acceptance boundary and should be kept focused on the committed behavior summarized above.

## Reconstruction Note

This spec was reconstructed on 2026-06-14 by reading the contaminated spec's `## Code Targets` section and the committed source/test files named there. The prior MCP-005 Error Taxonomy body was treated as non-authoritative contamination and was not used to infer this feature's intent. Unknown: central log aggregation is not defined.

## Reconstruction Sources

- `service/observability/logger.py`
- `service/observability/replay.py`
- `tests/test_observability.py`

## Code Targets

service/observability/logger.py; service/observability/replay.py; tests/test_observability.py
