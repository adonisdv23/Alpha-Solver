# CODE SPEC — RES-05 · Tool Adapters (Playwright, GSheets) — MVP stubs (RES)

> Reconstructed by lane `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` from committed code and tests only. This file replaces a non-authoritative contaminated MCP-005 body. Do not infer implementation quality from this reconstruction.

## Goal

Provide deterministic Playwright and GSheets adapter stubs with schema errors, retry metadata, idempotent sheet append, and route explanations.

## Acceptance Criteria

- Playwright get_text returns fixture text and schema/timeout errors map to AdapterError codes/retryability.
- GSheets append is idempotent for repeated keys and read returns rows.
- Invalid schemas raise non-retryable schema errors.
- Route explanations include adapter, latency, attempts, and retriable/idempotent fields.
- Sample adapter success rate is at least 95%.

## Design

- Source of truth for this reconstruction is limited to the committed implementation and test targets listed in `## Reconstruction Sources`.
- Runtime behavior is represented by the implementation files in `## Code Targets`; expected observable behavior is represented by the listed tests.
- No provider calls, tokens, external services, or runtime code changes are required by this spec reconstruction.
- MCP-005 remains the canonical source for MCP error taxonomy names and semantics wherever error classes are referenced.
- Unspecified behavior is not reconstructed; it remains unknown or requires an operator decision.

## Tests

Run the focused tests listed in `## Code Targets` for this spec. These tests define the reconstructed acceptance boundary and should be kept focused on the committed behavior summarized above.

## Reconstruction Note

This spec was reconstructed on 2026-06-14 by reading the contaminated spec's `## Code Targets` section and the committed source/test files named there. The prior MCP-005 Error Taxonomy body was treated as non-authoritative contamination and was not used to infer this feature's intent. Unknown: real browser/API integration is not in MVP stub sources.

## Reconstruction Sources

- `service/adapters/base.py`
- `service/adapters/playwright_adapter.py`
- `service/adapters/gsheets_adapter.py`
- `tests/test_adapters_playwright.py`
- `tests/test_adapters_gsheets.py`

## Code Targets

service/adapters/base.py; service/adapters/playwright_adapter.py; service/adapters/gsheets_adapter.py; tests/test_adapters_playwright.py; tests/test_adapters_gsheets.py
