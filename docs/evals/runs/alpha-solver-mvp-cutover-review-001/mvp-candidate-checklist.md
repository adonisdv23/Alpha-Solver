# MVP candidate checklist

Verdict: `LOCAL_OPERATOR_MVP_CANDIDATE_READY_FOR_MANUAL_REVIEW`.

| # | Criterion | Status | Evidence inspected |
|---|-----------|--------|--------------------|
| 1 | local console exists | Pass | `tools/operator_test_console.py`; `tests/test_operator_test_console.py` |
| 2 | route preview exists | Pass | console routing preview integration; `alpha/model_router.py`; `alpha/tool_router.py` |
| 3 | route preview is metadata-only | Pass | model/tool catalog and router boundaries state no provider, local-model, or tool execution |
| 4 | model recommendation appears | Pass | route preview exposes recommended model path metadata |
| 5 | tool recommendation appears | Pass | route preview exposes recommended tool path metadata |
| 6 | reasons appear | Pass | model and tool routers return reasons |
| 7 | warnings appear | Pass | model and tool routers return warnings |
| 8 | fallback appears | Pass | model router fallback path metadata exists |
| 9 | evidence boundary appears | Pass | model/tool catalog and preview metadata expose evidence boundary |
| 10 | execution authorization flags are false | Pass | catalog/router metadata keeps execution authorization false |
| 11 | preview does not execute providers | Pass | preview uses metadata-only router/catalog paths |
| 12 | preview does not execute local models | Pass | preview uses metadata-only router/catalog paths |
| 13 | preview does not execute tools | Pass | tool routing is metadata-only and execution-disabled |
| 14 | smoke execution remains separate | Pass | console separates preview from explicit smoke submit path |
| 15 | sanitized JSON exists | Pass | console has sanitized JSON output panel |
| 16 | copy behavior is scoped to sanitized JSON | Pass | console copy behavior is scoped to sanitized JSON |
| 17 | prompt-too-long behavior is fail-closed | Pass | console prompt length limit behavior is tested and blocks smoke execution |
| 18 | model/tool catalog metadata exists | Pass | `configs/model_catalog.json`; `configs/tool_catalog.json` |
| 19 | routed-vs-plain pilot packet exists | Pass | `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-packet-001/` |
| 20 | source-of-truth docs agree | Pass | `docs/CURRENT_STATE.md`; `docs/LANE_REGISTRY.md`; `docs/EVIDENCE_INDEX.md` |

## Boundary

This checklist supports only local operator manual review readiness for the candidate console workflow. It does not create production readiness, public readiness, benchmark readiness, provider readiness, local-model readiness, security/privacy completion, tool-quality validation, autonomous execution readiness, or Alpha-superiority evidence.
