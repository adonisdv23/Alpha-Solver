# Prompt Quality Scoring and Regression Harness

## Purpose

This guide defines the repeatable prompt quality scoring and regression harness
for future Alpha-vs-plain comparison runs in
`OUTPUT-DIFFERENTIATION-PHASE-001`.

The harness is documentation/spec-first. It is meant to make future evaluations
repeatable without changing provider routing, request metrics, dashboard
sessions, Cloud Run configuration, or runtime behavior.

Use this harness to:

- make Alpha-vs-plain runs repeatable;
- score prompts and outputs consistently;
- detect regressions in Alpha Solver expert-preview behavior;
- connect prompt manifests, run reports, and score tables to the artifact
  preservation lane;
- avoid unsupported superiority claims.

## Scope boundaries

This harness does not:

- validate the MVP;
- prove Alpha Solver superiority;
- prove production readiness;
- prove broad runtime readiness;
- prove benchmark success;
- prove exact billing accuracy;
- prove provider reasoning orchestration;
- change runtime behavior;
- change provider behavior;
- change request metrics;
- change dashboard auth/session/CSRF behavior;
- enable OpenAI;
- deploy Cloud Run;
- update Google Sheets.

## Inputs and outputs

### Inputs

A future evaluation run should start with:

- a sanitized prompt set manifest;
- the branch, commit, and mode being evaluated;
- the plain provider configuration summary;
- the Alpha Solver expert-preview configuration summary;
- the response rubric in `docs/evals/RESPONSE_QUALITY_RUBRIC.md`;
- the artifact preservation guide in `docs/evals/ARTIFACT_PRESERVATION.md`.

### Outputs

A completed run should preserve sanitized artifacts under `docs/evals/runs/`,
for example:

```text
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/prompt-set-manifest.md
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/run-summary.md
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/comparison-score-table.csv
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/regression-summary.md
```

Use `docs/evals/templates/run_report_template.md` and the templates added for
this harness as copyable starting points. Keep all committed artifacts sanitized
and summary-level.

## Prompt-level metadata

Each prompt in a stable prompt set should include the following metadata before
running either output surface.

| Field | Purpose |
| --- | --- |
| Prompt ID | Stable identifier used in manifests, score tables, and run reports. |
| Prompt family | Higher-headroom taxonomy family being exercised. |
| Prompt text or sanitized prompt summary | Full text only if safe; otherwise a summary preserving evaluation intent. |
| User intent | What the user is actually trying to accomplish. |
| Expected deliverable | The concrete artifact, answer, decision, or plan expected. |
| Required sections or format | Required headings, tables, bullets, citations, or output shape. |
| Hidden constraints being tested | Constraints the answer should infer or preserve. |
| Failure modes being tested | Known defects the prompt is designed to expose. |
| Rubric dimensions emphasized | Dimensions from `docs/evals/RESPONSE_QUALITY_RUBRIC.md` most relevant to the prompt. |
| Difficulty / headroom level | Low, medium, high, or stress; explain why. |
| Safety or claim-boundary concerns | Claims, readiness statements, privacy concerns, or overconfidence risks to watch. |
| Source or rationale | Why this prompt belongs in the set and what prior issue, user need, or spec it represents. |
| Allowed assumptions | Assumptions the model may make without asking a clarification. |
| Disallowed claims | Claims that should not appear without artifact-backed evidence. |
| Expected evidence capture | Artifacts to preserve, including summaries, score rows, defects, screenshots, or metrics when safe. |

## Prompt family taxonomy for higher-headroom testing

Use one primary family and optional secondary families per prompt.

| Family | What it tests |
| --- | --- |
| Ambiguous execution planning | Whether the answer can turn incomplete instructions into a useful plan while surfacing assumptions. |
| Claim-boundary / readiness judgment | Whether the answer avoids overclaiming MVP validation, superiority, production readiness, benchmark success, billing accuracy, or orchestration proof. |
| Hidden constraint detection | Whether the answer catches constraints embedded in context, formatting instructions, safety limits, or repo rules. |
| Prioritization under uncertainty | Whether the answer chooses useful next steps despite incomplete information and explains tradeoffs. |
| Artifact review / prompt review | Whether the answer evaluates prompts, specs, reports, or evidence packets against stated criteria. |
| Debugging and failure-mode diagnosis | Whether the answer identifies plausible causes, risks, and verification steps without inventing unsupported facts. |
| Rollout / go/no-go decision | Whether the answer supports deployment, preview, rollback, or operator decisions with conservative evidence handling. |
| Evidence interpretation | Whether the answer distinguishes observed evidence from conclusions and records confidence limits. |
| Adversarial/noisy context | Whether the answer resists irrelevant, conflicting, or unsafe instructions while preserving the real task. |
| Research synthesis / source hierarchy | Whether the answer applies source hierarchy, cites evidence appropriately, and avoids unsupported synthesis. |

## Scoring workflow

1. **Select prompt set.** Choose a stable prompt manifest and record the prompt
   IDs, families, expected deliverables, emphasized rubric dimensions, and
   claim-boundary concerns.
2. **Run plain provider output.** Capture only sanitized summaries and safe
   metadata. Do not commit raw provider payloads.
3. **Run Alpha expert-preview output.** Capture only sanitized summaries and safe
   metadata. Do not commit raw provider payloads.
4. **Preserve sanitized artifacts.** Store run summaries, prompt manifests, and
   score tables under `docs/evals/runs/` using
   `docs/evals/ARTIFACT_PRESERVATION.md`.
5. **Score with the universal rubric.** Use
   `docs/evals/RESPONSE_QUALITY_RUBRIC.md` for per-dimension scores. Score the
   answer, not the model brand.
6. **Calculate per-dimension scores.** Record plain and Alpha scores for each
   relevant rubric dimension.
7. **Calculate Alpha-vs-plain delta.** Use `Alpha score - Plain score`; the
   delta informs the verdict but does not automatically prove superiority.
8. **Identify defects.** Record defects for Alpha, plain, or both, including
   missed deliverables, format drift, hidden constraint misses, unsupported
   claims, or unsafe assumptions.
9. **Identify follow-up tickets.** Link proposed specs, tests, prompt updates,
   product changes, or evaluation follow-ups.
10. **Record conservative interpretation.** State only the narrowest conclusion
    supported by the preserved artifacts.

## Regression workflow

Use a stable prompt set as a regression suite after behavior, answer-structure,
prompting, provider, or routing-adjacent changes. The goal is to detect whether
Alpha behavior got worse on tasks it should continue to handle well.

1. Identify the prior preserved run artifact and baseline score table.
2. Rerun the same sanitized prompt set unless a documented expected change
   requires an updated prompt.
3. Preserve the new run artifacts under `docs/evals/runs/`.
4. Compare new scores against the prior run by prompt, family, and dimension.
5. Flag regressions in:
   - direct answer usefulness;
   - format preservation;
   - assumptions;
   - hidden constraints;
   - risk/failure modes;
   - claim boundaries;
   - next actions;
   - comparative added value.
6. Distinguish expected changes from regressions. An expected change should be
   tied to a spec, implementation change, or documented review rationale.
7. Record follow-up tickets for material regressions.
8. Record conservative interpretation and non-claims.

## Score interpretation

Use scores as structured evidence, not as proof by themselves.

- One prompt cannot prove superiority.
- Small deltas are inconclusive.
- Narrow prompt family wins only support local advantage.
- Broad claims require repeated artifact-backed evidence.
- Plain wins must be recorded honestly.
- Ties must be recorded honestly.
- Incomplete artifacts should produce `Inconclusive`, not a forced winner.
- Cost and latency may be noted when safely available, but they should not
  dominate this phase unless they prevent practical usability.

Suggested outcome labels:

| Label | Meaning |
| --- | --- |
| `Alpha local advantage` | Alpha materially outscored plain on a prompt or narrow family with artifact-backed reasons. |
| `Plain local advantage` | Plain materially outscored Alpha and the defect should be recorded honestly. |
| `Tie` | Outputs were materially equivalent for the user's goal. |
| `Inconclusive` | Delta is small, artifacts are incomplete, or reviewer context is insufficient. |
| `Regression flagged` | Alpha degraded against a prior stable-run baseline on one or more material dimensions. |
| `Expected change` | Score changed due to an intended, documented behavior change rather than a defect. |

## Artifact integration

Future run outputs should use `docs/evals/ARTIFACT_PRESERVATION.md`.
Committed future artifacts should live under `docs/evals/runs/`. Prompt
manifests and score tables should be sanitized. No raw provider payloads or
secrets should be committed.

Recommended templates:

- `docs/evals/templates/prompt_set_manifest_template.md`;
- `docs/evals/templates/comparison_score_table_template.csv`;
- `docs/evals/templates/regression_run_summary_template.md`;
- `docs/evals/templates/run_report_template.md`.

## Redaction and safety

Never store:

- API keys;
- bearer tokens;
- dashboard passwords;
- cookies;
- CSRF tokens;
- session values;
- raw provider payloads;
- provider account identifiers;
- full unredacted request/response traces;
- private user data unless explicitly sanitized and needed.

Before committing any prompt manifest, score table, run report, screenshot
reference, or regression summary:

- summarize or sanitize prompt text when it contains private, sensitive, or
  proprietary material;
- summarize outputs instead of pasting raw provider responses;
- remove provider account identifiers and private tenant/user identifiers;
- state what redactions were performed;
- omit the artifact if a safe summary cannot be produced.

## Relationship to related work

- `DISC-MRG-069` defines the response quality rubric used for prompt and output
  scoring. This harness defines how to apply it repeatably.
- `EVAL-ARTIFACT-PRESERVE-001` defines the preservation lane, artifact location,
  evidence strength labels, and redaction rules. This harness depends on that
  lane for committed evidence.
- `HIGHER-HEADROOM-EVAL-001` should use this taxonomy and manifest shape to
  select prompts with enough headroom to reveal output differentiation.
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001` should use these manifests, score
  tables, and conservative interpretations for side-by-side evidence packets.
- `EVAL-DIFFERENTIATION-RUN-001` should use this scoring and regression workflow
  for repeatable Alpha-vs-plain runs.
- `ALPHA-VISIBLE-DIFFERENTIATOR-001` should rely on repeated, artifact-backed
  local advantages rather than unsupported broad superiority claims.
- `ALPHA-ANSWER-STRUCTURE-V2-001` should use this regression workflow to detect
  whether answer-structure changes improve outputs without degrading format,
  assumptions, hidden-constraint handling, or claim boundaries.

## Strict non-claims

This harness does not validate the MVP.

This harness does not prove Alpha Solver superiority.

This harness does not prove production readiness.

This harness does not prove broad runtime readiness.

This harness does not prove benchmark success.

This harness does not prove exact billing accuracy.

This harness does not prove provider reasoning orchestration.

## Backlog impact

`DISC-MRG-068` should be marked Done only if this PR is merged.

This is P0 for `OUTPUT-DIFFERENTIATION-PHASE-001`.

This enables repeatable Alpha-vs-plain comparison and regression detection.

This does not prove Alpha Solver superiority.

This does not validate the MVP.

This does not prove production readiness.

Backlog spreadsheets are not edited from this repo task.
