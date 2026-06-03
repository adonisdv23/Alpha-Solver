# Batch B Post-Capture Scoring Workflow

## 1. Title and status

This document is a post-capture workflow package for Batch B in `OUTPUT-DIFFERENTIATION-PHASE-001`.

It is not a capture result, not a scoring result, and not artifact population. It does not execute Batch B, does not rerun capture, does not score outputs, does not unblind outputs, and does not create or populate a future run directory.

Use this workflow only after a clean Batch B capture returns. Until then, this file is an operator-facing procedure for downstream handling only.

## 2. Preconditions

Begin this workflow only after one Batch B live capture task completes and returns either the complete post-capture package or the explicit incomplete-capture stop marker.

A complete capture package must include all of the following capture-result sections:

- `BLINDED SCORING BUNDLE - SAFE TO SEND TO BLIND SCORER`
- `OPERATOR-ONLY UNBLINDING MATERIAL - DO NOT SEND TO BLIND SCORER`
- `PROMPT FOR BLIND SCORER`

An incomplete capture may instead return:

- `BATCH B CAPTURE INCOMPLETE - DO NOT SCORE`

If capture is incomplete, stop immediately. Do not score, do not unblind, do not populate artifacts, and do not attempt to repair the capture by making live provider calls from this workflow.

## 3. Capture result triage

Use this decision tree before any scorer-facing material is sent:

1. **Capture incomplete**
   - Do not score.
   - Do not unblind.
   - Preserve the failure summary exactly as returned.
   - Diagnose the blocker separately in a follow-up task that is explicitly scoped for capture diagnostics.
2. **Capture complete**
   - Validate the blinded bundle against the checklist in Section 4 before sending anything to a scorer.
   - Keep operator-only material separate from scorer-facing material.
3. **Route leak exists**
   - Do not score.
   - Create a cleanup or failure note that identifies the leaked field, location, and remediation needed.
   - Do not infer scores from leaked material.
4. **Outputs are missing**
   - Do not score.
   - Record which comparison ID, side, or prompt output is missing.
   - Return to capture diagnostics rather than filling gaps manually.
5. **Operator-only material is mixed into the scorer-facing bundle**
   - Do not score.
   - Treat the bundle as contaminated.
   - Preserve the issue and request a regenerated blinded scorer package from clean source material.

## 4. Blinded bundle validation checklist

The blinded bundle must contain exactly the approved Batch B pilot comparison IDs from the pilot run plan:

- `cmp-B1-CAND-001`
- `cmp-B1-CAND-003`
- `cmp-B1-CAND-005`
- `cmp-B1-CAND-007`
- `cmp-B1-CAND-009`
- `cmp-B1-CAND-011`
- `cmp-B1-CAND-013`
- `cmp-B1-CAND-015`
- `cmp-B1-CAND-017`
- `cmp-B1-CAND-020`
- `cmp-B1-CAND-021`
- `cmp-B1-CAND-022`

For each comparison, require all of the following:

- comparison ID;
- candidate ID;
- prompt text;
- Output A;
- Output B.

Confirm the blinded bundle does not include any of the following:

- plain labels;
- Alpha labels;
- route labels;
- expert labels;
- provider execution notes;
- model metadata;
- provider request count per output;
- assignment table;
- unblinding map;
- operator-only notes;
- score fields;
- interpretation;
- superiority or validation claims.

If any required comparison is missing, any extra comparison appears, or any disallowed material appears, stop and do not send the bundle to the blind scorer.

## 5. Blind scorer prompt template

Copy and paste the following prompt only after the blinded bundle passes Section 4 validation.

```text
You are the official blind scorer for the Alpha Solver Batch B pilot.

Scope and blinding rules:
- Score only the visible Output A and Output B for each comparison.
- Do not infer which output is Alpha, Plain, expert, routed, or provider-direct.
- Do not use route identity, provider metadata, model metadata, execution notes, request counts, assignment tables, unblinding maps, or operator-only notes.
- Use only the prompt text and the visible Output A / Output B content.
- Do not start Batch C, change runtime behavior, change model configuration, change provider behavior, change routing, or request live provider calls.

Scoring scale:
- Score every dimension independently on the repo rubric's 0 to 3 scale:
  - 0 = harmful, missing, or materially wrong
  - 1 = weak or incomplete
  - 2 = acceptable
  - 3 = strong
- Use conservative scoring when evidence is mixed.
- Do not invent missing content.

Required 14 dimension keys:
- d01_intent
- d02_direct
- d03_structure
- d04_assumptions
- d05_hidden_constraints
- d06_risk_failure
- d07_claim_boundary
- d08_evidence_uncertainty
- d09_decision
- d10_next_actions
- d11_specificity
- d12_brevity
- d13_safety
- d14_comparative_value

For each comparison, return this structure:

comparison_id: <comparison ID>
candidate_id: <candidate ID>
output_a_scores:
  d01_intent: <0-3>
  d02_direct: <0-3>
  d03_structure: <0-3>
  d04_assumptions: <0-3>
  d05_hidden_constraints: <0-3>
  d06_risk_failure: <0-3>
  d07_claim_boundary: <0-3>
  d08_evidence_uncertainty: <0-3>
  d09_decision: <0-3>
  d10_next_actions: <0-3>
  d11_specificity: <0-3>
  d12_brevity: <0-3>
  d13_safety: <0-3>
  d14_comparative_value: <0-3>
output_b_scores:
  d01_intent: <0-3>
  d02_direct: <0-3>
  d03_structure: <0-3>
  d04_assumptions: <0-3>
  d05_hidden_constraints: <0-3>
  d06_risk_failure: <0-3>
  d07_claim_boundary: <0-3>
  d08_evidence_uncertainty: <0-3>
  d09_decision: <0-3>
  d10_next_actions: <0-3>
  d11_specificity: <0-3>
  d12_brevity: <0-3>
  d13_safety: <0-3>
  d14_comparative_value: <0-3>
output_a_total: <sum of Output A dimensions>
output_b_total: <sum of Output B dimensions>
preference: <A / B / Tie>
rationale: <brief rationale grounded only in visible Output A and Output B>
defects_caveats:
  output_a: <defects or caveats, or none>
  output_b: <defects or caveats, or none>

After all comparisons, include these scorer confirmations exactly:
- I did not infer Alpha identity.
- I used only Output A / Output B labels.
- I did not use route identity.
- I did not use provider metadata.
- I did not start Batch C or any runtime changes.
```

## 6. Scorer result validation checklist

After the scorer returns results, validate all of the following before unblinding:

- all 12 approved comparisons are present;
- Output A and Output B each have all 14 dimensions for every comparison;
- all scores are within the rubric range;
- totals are recomputed from dimensions;
- scorer-stated totals match recomputed totals, or every mismatch is recorded without changing the original scorer text;
- scorer confirmations are present;
- no route identity was used;
- no provider metadata was used;
- no unblinding occurred before scoring.

If any item fails, stop and preserve the scorer result plus the validation failure. Do not unblind from an invalid or incomplete scorer result.

## 7. Operator approval to unblind

The operator must provide approval using this wording before the unblinding map is used:

```text
Blind scoring is complete.
Official 14-dimension scorer result is preserved.
Route-leak validation passed.
Operator approves unblinding using the operator-only map.
```

The unblinding map must not be opened, applied, summarized, or used before this approval is present and preserved with the source packet.

## 8. Unblinding and math verification protocol

After Section 7 approval, apply the operator-only map as follows:

1. Map Output A / Output B to Plain / Alpha for each comparison.
2. Recompute `plain_total` and `alpha_total` per comparison from the 14 dimension scores.
3. Compute `total_delta = alpha_total - plain_total`.
4. Compute `lift_subscore_plain` from the lift dimensions defined by the existing reporting hardening contract.
5. Compute `lift_subscore_alpha` from the same lift dimensions.
6. Compute `lift_delta = lift_subscore_alpha - lift_subscore_plain`.
7. Compute `polish_subscore_plain` from the polish dimensions defined by the existing reporting hardening contract.
8. Compute `polish_subscore_alpha` from the same polish dimensions.
9. Compute `polish_delta = polish_subscore_alpha - polish_subscore_plain`.
10. Compute `length_ratio` only from preserved Output A / Output B word-count evidence, mapped to the unblinded surfaces.
11. Assign `length_confound_flag` conservatively if evidence supports length as a confound; do not assign it optimistically.
12. Compute `winning_surface` from the unblinded total comparison.
13. Compute `winning_surface_resolved` after applying tie handling and guardrails required by the reporting templates.
14. Apply the polish-only guard before treating any total delta as meaningful lift.
15. Record `lift_qualified` conservatively.
16. Record `material_constraint_verified` conservatively from visible scorer evidence and preserved capture artifacts.

Do not infer missing data. Token fields may be recorded as `not-captured` if token data is absent. Preserve original scorer totals separately from corrected computed totals if they differ.

## 9. Source packet for artifact population

A later artifact-population Codex task must receive a complete source packet. Use this template:

```text
SOURCE PACKET - BATCH B POST-CAPTURE ARTIFACT POPULATION
1. Run ID:
2. Capture commit SHA:
3. Capture started timestamp, if available:
4. Capture completed timestamp, if available:
5. Selected comparison IDs:
   - cmp-B1-CAND-001
   - cmp-B1-CAND-003
   - cmp-B1-CAND-005
   - cmp-B1-CAND-007
   - cmp-B1-CAND-009
   - cmp-B1-CAND-011
   - cmp-B1-CAND-013
   - cmp-B1-CAND-015
   - cmp-B1-CAND-017
   - cmp-B1-CAND-020
   - cmp-B1-CAND-021
   - cmp-B1-CAND-022
6. Completed blinded bundle:
7. Official blind scorer result:
8. Scorer confirmations:
9. Operator-only unblinding map:
10. Operator approval to unblind:
11. Corrected computed totals:
12. Route-leak validation result:
13. Redaction notes:
14. Non-claims:
15. Operator approval to populate artifacts:
SOURCE PACKET COMPLETE: <yes/no>
```

No artifact-population task may run from summaries alone. Do not use placeholders if the source data is already available. If the source packet is too large for one message, use staged chunks with stable labels and a clear `SOURCE PACKET COMPLETE: yes` marker after the final chunk. Codex must not proceed without the complete source packet.

## 10. Artifact-population readiness checklist

A later artifact-population task should not start until all of the following are true:

- complete capture exists;
- blind scoring is complete;
- unblinding is approved;
- source packet is complete;
- score math is verified;
- route-leak validation passed;
- artifact path and run ID are approved;
- redaction boundaries are confirmed;
- no runtime, model, provider, routing, or scoring-rubric changes are needed.

## 11. Stop conditions

Stop without scoring, unblinding, or populating artifacts if any of the following occurs:

- capture incomplete;
- missing prompt output;
- route leak;
- operator-only material included in the scorer-facing bundle;
- missing 14-dimension scores;
- scorer refuses or gives a winner-only result;
- score totals cannot be recomputed;
- unblinding occurred too early;
- raw provider payloads or secrets would be committed;
- source packet incomplete;
- artifact task would require runtime, provider, model, or scoring-rubric changes;
- any broad superiority or validation claim appears.

## 12. Credit/API usage guidance

- Post-capture validation does not need OPENAI_API_KEY.
- Blind scoring does not need repo provider calls.
- Artifact population does not need live providers.
- API key material should only be present in explicit capture or diagnostic tasks that are separately approved and scoped.
- Do not run extra provider calls to improve answer quality.

## 13. Non-claims

This workflow package makes and permits none of the following claims:

- no MVP validation;
- no Alpha Solver superiority;
- no broad plain-provider superiority;
- no answer-quality superiority;
- no production readiness;
- no broad runtime readiness;
- no benchmark success;
- no exact billing accuracy;
- no provider reasoning orchestration.

## 14. Recommended operator workflow after capture returns

1. Send the capture result for blinded-bundle validation.
2. If the bundle is safe, send the blinded bundle to the official scorer.
3. Preserve the scorer result immediately after it returns.
4. Approve unblinding only after scorer-result validation and route-leak validation pass.
5. Compute scores using the operator-only unblinding map and the math verification protocol.
6. Create one artifact-population PR from the complete source packet.
7. Complete Sheet bookkeeping after the artifact-population PR merges.
