# Claim Boundary

Lane ID: `ALPHA-SOLVER-DISCRIMINATION-LAYER-DEMO-PACK-001`

Verdict: `DEMO_PACK_CAPTURED_NOT_EXECUTED`

## Evidence status

This packet is a docs-only demo-design artifact. It defines intended scenarios, ideal behavior, common baseline failure modes, presenter copy, and next-lane requirements.

It does not include executed prompts, captured outputs, scoring, adjudication, provider traces, runtime logs, statistical analysis, or operator validation.

## Permitted claims

- The packet defines a discrimination-layer demo thesis.
- The packet contains 10 illustrative scenarios.
- The packet identifies intended Alpha behavior and common baseline failure modes as hypotheses for a future demo or eval.
- The packet marks every scenario as illustrative until executed.
- The packet recommends a controlled execution/scoring next lane.

## Required disclaimers

Use one of these disclaimers in any handoff, slide, or demo narration:

- "This demo pack is illustrative and has not been executed or scored."
- "These scenarios are not proof of Alpha Solver performance."
- "Any performance, superiority, or benchmark claim would require a separate executed and scored run."

## Non-claims

This packet does not show that Alpha Solver:

- outperforms a baseline;
- is safer than generic LLMs;
- always detects ambiguity, false premises, hidden constraints, unsafe requests, bad objectives, or high-stakes uncertainty;
- is production-ready;
- is validated for customer, medical, legal, financial, security, or operational use;
- has executed these scenarios through `/v1/solve`, local models, or providers.

## Evidence needed for stronger claims

Before making stronger claims, create and complete a separate run lane with:

1. Frozen prompt set and scenario IDs.
2. Authorized execution environment.
3. No private user data or secrets.
4. Provider or local-model authorization if used.
5. Captured Alpha and baseline outputs.
6. Predefined scoring rubric.
7. Blind or independent review where practical.
8. Preserved artifacts and run metadata.
9. Explicit claim review before external use.
