# ALPHA-SOLVER-SUBSTANTIVE-LIFT-CASE-ANCHOR-HARDENING-001

## Goal

Harden the portable Substantive Lift wording contract so prompt-aware checks can reject structurally valid but generic lift blocks that could be reused under unrelated prompts.

## Motivation

The manual evaluation lane showed that a six-line lift block can satisfy label order, length, anti-hedge wording, and executable-next checks while still avoiding the concrete objects in the task. This spec narrows that gap on the portable surface by adding deterministic case-anchoring checks when prompt anchors are available.

## Scope

- Add case-anchoring contract wording to `alpha_solver_portable.py`.
- Add conservative deterministic prompt-anchor extraction for files, paths, PR references, issue references, backticked spans, uppercase lane IDs, and number-bearing identifier tokens.
- Extend `check_substantive_lift(solution_text, prompt=None)` with prompt-aware result fields while preserving prompt-omitted compatibility.
- Add fixtures and tests for generic cosplay blocks, anchored counterparts, anchor extraction, vacuous anchor-free prompts, intent-restatement checks, filler checks, and summary/spec indexing.

## Non-goals

- No `/v1/solve` changes.
- No dashboard or API changes.
- No routing, persona, SAFE-OUT, SolverEnvelope, budget, determinism, replay, observability, scoring, ranking, winner-field, source-map, identity-map, or benchmark changes.
- No provider calls, hosted model calls, or local model calls.
- No answer-quality, readiness, production, provider-validation, local-model-validation, model-superiority, or Alpha-superiority claims.

## Code targets

- `alpha_solver_portable.py`
- `tests/fixtures/alpha_substantive_lift_cases.json`
- `tests/test_alpha_substantive_lift_contract.py`
- `.specs/ALPHA-SOLVER-SUBSTANTIVE-LIFT-CASE-ANCHOR-HARDENING-001.md`
- `.specs/INDEX.md`

## Test plan

Run the focused and regression checks requested for this lane:

```bash
python -m pytest tests/test_alpha_substantive_lift_contract.py -q
python -m pytest tests/test_alpha_minimal_behavior_contract.py -q
python -m pytest tests/test_alpha_local_runtime_honesty.py -q
python -m pytest tests/test_alpha_no_echo_wiring.py -q
python -m pytest -q
python scripts/check_narrative_claim_safety.py .specs/ALPHA-SOLVER-SUBSTANTIVE-LIFT-CASE-ANCHOR-HARDENING-001.md
ruff check alpha_solver_portable.py tests/test_alpha_substantive_lift_contract.py
```

## Acceptance criteria

- The contract summary includes the case-anchoring rules, including the required non-compliance sentence.
- A structurally valid generic lift block passes the prompt-omitted checker path, proving the old shape-only gap remains representable in tests.
- The same generic lift block fails when prompt anchors are provided.
- Anchored counterpart examples pass when prompt anchors are provided.
- Anchor-free prompts do not create an unanchored failure.
- Intent restatement is flagged only for narrow obvious restatement patterns.
- Filler detection uses explicit word-boundary regexes only.
- The spec is indexed.

## Definition of done

- The implementation is limited to the scoped portable files.
- The checker remains deterministic and uses explicit regexes only.
- Back-compat for `check_substantive_lift(solution_text)` callers is preserved.
- Validation results are reported with exact commands.
- The PR description includes live-state verification, the pre-patch cosplay proof, changed files, implementation summary, validation results, explicit non-claims, and remaining risks.

## Explicit non-claims

A passing checker means only that the configured structural wording, anti-generic, and case-anchoring checks held for the supplied text and optional prompt. This lane does not claim improved answer quality, benchmark performance, production readiness, provider validation, local-model validation, model superiority, or Alpha superiority.
