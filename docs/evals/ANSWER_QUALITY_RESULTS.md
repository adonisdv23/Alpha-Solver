# EVAL-ANSWER-QUALITY-RESULTS-001: Answer Quality Eval Results

## 1. Purpose

This memo records the answer-quality live eval and repeatability findings before any case-set expansion, MVP thesis gate, observability, orchestration, hosting, budget, fallback, CLI, portable, SLO, or production-hardening work.

The purpose is narrow: preserve the evidence honestly, state what the current eval mechanism did and did not show, and prevent overclaiming from a small, mostly saturated 16-case set.

## 2. Source-of-truth hierarchy and artifact caveat

Source-of-truth order for this memo:

1. Repo implementation contracts and eval docs, especially `docs/evals/ANSWER_QUALITY_EVAL.md`, `docs/evals/ANSWER_QUALITY_EVAL_PLAN.md`, `config/quality_gate.yaml`, `scripts/run_answer_quality_eval.py`, `tests/test_answer_quality_eval.py`, and `datasets/answer_quality_operator_cases.jsonl`.
2. Preserved eval artifacts from documented live runs.
3. Operator-reported live-run summaries when artifacts were not preserved.

Artifact caveat:

- The first full live run was reported but its artifacts were not preserved. It is useful context, but it is weaker evidence than preserved artifacts.
- The preserved full rerun and the live repeatability run have documented artifact locations and archives.
- This memo records evidence, not proof. It does not replace the pre-registered eval design or the quality gate.

## 3. Implementation sequence, PRs #190-#193

- PR #190 implemented `EVAL-ANSWER-QUALITY-001`, the gated answer-quality eval mechanism.
- PR #191 fixed the baseline/treatment context confound by giving both arms shared project context and making the treatment variable the Alpha Solver operator-discipline checklist.
- PR #192 changed the default eval model from `gpt-5-mini` to `gpt-5.4-mini` and fixed artifact safety-scan false positives.
- PR #193 added `EVAL-REPEATABILITY-001`: opt-in repeatability support with `--repeat-runs N`, per-run artifacts, `repeatability_summary.json`, cost checks, `aq-lane-003` tracking, docs, and tests.
- `EVAL-REPEATABILITY-VERIFY-001` passed in no-live mode after PR #193.

## 4. Eval design summary

The eval mechanism compares two arms over the same Alpha Solver-native case set:

| Arm | Meaning |
| --- | --- |
| Baseline | Direct OpenAI provider primitive with a careful-assistant system prompt, shared project context, and the same output-format task instruction. |
| Treatment | Same model, settings, shared project context, and output-format task instruction, plus the Alpha Solver operator-discipline checklist. |

The treatment variable is structured operator discipline, not possession of project rules. The mechanism is operationally successful in the limited sense that it can run gated live comparisons, preserve artifacts, enforce safety checks, summarize per-run outcomes, and aggregate opt-in repeatability results.

The current dataset has 16 cases. With 16 cases, one case changes the treatment-minus-baseline margin by `0.0625`. The pre-registered minimum treatment margin is `0.05`, so the threshold is functionally a requirement to win by at least one case. The OpenAI seed is carried in the provider request but is not transmitted to the current OpenAI client, so live runs remain nondeterministic.

## 5. Full live run sequence

### First full live run

- Baseline: 15/16.
- Treatment: 15/16.
- Observed margin: 0.0.
- `success_criteria_met`: false.
- Artifacts were not preserved.

### Preserved full rerun

- Baseline: 15/16.
- Treatment: 16/16.
- Observed margin: 0.0625.
- `success_criteria_met`: true.
- Only incorrect row: baseline on `aq-lane-003`.
- Preserved artifact directory: `artifacts/eval/answer_quality/20260531T003426Z`.
- Archive: `artifacts/eval/answer_quality/full_live_artifacts_20260531T003426Z.tar.gz`.

## 6. Repeatability result

Live repeatability run:

- Artifact directory: `artifacts/eval/answer_quality/20260531T012119Z_repeatability`.
- Archive: `artifacts/eval/answer_quality/repeatability_live_artifacts_20260531T012119Z_repeatability.tar.gz`.
- Requested runs: 3.
- Completed runs: 3.
- Model: `gpt-5.4-mini`.
- Case count: 16.
- Live: true.
- Safety scan: passed.
- Files edited during run: none.
- PR created during run: none.

Per-run results:

| Run | Baseline | Treatment | Margin | Success |
| --- | --- | --- | --- | --- |
| 1 | 15/16 | 15/16 | 0.0 | false |
| 2 | 15/16 | 16/16 | 0.0625 | true |
| 3 | 15/16 | 16/16 | 0.0625 | true |

Aggregate repeatability metrics:

- Mean margin: 0.041666666666666664.
- Rounded mean margin: 0.042.
- Margin standard deviation: 0.03608439182435161.
- Rounded margin standard deviation: 0.036.
- Margin minimum: 0.0.
- Margin maximum: 0.0625.
- Success count by run: 2 of 3.
- Apparent treatment advantage stability: unstable.

## 7. aq-lane-003 finding

`aq-lane-003` is the only meaningful differentiating case observed so far.

Tracked hit rates:

- Repeatability baseline hit rate: 0/3.
- Repeatability treatment hit rate: 2/3.
- Including the preserved full rerun: baseline 0/4, treatment 3/4.

Interpretation of this case:

- The case tests a simulated-vs-live-evidence trap: whether simulated `compare_baseline` token/latency evidence may be used as real answer-quality evidence.
- The baseline failed this case in every documented run with preserved per-case data.
- The treatment usually succeeded, but not always.
- This is a useful mechanistic lead for case expansion, not proof of a general treatment effect.

## 8. Interpretation

A gated live repeatability check (N=3, `gpt-5.4-mini`, 16 Alpha Solver-native cases, fair shared-context baseline vs operator-discipline treatment), combined with two earlier full runs, produced treatment-minus-baseline margins that took only two values across all five runs: 0.0 or 0.0625. The three repeatability runs gave a mean margin of 0.042, below the pre-registered 0.05, with 2 of 3 runs passing and a standard deviation of 0.036. Because the set has 16 cases, one case is worth 0.0625, so the 0.05 threshold is functionally "win by at least one case," and runs are nondeterministic because seed is not transmitted to the OpenAI client. Across all runs with preserved per-case data, both arms answered fifteen of the sixteen cases correctly every time; the entire margin rests on a single case, `aq-lane-003`, on which the baseline failed in every documented run and the treatment usually succeeded. We therefore record no stable treatment advantage: the aggregate result is unstable and below threshold, and the only differentiating signal is confined to one case that is partly attributable to that case's phrasing and is itself unstable. This is inconclusive evidence on the MVP thesis. The positive finding, a stable baseline failure mode on a simulated-vs-live-evidence trap that the discipline checklist tends to correct, is recorded as a hypothesis to be tested through a larger, harder, deliberately discriminating case set, not as demonstrated value. No claim of Alpha Solver superiority, MVP validation, model superiority, or production readiness is warranted.

Summary interpretation:

- The eval mechanism worked operationally.
- The treatment evidence is inconclusive.
- The aggregate treatment advantage is unstable and below threshold.
- The current 16-case set is saturated and effectively hinges on one case.
- `aq-lane-003` is a plausible lead for future case design, not proof.
- Repeating the current case set is not the next useful step.

## 9. Allowed claims

The following claims are allowed:

- The gated answer-quality eval mechanism is operational and can produce live comparison artifacts when explicitly enabled.
- The shared-context baseline/treatment design makes the operator-discipline checklist the intended treatment variable.
- In the documented live runs, observed treatment-minus-baseline margins were either 0.0 or 0.0625.
- The N=3 repeatability run had mean margin `0.041666666666666664`, standard deviation `0.03608439182435161`, min `0.0`, max `0.0625`, and 2 of 3 runs passing.
- The aggregate repeatability result is unstable and below the pre-registered 0.05 threshold.
- The current 16-case set is saturated: fifteen cases were effectively correct for both arms in preserved runs, and the observed difference hinges on `aq-lane-003`.
- `aq-lane-003` identifies a useful hypothesis about simulated-vs-live-evidence confusion for future case-set expansion.
- `EVAL-CASESET-EXPANSION-001` is the recommended next lane.
- `MVP-THESIS-GATE-001` remains blocked.

## 10. Forbidden claims

The following claims are forbidden by the evidence:

- Alpha Solver superiority.
- MVP validation.
- Model superiority.
- Production readiness.
- That the current eval demonstrates a stable treatment win.
- That discipline-as-prompting validates full Alpha Solver reasoning orchestration.
- That `/v1/solve` OpenAI mode is more than provider pass-through unless future implementation changes prove otherwise.
- That budget enforcement, fallback, hosting, observability, orchestration, SLOs, CLI, portable behavior, or production hardening are completed by this eval result.
- That `aq-lane-003` proves general treatment value.

## 11. Decision

Record `EVAL-ANSWER-QUALITY-RESULTS-001` as a documentation/results memo only.

Decision:

- Do not claim a stable treatment advantage.
- Do not advance `MVP-THESIS-GATE-001`.
- Do not run more repeats of the current 16-case set as the main next step.
- Treat the current result as inconclusive evidence that found one useful failure-mode lead.

## 12. Next lane: EVAL-CASESET-EXPANSION-001

The next lane should be `EVAL-CASESET-EXPANSION-001`.

Recommended scope:

- Expand the case set with larger, harder, deliberately discriminating Alpha Solver-native cases.
- Add cases that test the mechanism behind `aq-lane-003` without depending on one phrasing.
- Preserve fair shared context across arms.
- Keep evidence-not-proof framing.
- Pre-register success criteria before running new live evals.

Non-scope for this memo:

- This memo does not create the expanded case set.
- This memo does not change code, tests, datasets, workflows, config, generated artifacts, or runtime behavior.

## 13. Blocked/deferred lanes

Blocked:

- `MVP-THESIS-GATE-001` remains blocked because treatment evidence is inconclusive, unstable, and below threshold.

Deferred until stronger eval evidence exists:

- `OBSERVABILITY-PLAN-001`.
- Provider orchestration.
- Hosting.
- Budget enforcement and billing integration.
- Fallback behavior.
- CLI work.
- Portable behavior changes.
- SLO work.
- Production hardening.
