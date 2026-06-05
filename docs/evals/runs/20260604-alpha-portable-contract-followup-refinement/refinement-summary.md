# Refinement Summary

Lane ID: `ALPHA-PORTABLE-CONTRACT-FOLLOWUP-REFINEMENT-001`

## Targeted problem

The interpreted operator feedback identified a recurring narrow defect family: otherwise usable manual prompt-contract simulation answers sometimes carried extra visible formatting around the requested answer.

The target defects were:

- process-style lead-in text before the answer;
- wrapper labels around content that should have been directly usable;
- accidental `standard:` artifacts;
- answer-shape mismatch on concise reviewer-comment, rewrite, template, and checklist requests.

## Contract refinement made

`alpha_solver_portable.py` now explicitly instructs the portable prompt contract to:

- start low-headroom `SOLUTION` content with the requested artifact itself;
- suppress process-style lead-ins before concise answers;
- suppress wrapper labels unless the user asks for a literal wrapper;
- suppress accidental `standard:` labels unless explicitly requested;
- avoid unnecessary memo framing for reviewer comments, replacement wording, checklists, two-sentence status updates, and compact prompt/template tasks;
- preserve compact caveats only when needed for evidence, safety, uncertainty, or claim boundaries.

## Preservation

The refinement keeps the existing portable-envelope protocol intact. It preserves the required SolverEnvelope labels, route/confidence/SAFE-OUT expectations, expert-roster availability, shortlist behavior, artifact stop conditions, evidence-boundary wording, claim-boundary restrictions, and Batch C blocking when evidence is limited.

## Non-actions

This lane did not change runtime/provider/model/routing behavior, `/v1/solve`, local adapters, provider calls, capture, scoring, rescoring, unblinding, Google Sheets, imported operator ratings, mechanical totals, source evidence, interpretation docs, or post-results decision docs.
