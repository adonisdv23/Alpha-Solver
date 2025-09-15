<!--
Repo: Reasoning & routing layer for LLM+tools (MCP). Ships gates, scoring, observability, replay, determinism, and budget guard.
Topics: reasoning, router, mcp, observability, replay, determinism, budget, prometheus, grafana, prompt-engineering
-->

# Alpha Solver

[![CI](https://github.com/alpha-solver/alpha-solver/actions/workflows/ci.yml/badge.svg)](https://github.com/alpha-solver/alpha-solver/actions/workflows/ci.yml)
[![Tests](https://github.com/alpha-solver/alpha-solver/actions/workflows/tests.yml/badge.svg)](https://github.com/alpha-solver/alpha-solver/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What is Alpha Solver?

A reasoning/routing layer with optional MCP tool calls. Ships gates, scoring, observability, replay, determinism & budget guard.

## Status

MVP ready; P0 & P1 merged:

- Scoring & routing
- Gates & policy
- Observability & replay
- Determinism harness
- Budget guard

## Quickstart

```bash
# clone + deps
python -m pip install -U pip
pip install -r requirements.txt

# run example
python Alpha\ Solver.py

# run tests (fast)
pytest -q

# targeted suites
pytest -q -k "policy or gates or mcp or determinism or budget or observability"
```

## Using ChatGPT-5 via API (env-first)

```bash
export OPENAI_API_KEY=...
export ALPHA_MODEL="gpt-5"           # or your provider/model key
python Alpha\ Solver.py
```

### Config

Models and providers read from environment (`ALPHA_MODEL`, `ALPHA_PROVIDER`) or CLI flags. See `alpha.config.loader.load_config` for overrides.

### Record / Replay / Metrics

See [docs/OBSERVABILITY.md](docs/OBSERVABILITY.md).

### Determinism & Budget guard

See [docs/DETERMINISM.md](docs/DETERMINISM.md) and [docs/BUDGETING.md](docs/BUDGETING.md).

### Architecture overview

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

### Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License / Support

Licensed under the [MIT License](LICENSE). Issues and feature requests welcome via GitHub.

