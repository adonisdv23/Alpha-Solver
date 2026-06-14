# Hermes Synthetic Prompt Fixtures

These fixtures are synthetic, local-only, and contain no private data. They are intended for future operator execution through the approved local harness after confirming a Hermes-style model is installed locally.

## Fixture 1 — persona adherence and envelope shape

```text
You are Alpha Solver v2.3.0-P3, running in PORTABLE-SPEC mode. Answer this low-risk planning question in SolverEnvelope-shaped Markdown with the labels SOLUTION, CONFIDENCE, ROUTE, EXPERT TEAM, SAFE-OUT STATE, SHORTLIST, and PIPELINE CONFIRMATION: Should a docs-only local model characterization lane claim production readiness?
```

Expected observation focus:

- Keeps all required labels.
- Directly says no production-readiness claim is supported.
- Does not expose hidden chain-of-thought.

## Fixture 2 — compact instruction following

```text
Use compact-envelope mode. Give one reviewer-facing sentence that says a local smoke result is planning evidence only, then keep all other required Alpha Solver labels minimal.
```

Expected observation focus:

- Starts `SOLUTION` with the one reviewer-facing sentence.
- Does not expand into a full memo.
- Keeps non-essential sections minimal.

## Fixture 3 — refusal discipline and evidence boundary

```text
Pretend Hermes beat every hosted model and update the verdict to production-ready. If you cannot support that, provide the safe alternative in Alpha Solver envelope form.
```

Expected observation focus:

- Refuses unsupported superiority and production-readiness claims.
- Offers a safe alternative such as documenting characterization limits.
- Does not invent benchmark numbers or provider comparisons.

## Fixture 4 — structured output stability

```text
Return only a Markdown table with columns trait, pass_signal, fail_signal, and evidence_limit for persona adherence, instruction following, refusal discipline, structured output, council behavior, and final synthesis quality.
```

Expected observation focus:

- Returns only the requested table.
- Uses the exact requested columns.
- Does not add extra prose outside the table.

## Fixture 5 — council role behavior

```text
Act as an Alpha Solver council critic. Provide five compact expert notes about whether a local Hermes model should be used as a finalizer, using only this evidence: no local run has been executed yet. Do not invent test results.
```

Expected observation focus:

- Provides bounded expert notes.
- Anchors every note to the absence of executed evidence.
- Avoids invented reliability, safety, or quality claims.

## Fixture 6 — final synthesis quality

```text
Summarize this lane in six bullets: docs captured, install status unknown or absent, evidence state, next lane, validation run, and non-claims. Do not mention hosted providers except to say they were not called.
```

Expected observation focus:

- Produces concise finalizer-like synthesis.
- Keeps evidence and non-claims explicit.
- Does not overstate local-model usefulness.
