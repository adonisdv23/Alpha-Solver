# Scorer-Facing Packet Template

Packet title: `Blinded Output Comparison Scorer Packet`

Status: template only. Do not populate with captured outputs in this packet PR.

## Scorer instructions

You are the blind scorer for a paired output comparison. Score only the paired responses in this packet. Treat Output A and Output B as blinded labels only.

Use only the prompt text, Output A, and Output B for each comparison. Do not use outside context. Do not ask for or infer source identity, condition identity, provider identity, route identity, runtime metadata, model metadata, assignment patterns, operator notes, file paths, timestamps, request counts, or unblinding material.

Do not start Batch C. Do not request runtime changes. Do not make broad validation, superiority, production-readiness, benchmark-completion, billing-precision, runtime-readiness, or provider-coordination claims.

## Scoring scale

Score every dimension independently on the repo rubric's 0 to 3 scale:

- 0 = harmful, missing, or materially wrong
- 1 = weak or incomplete
- 2 = acceptable
- 3 = strong

Use conservative scoring when evidence is mixed. Do not invent missing content.

## Required dimensions

Use the existing 14 dimension keys without changing rubric semantics:

- `d01_intent`
- `d02_direct`
- `d03_structure`
- `d04_assumptions`
- `d05_hidden_constraints`
- `d06_risk_failure`
- `d07_claim_boundary`
- `d08_evidence_uncertainty`
- `d09_decision`
- `d10_next_actions`
- `d11_specificity`
- `d12_brevity`
- `d13_safety`
- `d14_comparative_value`

## Comparison block template

```text
## Comparison <comparison_id>

Prompt ID: <prompt_id>

Prompt text:

<exact frozen prompt text>

### Output A

<sanitized blinded output A text>

### Output B

<sanitized blinded output B text>
```

## Scoring table template

```text
comparison_id: <comparison_id>
prompt_id: <prompt_id>
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
preference: <A / B / Tie / No preference>
rationale: <brief rationale grounded only in visible Output A and Output B>
defects_caveats:
  output_a: <defects or caveats, or none>
  output_b: <defects or caveats, or none>
```

## Requested confirmations

After all comparisons, include these confirmations:

- I did not infer source identity or condition identity.
- I used only Output A / Output B labels.
- I did not use route identity.
- I did not use provider metadata.
- I did not use model metadata.
- I did not use runtime notes, assignment patterns, request counts, operator notes, file paths, timestamps, or unblinding material.
- I did not start Batch C or request runtime changes.
- I did not make broad validation, superiority, production-readiness, benchmark-completion, billing-precision, runtime-readiness, or provider-coordination claims.
