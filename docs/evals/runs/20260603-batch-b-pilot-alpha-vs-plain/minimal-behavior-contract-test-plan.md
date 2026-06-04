# Minimal Alpha Behavior Contract Test Plan

## 1. Purpose

This plan defines the first contract-first, test-first lane after the Alpha
implementation-readiness review. It adds offline deterministic tests for minimal
Alpha behavior-contract examples before any runtime behavior change is proposed.

The lane is `ALPHA-MINIMAL-BEHAVIOR-CONTRACT-AND-TESTS-001`. It records desired
answer-shape, claim-boundary, evidence-boundary, and artifact stop-condition
examples as committed fixtures. Runtime enforcement is not implemented in this
PR.

## 2. Evidence basis

This plan is based on committed repository artifacts only:

- Batch B scored artifacts in
  `docs/evals/runs/20260603-batch-b-pilot-alpha-vs-plain/`.
- `interpretation-review.md` and `post-interpretation-decision.md`.
- `.specs/ALPHA-BREVITY-CONTROL-001.md`.
- The claim-boundary calibration packet in the Batch B run directory.
- `.specs/ALPHA-ANSWER-STRUCTURE-V2-001.md`.
- `implementation-readiness-review.md`.
- `minimal-implementation-decision-matrix.csv`.

The committed score math remains bounded:

- A3-1: Plain 237, Alpha 228, delta -9.
- Batch B: Plain 405, Alpha 455, delta +50.

These figures support planning a narrow next lane. They are planning evidence,
not validation.

## 3. What this PR tests

This PR tests static behavior-contract fixtures and documentation patterns. The
new tests validate that examples:

- Start short answers with the direct answer when the prompt asks a yes/no
  question.
- Keep reviewer comments brief instead of converting them into full memos.
- Avoid unrequested sections for one-sentence prompts.
- Avoid invented owners, dates, file paths, commands, metrics, acceptance
  criteria, and implementation claims when not supplied or explicitly requested.
- Use safe wording for limited evidence: "limited pilot favored Alpha," "does
  not establish broad superiority," "planning evidence, not validation," and
  "repo evidence overrides planning ledger."
- Stop when required score tables, capture packets, or raw provider payloads are
  missing instead of reconstructing evidence or making unsafe proof claims.

## 4. What this PR does not implement

This PR does not implement runtime enforcement. It does not change
provider/model/routing behavior, does not change /v1/solve, and does not
change prompts, SAFE-OUT, SolverEnvelope behavior,
scoring rubrics, scored artifacts, capture scripts, or Google Sheets
integrations.

The tests are offline deterministic tests. This PR does not call live
providers, does not require OPENAI_API_KEY, does not rerun capture, does not
rescore outputs, does not update Google Sheets, and does not start Batch C.

## 5. Test groups

The fixture and tests cover six groups:

1. **Short-answer-first**: yes/no, reviewer comment, and one-sentence examples.
2. **No invented scaffolding**: no invented owners, dates, paths, commands,
   metrics, acceptance criteria, or implementation claims.
3. **Claim-boundary safe wording**: limited evidence is not converted into MVP
   validation, Alpha superiority, plain-provider inferiority, production
   readiness, benchmark success, exact billing accuracy, broad runtime
   readiness, or provider orchestration.
4. **Evidence-boundary behavior**: examples preserve the distinction between
   A3-1 and Batch B and treat repo evidence as controlling over planning
   ledgers.
5. **Artifact stop-condition behavior**: missing score tables, missing capture
   packets, and unavailable raw provider payloads trigger stop-condition wording.
6. **Answer-structure mode examples**: direct answer, reviewer comment, safe
   rewrite, evidence-boundary answer, artifact stop-condition answer, and
   protocol checklist examples.

## 6. Future implementation path

A future lane may use these fixtures as the starting safety net for behavior
changes. Any future implementation must remain separately approved and should:

- Keep runtime/provider/model/routing changes out of this lane.
- Add targeted runtime tests before changing user-visible behavior.
- Preserve the non-claim language from this test plan.
- Confirm no live provider calls or secret-dependent checks are required.
- Reconfirm scored artifacts are not mutated.

## 7. Protected surfaces

This lane protects these surfaces from change:

- Runtime behavior and answer assembly paths.
- Provider, model, and routing behavior.
- `/v1/solve` behavior.
- SAFE-OUT, SolverEnvelope, budget guard, determinism, observability, and replay
  behavior.
- Scoring rubrics and scored artifacts.
- Capture artifacts and raw provider payload handling.
- Google Sheets integrations and backlog workbooks.
- Batch C planning or execution.

## 8. Non-claims

This plan makes strict non-claims:

- No MVP validation.
- No Alpha Solver superiority generally.
- No plain-provider inferiority generally.
- No answer-quality superiority generally.
- No production readiness.
- No broad runtime readiness.
- No benchmark success.
- No exact billing accuracy.
- No provider orchestration.
