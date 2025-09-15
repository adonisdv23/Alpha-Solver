# Pilot Readiness Quickstart

This guide covers the minimum steps required to stand up the Alpha Solver pilot, validate the smoke deck, and prepare a tagged release. The flow is designed so a fresh clone can complete the checklist in well under ten minutes on a typical developer laptop.

## Quickstart (≤10 minutes)
1. **Install dependencies**
   ```bash
   python -m pip install -U pip && pip install -r requirements.txt
   ```
2. **Prepare environment placeholders** – the example file only contains safe dummy values.
   ```bash
   cp .env.example .env
   ```
3. **Boot the service and verify health**
   ```bash
   make run &
   curl -sS localhost:8000/healthz
   ```
4. **Replay the smoke deck and check determinism** – run the replay command followed by the determinism gate to confirm stability before promoting a release.
   ```bash
   python cli/alpha_solver_cli.py replay data/scenarios/decks/smoke.jsonl --max-tokens 120 --min-budget-tokens 60
   pytest -q -k determinism_gate
   ```
   Stop the background server once the checks pass.

## Smoke Validation
- `make smoke` will build or refresh `data/scenarios/decks/smoke.jsonl`, execute the replay harness, report a ≥95% pass rate, and print an Obs Card sample for manual review.
- The lightweight deck contains concise prompts so runs complete in seconds.

## Release Flow
- `make release` runs `scripts/release.py`, regenerating `docs/RELEASE_NOTES_v0.1.md` from git history, writing `VERSION` with `0.1.0`, and creating an annotated tag `v0.1.0` locally (the script never pushes tags).
- Release notes and the VERSION file are idempotent; re-running the target does not change tracked files when no new commits land.
- Remember to run the determinism gate (`pytest -q -k determinism_gate` or `make test-gates`) before cutting a release.

## Evidence Pack
Additional runnable snippets and deep-dive checks live in the [Evidence Pack](EVIDENCE_PACK.md). Use it to demo math evaluators, gating behaviour, tracing, and policy redaction in the pilot environment.

## Pilot Checklist
See [docs/PILOT_CHECKLIST.md](PILOT_CHECKLIST.md) for the full readiness gate covering operations, smoke coverage, and release artefacts.
