# Preservation Checklist

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Status: packet prepared, second-pass test not yet executed

## Prior evidence preservation

- [ ] Do not modify PR #288 evidence docs.
- [ ] Do not modify PR #289 evidence docs.
- [ ] Do not modify PR #292 evidence docs.
- [ ] Do not modify PR #293 evidence docs.
- [ ] Do not modify PR #294 refinement docs.
- [ ] Do not modify imported first-pass operator feedback.
- [ ] Do not modify first-pass mechanical result logs or rating totals.
- [ ] Do not modify first-pass interpretation docs.
- [ ] Do not modify post-results decision docs.

## Raw artifact preservation for later execution

If a separate execution lane is authorized:

- [ ] Preserve exact prompt text submitted for each task.
- [ ] Preserve raw output exactly as returned for each task.
- [ ] Preserve visible process-style lead-ins if present.
- [ ] Preserve wrapper labels if present.
- [ ] Preserve `standard:` artifacts if present.
- [ ] Preserve unnecessary `Replacement:` labels if present.
- [ ] Preserve memo framing if present.
- [ ] Preserve refusal or stop-condition text if present.
- [ ] Preserve timestamps and operator identifiers according to the execution lane's handling rules.

## Template preservation

- [ ] Keep `operator-feedback-form-template.md` blank in this preparation packet.
- [ ] Keep `operator-result-log-template.md` blank in this preparation packet.
- [ ] Keep stop-condition fields present for every task.
- [ ] Keep the first-pass rating dimensions unchanged in naming and meaning.

## Non-action preservation

- [ ] Do not run the second-pass test in this preparation packet.
- [ ] Do not score, rescore, adjudicate, or unblind.
- [ ] Do not import results.
- [ ] Do not update Google Sheets.
- [ ] Do not start Batch C.
- [ ] Do not use `/v1/solve`.
- [ ] Do not call providers.
- [ ] Do not call local models.
- [ ] Do not make readiness, validation, superiority, benchmark, MVP, runtime, provider, local-model, or production claims.
