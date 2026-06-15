# Operator Run Template for a Future Authorized Simulation

Do not complete this template unless a later lane explicitly authorizes simulation execution. This packet does not authorize answer generation, provider calls, hosted model calls, local model calls, token use, scoring, unblinding, dashboard exposure, `/v1/solve` exposure, public API exposure, credential access, or Google Sheets mutation.

## Pre-run freeze

- Run ID:
- Lane ID:
- Date:
- Operator:
- Reviewer roster:
- Commit SHA:
- Packet path:
- Selected case IDs:
- Rubric version:
- Scoring scale:
- Stop conditions:
- Raw-output preservation path:
- Redaction rules:
- Blinding-map storage path:
- Statement: provider/runtime/local-model execution authorized? `no`
- Statement: external ledger mutation authorized? `no`

## Per-case prompt shell

```yaml
case_id:
source_case:
primary_category:
secondary_categories:
user_task:
answerability_fields_required:
  answerability_verdict:
  confidence_level:
  confidence_reason:
  assumptions_detected:
  missing_evidence:
  false_premise_flag:
  hidden_constraint_flag:
  needs_human:
  escalation_reason:
  will_not_claim:
  would_change_if:
  next_safe_operator_action:
blocked_claims:
stop_conditions:
```

## Output preservation

For each generated output in a later authorized run, preserve raw output before editing, scoring, summarizing, or interpreting. Keep operator notes separate from raw output. If private data, secrets, credentials, provider account details, or unsupported live-execution metadata appear, stop and preserve only a safe redaction log.

## Blind-before-unblind sequence

1. Freeze cases, rubric, answerability fields, stop conditions, evidence boundary, and artifact paths.
2. Generate or collect only the separately authorized simulation outputs.
3. Preserve raw outputs.
4. Create scorer-facing Output A / Output B packets with source identity removed.
5. Confirm scorer-facing packet contains no unblinding map, route identity, model identity, desired winner, prior score totals, or source labels.
6. Score independently against the frozen rubric.
7. Lock blind scores with reviewer and timestamp.
8. Only after score lock, use the operator-only map to unblind.
9. Interpret narrowly as simulation-only and preserve non-claims.

## Stop immediately if

- authorization is missing or ambiguous;
- a provider, hosted model, local model, endpoint, dashboard, public API, credential, token, or Google Sheet would be used;
- scorer sees unblinded identity before score lock;
- raw output is missing or materially altered;
- output asks to fabricate evidence;
- evidence conflicts cannot be reconciled but the summary would need a resolved claim;
- claim-safety lint would fail and cannot be rewritten within packet-scoped boundaries.
