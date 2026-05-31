# EVAL-ANSWER-QUALITY-RESULTS-001: Answer Quality Eval Results

## 1. Purpose

This memo records the answer-quality live eval and repeatability findings across both the original 16-case era and the expanded 48-case era, before any MVP thesis gate, observability, orchestration, hosting, budget, fallback, CLI, portable, SLO, or production-hardening work.

The purpose is narrow: preserve the evidence honestly, state what the eval mechanism did and did not show, and prevent overclaiming from small or saturated case sets.

## 2. Source-of-truth hierarchy and artifact caveat

Source-of-truth order for this memo:

1. Repo implementation contracts and eval docs, especially `docs/evals/ANSWER_QUALITY_EVAL.md`, `docs/evals/ANSWER_QUALITY_EVAL_PLAN.md`, `config/quality_gate.yaml`, `scripts/run_answer_quality_eval.py`, `tests/test_answer_quality_eval.py`, and `datasets/answer_quality_operator_cases.jsonl`.
2. Preserved eval artifacts from documented live runs.
3. Operator-reported live-run summaries when artifacts were not preserved.

Artifact caveat:

- The first full live run was reported but its artifacts were not preserved. It is useful context, but it is weaker evidence than preserved artifacts.
- The preserved full rerun and the 16-case live repeatability run have documented artifact locations and archives.
- The expanded 48-case live repeatability run is documented below as operator-reported because the requested live artifact directory `artifacts/eval/answer_quality/20260531T034439Z_repeatability/` and archive `artifacts/eval/answer_quality/expanded_live_artifacts_20260531T034439Z_repeatability.tar.gz` were not present in the repo workspace reviewed after the run, `artifacts/` is gitignored, and no committed reference was found for `034439Z_repeatability`.
- This memo records evidence, not proof. It does not replace the pre-registered eval design or the quality gate.

## 3. Implementation sequence, PRs #190-#193

- PR #190 implemented `EVAL-ANSWER-QUALITY-001`, the gated answer-quality eval mechanism.
- PR #191 fixed the baseline/treatment context confound by giving both arms shared project context and making the treatment variable the Alpha Solver operator-discipline checklist.
- PR #192 changed the default eval model from `gpt-5-mini` to `gpt-5.4-mini` and fixed artifact safety-scan false positives.
- PR #193 added `EVAL-REPEATABILITY-001`: opt-in repeatability support with `--repeat-runs N`, per-run artifacts, `repeatability_summary.json`, cost checks, `aq-lane-003` tracking, docs, and tests.
- `EVAL-REPEATABILITY-VERIFY-001` passed in no-live mode after PR #193.

## 4. Pre-expansion eval design summary

The eval mechanism compares two arms over the same Alpha Solver-native case set:

| Arm | Meaning |
| --- | --- |
| Baseline | Direct OpenAI provider primitive with a careful-assistant system prompt, shared project context, and the same output-format task instruction. |
| Treatment | Same model, settings, shared project context, and output-format task instruction, plus the Alpha Solver operator-discipline checklist. |

The treatment variable is structured operator discipline, not possession of project rules. The mechanism is operationally successful in the limited sense that it can run gated live comparisons, preserve artifacts, enforce safety checks, summarize per-run outcomes, and aggregate opt-in repeatability results.

The pre-expansion dataset had 16 cases. With 16 cases, one case changes the treatment-minus-baseline margin by `0.0625`. The pre-registered minimum treatment margin is `0.05`, so the threshold is functionally a requirement to win by at least one case. The OpenAI seed is carried in the provider request but is not transmitted to the current OpenAI client, so live runs remain nondeterministic.

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

## 14. EVAL-EXPANDED-RESULTS-001 purpose

This expanded-results section records the 48-case answer-quality eval interpretation after `EVAL-CASESET-EXPANSION-001`, PR #195, PR #196, no-live verification, Claude pre-live review, the gated live repeatability run `EVAL-EXPANDED-LIVE-001`, and Claude Code post-live review.

The purpose is to document the expanded 48-case result honestly, keep the prior 16-case result history intact, and prevent overclaiming. This section is a docs-only interpretation memo. It does not change code, tests, datasets, config, workflows, generated artifacts, provider behavior, or runtime behavior.

## 15. Expanded source-of-truth and artifact caveat

Source-of-truth order for the expanded result remains:

1. Checked-in implementation contracts and eval docs.
2. Preserved eval artifacts, when present.
3. Operator-reported run summaries when artifacts are not preserved in the repo workspace.

For `EVAL-EXPANDED-LIVE-001`, the live numbers below are operator-reported, not repo-artifact-backed, unless the archive is separately recovered, attached, and preserved. The requested post-run artifact directory `artifacts/eval/answer_quality/20260531T034439Z_repeatability/` was absent from the reviewed repo workspace. The requested archive `artifacts/eval/answer_quality/expanded_live_artifacts_20260531T034439Z_repeatability.tar.gz` was also absent. The repository ignores `artifacts/`, and `git log --all -S "034439Z_repeatability"` was reported to find no committed reference. Therefore this memo must not claim the expanded 48-case numbers are backed by committed or present repo artifacts.

This caveat does not mean the operator-reported numbers are unusable as a run note. It means they are weaker evidence than preserved artifacts and must be labeled as operator-reported in downstream summaries, backlog updates, and PR descriptions.

## 16. Prior 16-case result summary

The prior 16-case result remains preserved as historical context:

- The eval mechanism worked operationally and could run a fair shared-context baseline versus operator-discipline treatment comparison.
- The first full live run was reported as 15/16 baseline, 15/16 treatment, margin 0.0, with artifacts not preserved.
- The preserved full rerun was 15/16 baseline, 16/16 treatment, margin 0.0625, with the only incorrect row being baseline on `aq-lane-003`.
- The 16-case repeatability run completed three live runs with margins 0.0, 0.0625, and 0.0625, yielding an unstable aggregate below the pre-registered 0.05 threshold.
- The signal was saturated and effectively hinged on `aq-lane-003`, a simulated-vs-live-evidence trap.
- The 16-case result did not establish Alpha Solver superiority, MVP validation, model superiority, orchestration validation, or production readiness.

## 17. Expansion and hardening summary

PR #195 expanded the answer-quality eval dataset from 16 to 48 fixed cases. The expanded dataset preserved the original cases and targeted 12 cases per implemented category: runtime overclaim detection, source hierarchy conflict detection, lane selection, and backlog impact classification.

PR #196 hardened the expanded dataset after Claude review. The hardening pass fixed the reviewed 48-case set before live evaluation and kept the result framed as smoke evidence, not proof.

The expanded set remained an Alpha Solver-native answer-quality eval for a fair shared-context baseline versus an operator-discipline treatment. It did not become an MVP-validation dataset, a model benchmark, a production-readiness certification, or a validation of provider reasoning orchestration.

## 18. No-live verification summary

Post-merge no-live verification passed before the expanded live run. The no-live phase verified the fixed 48-case dataset and eval path without calling OpenAI and without creating live provider predictions.

This no-live verification supported readiness to run the gated live eval, but it was not live answer-quality evidence and did not by itself validate treatment quality, model quality, orchestration, MVP readiness, or production readiness.

## 19. Claude pre-live case-quality approval

Claude pre-live review approved the fixed 48-case dataset for live eval after the PR #196 hardening pass. That approval addressed case quality and readiness to run the gated eval. It did not pre-judge the live result and did not authorize superiority, MVP-validation, orchestration-validation, model-superiority, or production-readiness claims.

## 20. Expanded live eval setup

`EVAL-EXPANDED-LIVE-001` was run as a gated live repeatability eval with `--repeat-runs 3`.

Operator-reported setup:

| Field | Value |
| --- | --- |
| Fixed cases | 48 |
| Cases per category | 12 |
| `minimum_margin` | 0.0625 |
| Requested runs | 3 |
| Completed runs | 3 |
| Live | true |
| Default model | `gpt-5.4-mini` |
| `--model` passed | no |
| `--limit` passed | no |
| Safety scan | passed |
| Files edited by run | none |
| PR created by run | none |

The pre-registered success criterion for the expanded 48-case run was treatment-minus-baseline accuracy margin at least `0.0625`, equivalent to at least three net cases out of 48.

## 21. Expanded live eval result

Operator-reported aggregate result:

| Metric | Value |
| --- | --- |
| Mean margin | 0.006944444444444457 |
| Rounded mean margin | 0.0069 |
| Margin standard deviation | 0.012028130608117225 |
| Rounded margin standard deviation | 0.0120 |
| Margin minimum | 0.0 |
| Margin maximum | 0.02083333333333337 |
| Rounded margin maximum | 0.0208 |
| Success count by run | 0 of 3 |
| Stability label | inconclusive |

Operator-reported per-run results:

| Run | Baseline | Treatment | Margin | Success |
| --- | --- | --- | --- | --- |
| 1 | 47/48 | 48/48 | 0.02083333333333337 | false |
| 2 | 47/48 | 47/48 | 0.0 | false |
| 3 | 47/48 | 47/48 | 0.0 | false |

The completed runs did not show a repeatable treatment-margin pass. Zero of three runs met the pre-registered `0.0625` success criterion. The expanded live result is therefore inconclusive and negative against the threshold.

## 22. Saturation and aq-lane-003 concentration analysis

The expanded 48-case result is saturated for `gpt-5.4-mini` on this fixed case set. Operator-reported per-case observations show that 47 of 48 cases were perfect for both arms across all three runs.

The only differentiating case was `aq-lane-003`:

- Baseline on `aq-lane-003`: 0/3.
- Treatment on `aq-lane-003`: 1/3.
- Earlier `aq-lane-003` treatment strength weakened from the prior 16-case era.

This makes the expanded result single-case-concentrated and fragile. The result identifies `aq-lane-003` as a useful diagnostic lead, but the 48-case live run does not show a broad treatment effect across categories. More polishing of this same dataset is not recommended right now because the live result suggests the set has too little headroom for this model rather than a simple wording defect.

## 23. Repeatability interpretation

`EVAL-EXPANDED-REPEATABILITY-001` is functionally satisfied and folded into `EVAL-EXPANDED-LIVE-001` because the expanded live run used `--repeat-runs 3`, completed all three requested runs, and produced an aggregate repeatability result.

The repeatability interpretation is negative against the pre-registered gate: the run-to-run margins were 0.0208, 0.0, and 0.0, with zero successful runs. Additional live spending on the same 48-case set is not recommended because the set is saturated, the signal is concentrated on `aq-lane-003`, and repeat-runs=3 already showed no repeatable pass.

## 24. Allowed expanded-result claims

The following claims are allowed from the expanded 48-case result:

- PR #195 expanded the answer-quality eval dataset from 16 to 48 cases.
- PR #196 hardened the expanded dataset after Claude review.
- No-live verification passed before the expanded live run.
- Claude pre-live review approved the fixed 48-case dataset for live eval.
- `EVAL-EXPANDED-LIVE-001` was operator-reported as a gated live repeatability eval with 48 fixed cases, 12 cases per category, `--repeat-runs 3`, default model `gpt-5.4-mini`, no `--model`, no `--limit`, and `minimum_margin` 0.0625.
- The expanded live numbers are operator-reported unless the missing artifact directory or archive is separately recovered and preserved.
- As operator-reported, completed runs had treatment-minus-baseline margins 0.0208, 0.0, and 0.0, mean 0.0069, stdev 0.0120, min 0.0, max 0.0208, and zero of three runs meeting the pre-registered 0.0625 margin.
- As operator-reported, 47 of 48 cases were correct for both arms in every run, and the only differentiating case was `aq-lane-003`.
- The expanded result is inconclusive, negative against the pre-registered gate, saturated for this model, and concentrated on a fragile single-case signal.
- `EVAL-EXPANDED-REPEATABILITY-001` is functionally satisfied by the repeat-runs=3 live run.
- Additional live spending on the same 48-case set is not recommended.
- `MVP-THESIS-GATE-001` remains blocked/deferred.
- Artifact preservation is a known gap and future lane.
- A future higher-headroom discriminating eval and candidate `PROVIDER-REASONING-ORCHESTRATION-001` scoping may be considered as future analysis, but neither is validated by this result.

## 25. Forbidden expanded-result claims

The following claims are forbidden by the expanded 48-case evidence:

- Alpha Solver superiority.
- MVP validation.
- Model superiority.
- Orchestration validation.
- Production readiness.
- A repeatable treatment-margin pass on the fixed 48-case set.
- That the expanded 48-case live numbers are repo-artifact-backed unless the missing artifacts are separately recovered, attached, and preserved.
- That `aq-lane-003` proves general treatment value.
- That more live spending on the same 48-case set is likely to unlock useful evidence.
- That dataset polishing alone is the right next step.
- That `PROVIDER-REASONING-ORCHESTRATION-001` has been started or validated.
- That budget enforcement, fallback, hosting, observability, SLOs, CLI, portable behavior, or production hardening are completed by this eval result.

## 26. MVP thesis gate implication

`MVP-THESIS-GATE-001` remains blocked/deferred. The expanded live result did not meet the `0.0625` success criterion, did not show a repeatable treatment-margin pass, and was saturated with the only differentiating signal concentrated on `aq-lane-003`.

This memo should be used to prevent accidental advancement of the MVP thesis gate. The expanded result may inform future eval design, but it does not validate the MVP thesis.

## 27. Recommended next steps

Recommended next steps:

1. Treat `EVAL-EXPANDED-RESULTS-001` as the current source-of-truth documentation lane for the expanded 48-case result.
2. Do not spend more live budget on the same fixed 48-case set.
3. Do not spend more time polishing the same dataset as the immediate next value lane.
4. Preserve or recover the missing live artifacts if they exist outside the repo workspace; otherwise keep the expanded live numbers labeled operator-reported.
5. Consider a future artifact-preservation lane so live result directories and archives that should be cited later are not lost behind `artifacts/` gitignore behavior.
6. Consider a future higher-headroom, deliberately discriminating eval with enough difficult cases to avoid saturation for `gpt-5.4-mini` or successor models.
7. Consider candidate `PROVIDER-REASONING-ORCHESTRATION-001` scoping only as future analysis. This expanded eval result does not validate orchestration.

## 28. Known gaps

Known gaps:

- The expanded live artifact directory and archive were not present in the reviewed repo workspace.
- The expanded live numbers are operator-reported unless separate artifact recovery occurs.
- `artifacts/` is gitignored, so live evidence intended for later citation can be lost unless it is explicitly archived or otherwise preserved outside normal ignored paths.
- The fixed 48-case set appears too saturated for the tested default model to provide useful headroom.
- The only differentiating signal is concentrated on `aq-lane-003`, so it is not broad category evidence.
- The result does not decide whether to build provider reasoning orchestration; it only suggests that future value-lane scoping may need a higher-headroom eval design.

## 29. Expanded 48-case conclusion

A gated live repeatability eval (N=3, `gpt-5.4-mini`, the fixed 48-case Alpha Solver-native set, fair shared-context baseline vs operator-discipline treatment, `minimum_margin` 0.0625) was reported with three requested and three completed runs. As operator-reported, because the run artifact directory and archive were not present in the repo workspace and `artifacts/` is gitignored, per-run treatment-minus-baseline margins were 0.0208, 0.0, and 0.0, with mean 0.0069, stdev 0.0120, min 0.0, max 0.0208, and zero of three runs meeting the pre-registered 0.0625 margin. Forty-seven of the forty-eight cases were correct for both arms in every run; the only differentiating case was `aq-lane-003`, where baseline failed all three runs and treatment succeeded once. The expanded 48-case result is therefore inconclusive, negative against the pre-registered success gate, saturated for this model, and concentrated on a fragile single-case signal. It does not support Alpha Solver superiority, MVP validation, model superiority, orchestration validation, or production readiness. `EVAL-EXPANDED-REPEATABILITY-001` is functionally satisfied by the repeat-runs=3 live run, and additional live spending on the same 48-case set is not recommended. `MVP-THESIS-GATE-001` remains blocked/deferred pending a documented interpretation and a future decision about whether to scope a higher-headroom discriminating eval and/or `PROVIDER-REASONING-ORCHESTRATION-001`.
