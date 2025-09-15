# Pilot Readiness Checklist v0.1.0

Use this checklist to confirm Alpha Solver is ready for pilot release v0.1.0. Each item should be checked during the same working session so the environment used for validation matches the tagged commit.

## Environment Bring-Up
- [ ] Fresh clone installs dependencies via `python -m pip install -U pip && pip install -r requirements.txt`.
- [ ] `.env` copied from `.env.example` with only placeholder values.
- [ ] `make run` starts the FastAPI service; `/healthz` and `/metrics` return HTTP 200 locally.

## Smoke Deck Verification
- [ ] `make smoke` reports deck size (5–10 records), prints an Obs Card example, and shows ≥95% pass rate.
- [ ] Replay command (`python cli/alpha_solver_cli.py replay data/scenarios/decks/smoke.jsonl --max-tokens 120 --min-budget-tokens 60`) succeeds.
- [ ] Evidence Pack math evaluator (`alpha.executors.math_exec.evaluate("2+2")`) returns `4.0`.

## Quality Gates
- [ ] Determinism gate passes (`pytest -q -k determinism_gate` or `make test-gates`).
- [ ] Policy, budget, and metrics gates run as needed for the pilot scope.

## Release Artefacts
- [ ] `VERSION` file reflects `0.1.0`.
- [ ] `docs/RELEASE_NOTES_v0.1.md` regenerated from `scripts/release.py` and committed.
- [ ] Annotated tag `v0.1.0` exists locally (`git tag -n v0.1.0`) and has not been pushed yet.
- [ ] CHANGELOG and README links verified (Evidence Pack, smoke instructions, release flow).

Document completion of the checklist in your pilot readiness ticket or release PR description.
