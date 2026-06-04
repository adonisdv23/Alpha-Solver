# Forbidden Claim and Action Table

Lane ID: `ALPHA-OPERATOR-TEST-BATCH-C-RUNTIME-FIREWALL-001`

Status: forbidden claims and actions recorded for firewall use.

| Trigger or evidence | Forbidden claim | Forbidden action | Required safe framing |
|---|---|---|---|
| Limited operator-test packet exists | “User testing completed.” | Treat packet preparation as evidence of validation. | Packet preparation is not user testing. |
| Limited operator-test packet exists | “Batch C ready.” | Start Batch C or create Batch C prompts. | Batch C requires a separate readiness decision. |
| Operator feedback is later collected | “Batch C readiness proven.” | Skip readiness review and begin Batch C. | Limited operator-test feedback is not Batch C readiness. |
| Operator feedback is later collected | “MVP validated.” | Publish validation or launch-readiness claims. | Operator feedback may identify usability defects only. |
| Operator feedback is later collected | “Production-ready.” | Start production-readiness documentation. | Interpretation is not production readiness. |
| Operator feedback is later collected | “Runtime-ready.” | Begin runtime wiring or model-routing changes. | Runtime work requires separate wiring/readiness review. |
| Operator result templates are later imported | “Validation complete.” | Treat preservation import as scoring, validation, or benchmark success. | Results import is not validation. |
| Operator result templates are later imported | “Scoring completed.” | Create scores, rescoring, or benchmark totals without an approved scoring lane. | Importing records preserves records only. |
| Future interpretation summarizes feedback | “Public launch ready.” | Expand into public-launch, MVP, or production claims. | Interpretation may remain limited to operator feedback only. |
| Future interpretation identifies positive feedback | “Alpha is broadly superior.” | Generalize beyond the limited portable-surface evidence. | Feedback is prompt/operator/surface limited. |
| Future interpretation identifies few defects | “Provider orchestration works.” | Enable or claim provider orchestration. | Provider orchestration remains blocked. |
| Future interpretation identifies few defects | “Exact billing proven.” | Claim billing accuracy or reconcile live costs. | Exact billing remains blocked. |
| Future interpretation identifies few defects | “`/v1/solve` works.” | Claim runtime API behavior or use `/v1/solve` as validated. | `/v1/solve` remains unproven unless separately measured. |
| Post-improvement scored result remains positive | “Batch C should start automatically.” | Treat prior portable-surface score as Batch C authorization. | Prior scored evidence was limited and did not authorize Batch C. |
| Brevity refinement is complete | “Runtime behavior improved.” | Claim runtime, provider, routing, or `/v1/solve` changes. | Brevity refinement changed portable contract wording only. |

## Always forbidden in this lane

- Importing or fabricating results.
- Starting Batch C.
- Creating Batch C prompts.
- Calling providers.
- Using `/v1/solve`.
- Modifying runtime APIs, provider adapters, model routing, billing, budget guard, SAFE-OUT, SolverEnvelope, replay, observability, or determinism behavior.
- Updating Google Sheets or external status ledgers.
- Modifying scored artifacts, raw outputs, sanitized scorer-facing packets, or operator-only maps.
