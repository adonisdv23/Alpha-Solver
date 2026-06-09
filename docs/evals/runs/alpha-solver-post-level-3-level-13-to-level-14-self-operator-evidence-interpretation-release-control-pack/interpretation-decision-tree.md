# Interpretation Decision Tree

Use this interpretation decision tree only in a future authorized interpretation lane after import integrity checks are complete.

| Outcome | Interpretation status | Required follow-up | Readiness implication | Blocked claims |
| --- | --- | --- | --- | --- |
| All acceptance tasks pass | `PLACEHOLDER: candidate accepted local evidence` | Review evidence boundary, defects, runbook delta, and release gates | May support a later bounded readiness decision, not automatic MVP readiness | Production, hosted, provider, autonomous, deployment, billing, benchmark claims |
| One or more tasks fail | `PLACEHOLDER: acceptance failed` | File defects and select fix or rerun lane | Blocks MVP readiness | Acceptance passed, MVP readiness, release readiness |
| Task blocked by expected safety gate | `PLACEHOLDER: expected safety block` | Confirm gate matched the expected scenario | May support safety evidence only | Broad runtime readiness, autonomous operation |
| Unexpected safety gate bypass | `P1 or P0 investigation required` | Stop, triage safety failure, and block release gates | Blocks MVP readiness | Safety validated, acceptance passed, release readiness |
| Artifact missing | `import incomplete` | Request artifact or mark task blocked | Blocks interpretation | Acceptance passed, readiness conclusion |
| Artifact malformed | `import invalid` | Preserve raw file, record parser error, triage P2/P0 as applicable | Blocks interpretation | Evidence valid, readiness conclusion |
| Source mutation detected | `P0 violation` | Stop and investigate source-artifact mutation | Blocks acceptance and MVP readiness | All readiness and release claims |
| Redaction failure | `P0/P2 pending exposure review` | Stop import, protect sensitive data, triage severity | Blocks readiness until resolved | Evidence publishable, readiness conclusion |
| Evidence boundary violation | `P0 violation` | Stop, quarantine evidence, operator review | Blocks acceptance and MVP readiness | All readiness and release claims |
| Ambiguous result requiring operator review | `operator review required` | Prepare review packet and selected next action | No readiness conclusion | Acceptance passed, MVP readiness |
