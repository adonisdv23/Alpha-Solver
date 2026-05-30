<!--
Repo: Reasoning & routing layer for LLM+tools (MCP). Ships gates, scoring, observability, replay, determinism, and budget guard.
Topics: reasoning, router, mcp, observability, replay, determinism, budget, prometheus, grafana, prompt-engineering
-->

# Alpha Solver

[![CI](https://github.com/adonisdv23/Alpha-Solver/actions/workflows/ci.yml/badge.svg)](https://github.com/adonisdv23/Alpha-Solver/actions/workflows/ci.yml)
[![Tests](https://github.com/adonisdv23/Alpha-Solver/actions/workflows/tests.yml/badge.svg)](https://github.com/adonisdv23/Alpha-Solver/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What is Alpha Solver?

Alpha Solver is a reasoning/routing layer with optional MCP tool calls. It ships gates, scoring, observability, replay, determinism, and a budget guard.

See [docs/OPERATING_GUIDE.md](docs/OPERATING_GUIDE.md) for the working
process: roles, when specs are required, and how PRs are reviewed and merged.

See [docs/RUNTIME_READINESS.md](docs/RUNTIME_READINESS.md) for the current
runtime status matrix: what works locally, what is env-validation only, what is
mocked/simulated, and what remains future work.

## Status

MVP ready; P0 & P1 merged:

- Scoring & routing
- Gates & policy
- Observability & replay
- Determinism harness
- Budget guard

## Fresh macOS setup

Alpha Solver requires Python 3.12 or newer. On a fresh Mac, first confirm your Python version:

```bash
python3 --version
```

If that prints a version older than 3.12, install a newer Python before continuing. One common macOS option is Homebrew:

```bash
brew install python@3.12
```

Then clone the real repository and install dependencies in a virtual environment:

```bash
git clone https://github.com/adonisdv23/Alpha-Solver.git
cd Alpha-Solver

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `python3.12` is not the executable name on your machine, use any Python 3.12+ executable for the `venv` command.

## Configure environment

Copy the example environment file for the verified local/offline default:

```bash
cp .env.example .env
```

The sample file uses `MODEL_PROVIDER=local`. This is the safe default for local checks and does not require OpenAI, Anthropic, or Google credentials. `MODEL_PROVIDER=none` is also accepted by the environment checker for no-key local validation.

Remote-provider modes currently have environment-variable validation only. The checker verifies that the expected key variable is present; it does not call a remote LLM API and does not prove that a remote provider is usable. Do not add real secrets to source-controlled files.

If you are doing provider-specific work, set `MODEL_PROVIDER` and the matching placeholder or secret in your private `.env`:

```bash
# OpenAI env-var presence check
MODEL_PROVIDER=openai
OPENAI_API_KEY=placeholder

# Anthropic env-var presence check
MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=placeholder

# Google Gemini env-var presence check
MODEL_PROVIDER=gemini   # or: google
GOOGLE_API_KEY=placeholder
```

Provider values accepted by the environment checker are `local`, `none`, `openai`, `anthropic`, `gemini`, and `google`. Unknown provider values fail with an allowed-values message.

Load the `.env` file into your shell, then validate the environment configuration:

```bash
set -a
source .env
set +a
python scripts/check_env.py
```

You can also validate the local/offline default without editing `.env`:

```bash
MODEL_PROVIDER=local python scripts/check_env.py
```

## Smoke checks and common commands

Use these commands to confirm the checkout is runnable:

```bash
python cli/alpha_solver_cli.py --help
python alpha_solver_cli.py --help
python -m alpha.cli --help
python alpha_solver_portable.py "Summarize Alpha Solver restart state" --json --deterministic
python -m pytest -q
```

Runnable tracked entrypoints include:

- `alpha_solver_portable.py`
- `alpha_solver_cli.py`
- `cli/alpha_solver_cli.py`
- `alpha_solver_entry.py`
- `python -m alpha.cli`

## CLI usage

The offline CLI wrapper exposes commands such as `run`, `replay`, `gates`, `finops`, and `traces`:

```bash
python cli/alpha_solver_cli.py --help
echo "hello world" | python cli/alpha_solver_cli.py run
```

The package CLI is also available from the repository checkout:

```bash
python -m alpha.cli --help
```

See [docs/CLI.md](docs/CLI.md) for more CLI examples.

## Record / Replay / Metrics

See [docs/OBSERVABILITY.md](docs/OBSERVABILITY.md).

## Determinism & Budget guard

See [docs/DETERMINISM.md](docs/DETERMINISM.md) and [docs/BUDGETING.md](docs/BUDGETING.md).

## Architecture overview

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). For the role of the portable, modular/reference, bridge, and CLI entrypoint files, see [docs/ENTRYPOINTS.md](docs/ENTRYPOINTS.md).

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License / Support

Licensed under the [MIT License](LICENSE). Issues and feature requests welcome via GitHub.
