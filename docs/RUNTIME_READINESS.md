# Runtime Readiness

A practical status matrix for Alpha Solver runtime surfaces. This document tells operators and AI agents what is verified, what is local/offline only, what is mocked or simulated, what requires credentials, and what is future work.

This document does not replace `.specs/`. Specs define intended behavior. This document summarizes current runtime truth.

Provider environment validation does not prove live provider usability. Remote-provider modes can require the presence of API-key environment variables, but current validated paths do not perform live LLM provider API calls by default.

## Status Legend

| Status                    | Meaning                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| Verified local/offline    | Works without external credentials or services.                                             |
| Env-validation only       | Config/env variables can be checked, but no live API call is made.                          |
| Mocked / simulated        | Tests or adapters simulate behavior without real external execution.                        |
| Partial                   | Some supporting pieces exist, but end-to-end runtime is not complete.                       |
| Placeholder / future      | File, doc, or test exists mainly as a future target.                                        |
| Requires external service | Needs credentials, Docker, Redis, Prometheus, Grafana, browser tooling, or another service. |
| Not implemented           | No working implementation yet.                                                              |

## Runtime Surface Matrix

| Surface | Current status | What works now | What does not work yet | Credentials/services needed | Source of truth / next step |
| ------- | -------------- | -------------- | ---------------------- | ---------------------------- | --------------------------- |
| Local/offline solver core | Verified local/offline | Deterministic local solver paths run without provider credentials. | Live remote-provider execution is not part of the default local path. | None for local/offline use. | Existing solver tests and `.specs/` behavior contracts. |
| `alpha_solver_portable.py` | Verified local/offline | Standalone deterministic behavior contract and portable solver path. | It should not run live providers unless a future approved spec explicitly changes that. | None for portable local/offline use. | `docs/ENTRYPOINTS.md` and `alpha_solver_portable.py`. |
| Root CLI: `alpha_solver_cli.py` | Verified local/offline | Root Tree-of-Thought CLI invokes local `_tree_of_thought` behavior and prints JSON. | No live provider client execution. | None for local CLI use. | `docs/ENTRYPOINTS.md`, `docs/CLI.md`, and CLI smoke tests. |
| Package CLI: `python -m alpha.cli` | Verified local/offline | Package CLI supports local solve/eval/gate/budget/router commands from repo checkout. | No live provider client execution. | None for local CLI use; dataset/report inputs may be needed for specific subcommands. | `docs/CLI.md`, `alpha/cli/main.py`, and CLI tests. |
| Command CLI: `cli/alpha_solver_cli.py` | Verified local/offline | Command-oriented CLI supports local run/replay/gates/finops/traces-style workflows. | No live provider client execution. | None for local CLI use; replay input files may be needed for replay. | `docs/ENTRYPOINTS.md`, `docs/CLI.md`, and CLI tests. |
| FastAPI service `/v1/solve` | Verified local/offline / Partial | Existing route calls local deterministic ToT/ReAct-style runtime paths and is covered by service/API tests. | Live OpenAI provider execution is specified for the future but is not implemented in `/v1/solve` yet. | None for local API tests; service runtime dependencies depend on deployment mode. | Service tests and `.specs/PROVIDER-OPENAI-001.md` for future provider behavior. |
| `.env.example` | Verified local/offline | Defaults to `MODEL_PROVIDER=local`, the safe local/offline environment value. | Placeholder key examples do not enable or prove real remote LLM execution. | None when left at `MODEL_PROVIDER=local`. | `.env.example` and `scripts/check_env.py`. |
| `scripts/check_env.py` | Env-validation only | Validates `MODEL_PROVIDER`, expected key-variable presence, and basic config invariants. | It does not perform remote provider API pings or prove provider usability. | Provider-specific key variables are required only for remote-provider env-validation modes. | `scripts/check_env.py`; keep default checks credential-free. |
| OpenAI provider mode | Env-validation only / Placeholder / future | `MODEL_PROVIDER=openai` can require/check `OPENAI_API_KEY` presence through `scripts/check_env.py`. | No real OpenAI provider execution is implemented yet. | `OPENAI_API_KEY` for env validation only; no key is required for default local/offline mode. | `.specs/PROVIDER-OPENAI-001.md`. |
| Anthropic provider mode | Env-validation only / Placeholder / future | `MODEL_PROVIDER=anthropic` can require/check `ANTHROPIC_API_KEY` presence through `scripts/check_env.py`. | No real Anthropic provider execution is implemented. | `ANTHROPIC_API_KEY` for env validation only. | Future provider spec would be required before behavior changes. |
| Gemini/Google provider mode | Env-validation only / Placeholder / future | `MODEL_PROVIDER=gemini` or `MODEL_PROVIDER=google` can require/check `GOOGLE_API_KEY` presence through `scripts/check_env.py`. | No real Gemini/Google provider execution is implemented. | `GOOGLE_API_KEY` for env validation only. | Future provider spec would be required before behavior changes. |
| Deepseek adapter | Mocked / simulated / Placeholder / future | A Deepseek prompt adapter can render prompt dictionaries. | `deepseek` is not accepted by the current env checker and no real Deepseek provider execution is implemented. | None for prompt-rendering tests; live execution is not available. | Existing adapter code/tests; future provider spec required for real execution. |
| Provider prompt adapters | Mocked / simulated | OpenAI, Anthropic, Gemini, and Deepseek adapter classes render prompt dictionaries for tests and routing surfaces. | They are not remote provider clients and do not execute live provider API calls. | None for prompt rendering. | Existing adapter tests plus future provider specs. |
| OpenAI real provider execution | Not implemented | `.specs/PROVIDER-OPENAI-001.md` defines the future implementation contract. | Provider client abstraction, live OpenAI call path, safe error normalization, usage/cost capture, and opt-in `/v1/solve` integration are not implemented yet. | Future opt-in implementation will require `OPENAI_API_KEY`; default CI should remain keyless. | `.specs/PROVIDER-OPENAI-001.md`. |
| Model-set registry/resolver | Partial | Model-set config loading and deterministic resolution support model/provider metadata and price hints. | It is not a provider executor and does not call remote models. | None for local registry/resolver tests. | `service/models/modelset_registry.py`, `service/models/modelset_resolver.py`, and model-set tests. |
| Python client SDK | Partial | Client package/docs and tests exist for API-style integration. | It depends on a running Alpha Solver service for end-to-end calls; it does not make provider execution real by itself. | Running API service for live integration use. | `clients/python/` docs/code and client SDK tests. |
| MCP adapters | Partial / Requires external service | MCP adapter, registry, policy/auth, retry, sandbox, and observability scaffolding/tests exist. | Real tool availability depends on configured MCP registries, credentials, and external tool services. | External MCP servers/tools and any required OAuth/secrets for live use. | MCP specs, `docs/ADDING_TOOLS.md`, `alpha/tools/mcp_adapter.py`, and `service/mcp/`. |
| Google Sheets adapter/tooling | Mocked / simulated / Requires external service | Adapter tests cover local/mocked Google Sheets behavior. | Live Google Sheets execution requires credentials and configured external access. | Google credentials/OAuth and network access for live use. | `service/adapters/gsheets_adapter.py` and adapter tests. |
| Browser/Playwright/web extraction adapter/tooling | Mocked / simulated / Requires external service | Adapter tests and hardening tests cover local/mocked browser extraction behavior. | Live browser extraction requires browser tooling and target-site/network availability. | Playwright/browser runtime and network access for live use. | `service/adapters/playwright_adapter.py` and adapter tests. |
| Health/readiness endpoints | Partial | Service endpoints such as `/health`, `/ready`, `/healthz`, and `/readyz` exist. | Placeholder or future health targets may still describe richer dependency checks that are not fully implemented. | None for basic local service health; future dependency checks may require Redis, VectorDB, or provider pings. | `service/app.py`, `service/health.py`, `.specs/NEW-HEALTH-001.md`, and health docs/tests. |
| Rate limiting | Partial | An in-process service rate limiter exists and can emit rate-limit telemetry. | The previously labeled Redis/SlowAPI-style token-bucket target is not fully implemented as described by the spec. | None for in-process limiter; Redis would be required for the future Redis-backed target. | `.specs/NEW-RATE-001.md`, `docs/RATE_LIMITING.md`, and backlog follow-up. |
| Metrics endpoint | Partial | `/metrics` exposes Prometheus-format metrics from the running service. | Complete production observability depends on collector/scrape configuration and deployment wiring. | Prometheus or compatible scraper for external collection. | `service/app.py`, `service/metrics/exporter.py`, `docs/METRICS.md`, and metrics tests. |
| Grafana/Prometheus dashboards | Requires external service / Partial | Dashboard JSON and observability docs exist. | Dashboards require external Grafana/Prometheus infrastructure and populated metrics. | Grafana, Prometheus, and service metrics scraping. | `observability/grafana/dashboards/`, `docs/GRAFANA_DASHBOARDS.md`, and dashboard tests. |
| Docker/compose/runtime infrastructure | Requires external service / Partial | Compose files exist for containerized/runtime infrastructure experiments. | Containerized production readiness depends on local Docker, configured services, secrets, and deployment validation. | Docker/Compose and any declared backing services. | `infrastructure/docker-compose.yml`, `infrastructure/docker-compose.prod.yml`, and deployment docs. |
| Benchmark scripts | Verified local/offline / Partial | Local benchmark scripts/tests can exercise deterministic benchmark paths. | Benchmarks do not prove live provider readiness unless a future gated live smoke path is added. | None for local benchmark scripts; datasets/config may be needed. | `scripts/benchmark_tot.py`, `alpha/core/benchmark.py`, docs, and benchmark tests. |
| Replay/determinism tooling | Verified local/offline | Replay, determinism harnesses, gates, reports, and tests support local reproducibility checks. | They do not prove live provider determinism or remote-provider availability. | None for local replay/determinism tests; replay datasets may be needed. | `docs/REPLAY_GUIDE.md`, `docs/DETERMINISM.md`, `service/replay/`, `service/determinism/`, and tests. |
| Reliability/SLO gates | Partial / Placeholder / future | Quality gates and docs exist for local reports and CI-style checks. | Full production SLO enforcement and external runtime gates are not complete. | Depends on metrics, dashboards, service deployment, and configured thresholds. | `docs/QUALITY_GATES.md`, `docs/TRACING_ALERTS.md`, gate CLI/tests, and future specs. |
| Placeholder health/rate-limit targets | Placeholder / future | Specs/docs identify intended richer health and Redis-backed rate-limit behavior. | These placeholders must not be mistaken for completed production implementations. | Future implementations may require Redis, provider ping configuration, VectorDB, or other services. | `.specs/NEW-HEALTH-001.md`, `.specs/NEW-RATE-001.md`, and backlog follow-up. |

## Provider Mode Matrix

| Provider/mode | Accepted by env checker? | Requires key? | Live API call implemented? | Default CI? | Notes |
| ------------- | ------------------------ | ------------- | -------------------------- | ----------- | ----- |
| `local` | Yes | No | No | Yes | Safe verified default for local/offline checks. |
| `none` | Yes | No | No | Acceptable for no-key validation | Accepted by the env checker for no-key local validation. |
| `openai` | Yes | `OPENAI_API_KEY` | No | No | Env validation requires key presence, but real OpenAI execution is specified and not implemented. |
| `anthropic` | Yes | `ANTHROPIC_API_KEY` | No | No | Env validation requires key presence only; no live Anthropic execution is implemented. |
| `gemini` | Yes | `GOOGLE_API_KEY` | No | No | Env validation requires key presence only; no live Gemini execution is implemented. |
| `google` | Yes | `GOOGLE_API_KEY` | No | No | Alias-style env-check mode for Google/Gemini key validation; no live Google provider execution is implemented. |
| `dummy` | No | No | No | No | Not accepted by the current env checker; treat any dummy/fake behavior as internal test scaffolding, not a user-facing remote provider mode. |
| `deepseek` | No | No | No | No | Prompt adapter exists, but `deepseek` is not accepted by `scripts/check_env.py` and no live Deepseek execution is implemented. |

## Known Gaps

1. Real OpenAI provider execution is specified in `.specs/PROVIDER-OPENAI-001.md` but not implemented.
2. Runtime readiness should be updated after provider implementation PRs.
3. Remote provider modes currently validate env-var presence only; they do not prove live provider usability.
4. Some external-tool surfaces may be simulated, credentialed, or service-dependent.
5. Placeholder health/rate-limit targets should not be mistaken for complete implementations.
6. Rate limiting needs separate follow-up for the Redis/SlowAPI mismatch if still relevant.
7. Optional live provider smoke tests should be gated and never part of default CI.

## Update Rules

Update this document when:

* a provider implementation is added or materially changed;
* a placeholder is retired or implemented;
* a runtime surface changes from local/offline to real external execution;
* an external service becomes required or optional;
* a spec changes runtime expectations;
* a smoke test or CI gate changes what is verified.

Do not use this document to create new behavior. Behavior changes require `.specs/` first.
