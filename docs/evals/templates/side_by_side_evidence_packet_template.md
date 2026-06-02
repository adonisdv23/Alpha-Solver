# Side-by-Side Evidence Packet Template

This packet is a blank, placeholder-only **review/index/interpretation artifact**
for a single future Alpha-vs-plain comparison. It references and interprets the
source artifacts listed below; it does not replace the score table,
paired-output capture, blinded score sheet, blinding map, or run report.

Use with:

- `docs/evals/templates/paired_output_capture_template.md`
- `docs/evals/templates/blinded_score_sheet_template.csv`
- `docs/evals/templates/blinding_map_template.csv`
- `docs/evals/templates/comparison_score_table_template.csv`
- `docs/evals/templates/run_report_template.md`
- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/LIFT_DECISION_RULE.md`
- `docs/evals/BLIND_SCORING_PROCEDURE.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`

## 1. Packet identity

| Field | Placeholder |
| --- | --- |
| `packet_id` | `TBD` |
| `comparison_id` | `TBD` |
| `parent_run_id` | `TBD` |
| `run_directory` | `docs/evals/runs/TBD/` |
| `prompt_id` | `TBD` |
| `prompt_family` | `TBD` |
| `difficulty_headroom` | `TBD` |
| `evidence_strength` | `TBD` |
| `non_claims_confirmed` | `TBD` |

## 2. Source artifact references

| Source artifact | Path |
| --- | --- |
| `blinded_score_sheet path` | `TBD` |
| `blinding_map path` | `TBD` |
| `paired_output_capture path` | `TBD` |
| `comparison_score_table path` | `TBD` |
| `run_report path` | `TBD` |

Storage boundary: this packet indexes sanitized artifacts already preserved under
`docs/evals/runs/`. Do not paste any of the following here:

- raw provider payloads;
- provider account identifiers;
- private user data;
- full unredacted request/response traces;
- environment dumps;
- dashboard credentials;
- cookies;
- CSRF tokens;
- session values;
- credential strings;
- authorization-token material.

## 3. Prompt under review

- `prompt_id`: `TBD`
- `prompt_family`: `TBD`
- `difficulty_headroom`: `TBD`
- Prompt summary: `TBD sanitized summary only`
- Expected deliverable: `TBD`
- Material constraints to verify: `TBD`

## 4. Output capture summary

- `paired_output_capture path`: `TBD`
- Output A sanitized summary: `TBD`
- Output B sanitized summary: `TBD`
- `length_ratio`: `TBD`
- Length-control notes: `TBD`

## 5. Blinded scoring record

- `blinded_score_sheet path`: `TBD`
- Blinded scoring completed before unblinding: `TBD yes/no`
- Reviewer: `TBD`
- Rubric reference: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- Procedure reference: `docs/evals/BLIND_SCORING_PROCEDURE.md`

## 6. Unblinding record

- `blinding_map path`: `TBD`
- Unblinded by: `TBD`
- Unblinded at: `TBD`
- Plain surface after unblinding: `TBD Output A or Output B`
- Alpha surface after unblinding: `TBD Output A or Output B`
- Mapping notes: `TBD`

## 7. Fourteen-dimension scores

Copy score values from `comparison_score_table path`; do not rescore in this
packet.

| Dimension key | Plain score | Alpha score | Delta | Evidence note |
| --- | --- | --- | --- | --- |
| `d01_intent` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d02_direct` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d03_structure` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d04_assumptions` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d05_hidden_constraints` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d06_risk_failure` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d07_claim_boundary` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d08_evidence_uncertainty` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d09_decision` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d10_next_actions` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d11_specificity` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d12_brevity` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d13_safety` | `TBD` | `TBD` | `TBD` | `TBD` |
| `d14_comparative_value` | `TBD` | `TBD` | `TBD` | `TBD` |

## 8. Lift / polish / total decision aid

Use `docs/evals/LIFT_DECISION_RULE.md`; treat these fields as internal review
decision aids, not broad claims.

| Field | Placeholder |
| --- | --- |
| `plain_total` | `TBD` |
| `alpha_total` | `TBD` |
| `total_delta` | `TBD` |
| `lift_delta` | `TBD` |
| `polish_delta` | `TBD` |
| `winning_surface` | `TBD` |
| `lift_qualified` | `TBD` |
| `material_constraint_verified` | `TBD` |
| `polish_only_flag` | `TBD` |
| `length_ratio` | `TBD` |

## 9. Expert-envelope evidence

Use only sanitized envelope fields from `paired_output_capture path` after
unblinding.

- `considerations`: `TBD`
- `assumptions`: `TBD`
- `material/correct tags`: `TBD`
- `confidence`: `TBD`
- `mode`: `TBD`
- `clarifying questions`: `TBD`
- `sanitized metadata`: `TBD`

## 10. Material constraints, assumptions, and risks

- Material constraints verified: `TBD`
- Assumptions accepted: `TBD`
- Assumptions rejected or unsupported: `TBD`
- Risk and failure-mode notes: `TBD`
- Constraint misses: `TBD`

## 11. Defects, regressions, and over-interrogation

- Plain defects: `TBD`
- Alpha defects: `TBD`
- Regression status: `TBD`
- Over-interrogation observed: `TBD yes/no`
- `over-interrogation defect category`:
  `TBD none / unnecessary clarification / excessive caveats / delayed answer / other`
- Defect evidence references: `TBD`

## 12. Evidence-limited explanation

State only what the referenced artifacts support. Do not infer hidden runtime
behavior, model quality in general, provider reasoning orchestration, or product
readiness from this packet.

- Evidence-limited explanation: `TBD`

## 13. Conservative interpretation

- Outcome label:
  `TBD Alpha local advantage / Plain local advantage / Tie / Inconclusive / Regression flagged / Expected change`
- Conservative interpretation: `TBD`
- Reasons the evidence may be incomplete: `TBD`

## 14. Redactions performed

- `redactions performed`: `TBD`
- Sanitization reviewer: `TBD`
- Storage boundary confirmed: `TBD yes/no`
- Omitted unsafe material: `TBD`

## 15. Follow-up tickets

| Ticket/spec | Reason | Owner/status |
| --- | --- | --- |
| `TBD` | `TBD` | `TBD` |

## 16. Non-claims

This packet does not claim:

- MVP validation;
- Alpha Solver superiority;
- answer-quality superiority;
- production readiness;
- broad runtime readiness;
- benchmark success;
- exact billing accuracy;
- provider reasoning orchestration.

`non_claims_confirmed`: `TBD`
