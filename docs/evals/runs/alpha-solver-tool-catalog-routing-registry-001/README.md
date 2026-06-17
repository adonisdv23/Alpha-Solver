# ALPHA-SOLVER-TOOL-CATALOG-ROUTING-REGISTRY-001

## Purpose

Add a metadata-only tool catalog and deterministic tool recommendation preview so Alpha Solver can recommend the right class of tool for a task without executing tools, calling providers, browsing, mutating files, or expanding runtime authority.

## Catalog schema

Each tool entry records:

- `tool_id`
- `display_name`
- `tool_family`
- `task_families`
- `best_for`
- `not_for`
- `requires_network`
- `requires_credentials`
- `privacy_risk`
- `untrusted_input_risk`
- `execution_authorized`
- `enabled_by_default`
- `routing_weight`
- `confidence_effect`
- `evidence_boundary`
- `operator_notes`
- `match_keywords`

The catalog rejects entries that set `execution_authorized` to true or move outside the `metadata_only_recommendation_preview_no_tool_execution` evidence boundary.

## Initial tool families

- Python/computation
- Web/current research
- GitHub/code
- Docs/files
- Spreadsheets
- PDF/file parsing
- Browser/computer use, metadata-only and disabled by default
- Specialized math tools, metadata-only
- Future provider-specific tools, metadata-only and disabled by default

## Recommendation behavior

The tool router returns a preview containing `recommended_tool_id`, `recommended_tool_family`, `reasons`, `warnings`, `execution_authorized`, `untrusted_input_risk`, and `evidence_boundary`. Selection is deterministic and based on catalog metadata, task family, keywords, and routing weight. Failed or disabled selections fail closed and keep `execution_authorized` false.

## Injection-risk protections

Untrusted task text, requested tool names, model output text, and metadata are treated as untrusted inputs. Prompt-injection or authority-escalation phrases can add warnings, but they cannot authorize execution, enable disabled tools, or override catalog validation.

## Checks run

- `python -m pytest -q tests/test_tool_catalog.py tests/test_tool_router.py`
- `python -m pytest -q`
- `git diff --check`
- `python scripts/check_narrative_claim_safety.py docs/evals/runs/alpha-solver-tool-catalog-routing-registry-001/README.md docs/CURRENT_STATE.md docs/LANE_REGISTRY.md docs/EVIDENCE_INDEX.md`
- Source-of-truth consistency check: verified selected next state is `OPERATOR_REVIEW_REQUIRED_AFTER_TOOL_CATALOG_ROUTING_REGISTRY_001` in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md`.
- Changed-line secret-safety check: reviewed added lines for credential-like assignments and secret material.

## Explicit non-actions and non-claims

This lane does not execute tools, browse the web, call providers, run hosted or local models, pull models, mutate Google Sheets or Google Docs, call GitHub APIs from runtime code, add browser automation, add Computer Use execution, add dependencies, expose `/v1/solve`, expose dashboard or public API behavior, add scoring, unblinding, source-map work, or inspect raw outputs.

This lane does not claim tool quality, model quality, readiness, benchmark success, production/public suitability, security/privacy completion, provider validation, local-model validation, or Alpha superiority.
