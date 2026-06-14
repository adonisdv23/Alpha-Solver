# Per-Spec Source Map

| Spec | Sources |
| --- | --- |
| `MCP-001` | `registries/mcp/loader.py`; `service/mcp/wiring.py`; `tests/test_mcp_loader.py` |
| `MCP-002` | `registries/mcp/registry_lookup.py`; `tests/test_mcp_router_rule.py` |
| `MCP-003` | `service/mcp/policy_auth.py`; `tests/test_mcp_auth.py` |
| `MCP-004` | `service/mcp/sandbox_limits.py`; `tests/test_mcp_sandbox.py` |
| `MCP-006` | `service/mcp/retry_backoff.py`; `tests/test_mcp_retry.py` |
| `MCP-007` | `service/mcp/observability.py`; `tests/test_mcp_observability.py` |
| `NEW-009` | `service/clarify/trigger.py`; `service/clarify/templates.yaml`; `service/clarify/render.py`; `tests/test_clarify.py` |
| `NEW-010` | `service/prompts/decks.yaml`; `service/prompts/selector.py`; `service/prompts/renderer.py`; `tests/test_prompt_decks.py` |
| `NEW-011` | `service/scoring/tuning.py`; `config/tuning.yaml`; `tests/test_weight_tuning.py` |
| `NEW-012` | `service/budget/guard.py`; `service/budget/cli.py`; `tests/test_budget_cli_guard.py` |
| `NEW-013` | `service/observability/replay_cli.py`; `service/observability/diff.py`; `tests/test_replay_cli_diff.py` |
| `NEW-014` | `service/evidence/store.py`; `service/evidence/index.jsonl`; `service/evidence/api.py`; `tests/test_evidence_store.py` |
| `NEW-015` | `service/determinism/harness.py`; `service/determinism/report.py`; `config/determinism.yaml`; `tests/test_determinism.py` |
| `NEW-016` | `service/metrics/exporter.py`; `dashboards/alpha_observability.json`; `dashboards/cost_budget.json`; `tests/test_metrics_dashboards.py` |
| `NEW-017` | `service/prompts/quality/rubrics.yaml`; `service/prompts/quality/evaluator.py`; `service/prompts/quality/report.py`; `tests/test_prompt_quality.py` |
| `RES-03` | `service/scoring/decision_rules.py`; `config/decision_rules.yaml`; `tests/test_decision_rules.py` |
| `RES-04` | `service/gating/gates.py`; `alpha_solver_cli.py`; `tests/test_gates.py` |
| `RES-05` | `service/adapters/base.py`; `service/adapters/playwright_adapter.py`; `service/adapters/gsheets_adapter.py`; `tests/test_adapters_playwright.py`; `tests/test_adapters_gsheets.py` |
| `RES-06` | `service/scenarios/runner.py`; `service/scenarios/rubric.py`; `scenarios/pack.yaml`; `tests/test_scenarios.py` |
| `RES-07` | `service/observability/logger.py`; `service/observability/replay.py`; `tests/test_observability.py` |
| `RES-08` | `service/budget/simulator.py`; `service/evidence/collector.py`; `config/cost_models.yaml`; `tests/test_budget_simulator.py`; `tests/test_evidence_pack.py` |
| `AS-145` | `service/adapters/base.py`; `service/adapters/playwright_adapter.py`; `service/adapters/gsheets_adapter.py`; `tests/test_adapters_playwright_hardened.py`; `tests/test_adapters_gsheets_hardened.py` |
