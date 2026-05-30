# Alpha Solver Quickstart

This guide gets you running Alpha Solver from a fresh macOS checkout.

## 1. Confirm Python 3.12+

Alpha Solver requires Python 3.12 or newer:

```bash
python3 --version
```

If needed, install a current Python first. For example, with Homebrew:

```bash
brew install python@3.12
```

## 2. Clone and install

```bash
git clone https://github.com/adonisdv23/Alpha-Solver.git
cd Alpha-Solver

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If your Python 3.12+ executable has a different name, use that executable when creating `.venv`.

## 3. Configure environment

Copy the example environment file:

```bash
cp .env.example .env
```

The example file defaults to the verified local/offline mode:

```bash
MODEL_PROVIDER=local
```

Use `local` for offline checks. `MODEL_PROVIDER=none` is also accepted for no-key local validation. Remote-provider modes currently validate required environment variables only; `python scripts/check_env.py` does not perform remote LLM API calls and does not prove remote provider usability.

For provider-specific environment checks, set the matching key variable in your private `.env`:

- `MODEL_PROVIDER=openai` requires `OPENAI_API_KEY`.
- `MODEL_PROVIDER=anthropic` requires `ANTHROPIC_API_KEY`.
- `MODEL_PROVIDER=gemini` or `MODEL_PROVIDER=google` requires `GOOGLE_API_KEY`.

## 4. Validate setup

```bash
set -a
source .env
set +a
python scripts/check_env.py
```

For local/offline validation without editing `.env`, run:

```bash
MODEL_PROVIDER=local python scripts/check_env.py
```

## 5. Run smoke checks

```bash
python cli/alpha_solver_cli.py --help
python alpha_solver_cli.py --help
python -m alpha.cli --help
python alpha_solver_portable.py "Summarize Alpha Solver restart state" --json --deterministic
```

## 6. Run tests

```bash
python -m pytest -q
```

## Optional server command

If you have installed the service dependencies needed by your environment, start the API server with:

```bash
make run
```

The API is then available at [http://localhost:8000](http://localhost:8000).

Codespaces users can run the same repository commands in the integrated terminal.
