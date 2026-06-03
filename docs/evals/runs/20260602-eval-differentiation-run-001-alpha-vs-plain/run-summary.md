# 20260602-eval-differentiation-run-001-alpha-vs-plain · Eval Run Report

## Run metadata

- Run ID: `20260602-eval-differentiation-run-001-alpha-vs-plain`
- Date: 2026-06-03 artifact population from completed A3-1 source packets
- Operator: operator-approved source packet; artifact population by Codex
- Branch/commit: `output-diff-a3-first-scored-run-artifact-001` / recorded in PR commit
- Provider/mode: clean capture completed before scoring; no provider calls were made during artifact population
- Prompt set: higher-headroom prompt set pilot subset
- Prompt count: 4 completed comparisons (`HHE-002`, `HHE-003`, `HHE-007`, `HHE-009`)
- Live mode used: capture completed before this artifact population; not rerun here
- Request cap used: 8 outputs captured before scoring, per operator packet
- Rollback confirmed: not applicable; no runtime or provider behavior changed
- Blinding performed: yes; blind scorer used Output A / Output B labels only
- Output A/B mapping file: `blinding-map.csv`

## Execution status

A clean A3-1 capture had already completed with all 8 outputs for the four listed prompts before this artifact-population pass. This pass did not rerun capture, did not call live providers, did not rescore outputs, did not change runtime/provider/model behavior, did not update Google Sheets, and did not start Batch B.

Blind scoring preceded unblinding. Source Packet B is the official blind scorer result because it includes all 14 rubric dimensions, preferences, rationales, and defects/caveats. The operator-approved unblinding map was applied only after scoring was complete.

## Plain output summary

Plain won all four local comparisons after applying the approved unblinding map. The aggregate plain total is 237 across the four prompts. This is a limited run result only, not broad plain-provider superiority.

## Alpha output summary

Alpha did not win any of the four local comparisons after applying the approved unblinding map. The aggregate Alpha total is 228, for an Alpha-minus-plain aggregate delta of -9. This does not prove Alpha is worse generally and does not support broad product-readiness conclusions.

## Rubric used

- Rubric reference: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- Scoring procedure: `docs/evals/BLIND_SCORING_PROCEDURE.md`
- Lift decision rule: `docs/evals/LIFT_DECISION_RULE.md`
- Scoring dimensions: all 14 dimensions were present for Output A and Output B for all four comparisons
- Arithmetic rule: totals were recomputed from the 14 official dimension scores; inconsistent written scorer total lines were not copied

## Score table

Use `score-table.csv` for the full 14-dimension per-output scores. Summary per prompt:

| Prompt ID | Plain total | Alpha total | total_delta | lift_delta | polish_delta | winning_surface | lift_qualified | polish_only_flag | length_ratio |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| HHE-002 | 55 | 52 | -3 | 0 | -2 | Plain | no | no | 1.79 |
| HHE-003 | 69 | 68 | -1 | 0 | -1 | Plain | no | no | 1.5 |
| HHE-007 | 68 | 64 | -4 | -3 | -2 | Plain | no | no | 1.84 |
| HHE-009 | 45 | 44 | -1 | 0 | -1 | Plain | no | no | 3.22 |


Aggregate: Plain = 237; Alpha = 228; Alpha delta = -9.

## Alpha advantages observed

- No aggregate or per-comparison total-score advantage was observed for Alpha in this limited four-comparison run.
- The evidence does not support any broader claim about Alpha Solver superiority, MVP validation, production readiness, or provider reasoning orchestration.

## Plain advantages observed

- Plain had the higher recomputed total in all four comparisons in this run.
- The observed margins were small per comparison (`-1` to `-4` Alpha-minus-plain), so interpretation must remain conservative.

## Defects or regressions

See `defects.md` for scorer-recorded defects and caveats. Notable caveats include unsupported comparative/readiness claims in `cmp-HHE-002`, over-broad or assumed requirements in `cmp-HHE-007`, and retained invalid “prove Alpha better” / “MVP validated” framing in both outputs for `cmp-HHE-009`.

## Metrics summary

- Latency summary: not included in source packets; no live calls were made during artifact population.
- Token/cost summary: not included in source packets; no billing or exact cost claim is made.
- Request cap usage: clean capture completed before scoring with 8 outputs for 4 prompts x 2 surfaces; not rerun here.
- Error/rollback summary: no runtime changes, deployment, rollback, or provider/model changes occurred in this artifact-population pass.

## Evidence strength

- `repo-preserved-sanitized-artifact`
- `official-blind-scorer-result`
- `operator-approved-unblinding-map`

Explanation: artifacts are populated from Source Packet A, Source Packet B, and the operator-approved unblinding map only. Raw provider payloads and provider metadata are not preserved.

## Consolidated internal checks

1. Score math verification: all four comparisons are present; each has Output A and Output B; all 14 dimensions are present for both outputs in Source Packet B; Output A, Output B, plain, Alpha, and aggregate totals were recomputed from dimension scores.
2. Blinding verification: Source Packet B confirms the scorer used only Output A / Output B labels, did not infer Alpha identity, did not use route identity or provider metadata, and did not start Batch B; the unblinding map was applied only after scoring.
3. Artifact integrity verification: expected artifacts are populated in this run directory; judge-facing `blinded-score-sheet.csv` uses neutral Output A / Output B fields; artifacts omit raw provider payloads, response IDs, headers, cookies, auth tokens, environment dumps, private data, and secret-like values.
4. PR review readiness: this artifact-population pass includes no runtime code, provider/model config, rubric changes, capture rerun, Google Sheet update, or Batch B work.

## Redactions performed

- Secrets removed: none encountered in synthetic prompt/output text.
- Tokens/cookies/session values removed: none committed; the HHE-009 cookie reference is synthetic prompt/output content, not an actual credential.
- Provider account identifiers removed: none committed.
- Private user data sanitized or not present: not present.
- Raw provider payloads omitted: yes.
- Full unredacted request/response traces omitted: yes.
- Screenshots sanitized or not applicable: not applicable.

## Conservative interpretation

Official results favor plain on this limited four-comparison A3-1 run: Plain = 237, Alpha = 228, Alpha delta = -9. This run does not prove broad plain superiority, does not prove Alpha is worse generally, does not validate MVP readiness, and does not establish production readiness or benchmark success.

## Follow-up tickets

- None created by this artifact-population pass.

## Non-claims

This artifact does not prove MVP validation, Alpha Solver superiority, answer-quality superiority, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration.
