# OUTPUT-DIFF-MEASUREMENT-HARDENING-001 · Output Differentiation Measurement Hardening

## Status

Documentation/spec-first lane for `OUTPUT-DIFFERENTIATION-PHASE-001`.

`OUTPUT-DIFF-MEASUREMENT-HARDENING-001` adds additive measurement-layer hardening
**before the first scored Alpha-vs-plain differentiation run**. The rubric
(`DISC-MRG-069`), artifact lane (`EVAL-ARTIFACT-PRESERVE-001`), prompt-quality
harness (`DISC-MRG-068`), and higher-headroom prompt set (`HIGHER-HEADROOM-EVAL-001`)
are already merged docs/spec lanes; this lane is the pre-run measurement hardening
that lets a future run distinguish expert-interrogation lift from output polish.

This lane is docs/templates/tests only. It does not change runtime behavior,
provider behavior, clarify behavior, `/v1/solve`, preview UI rendering, dashboard
auth, request metrics, the multiple-choice answer-quality eval
(`scripts/run_answer_quality_eval.py`), live provider behavior, tool routing,
effort toggle, persistent quota, Cloud Run configuration, or Google Sheets ledgers.

## Purpose

A read-only audit found the measurement layer could not yet separate
expert-interrogation lift from output polish: the committed score table captured
only 8 of 14 rubric dimensions, artifacts stored verdicts rather than re-scorable
paired outputs, there was no structured Alpha expert-envelope capture, no blinding
or label-stripping, no separate Output A/Output B mapping, no length metric, and
the equal-weight 14-dimension sum let structure/formatting/next-action polish
produce a positive delta even when no real expert constraint was surfaced.

This lane closes those gaps additively so a later scored run is trustworthy. It
does not run that comparison and does not rewrite the rubric prose.

## Scope

In scope:

- Expand the comparison score table to capture all 14 rubric dimensions
  (per-output plain and alpha scores), plus lift/polish/total deltas, length
  metrics, and verdict-qualification fields.
- Add structured Alpha expert-envelope capture fields (considerations,
  assumptions, confidence, mode, clarifying questions, metadata).
- Add a sanitized paired-output capture template that may preserve re-scorable
  sanitized answer text for the synthetic higher-headroom prompt set.
- Add a blind/label-stripped scoring sheet (Output A / Output B) and a separate
  blinding mapping file.
- Add a length metric and length-control guidance.
- Add a lift decision rule and polish-only-win guard as an internal review
  decision aid.
- Backfill the prescribed difficulty/headroom rating for every higher-headroom
  prompt.
- Add a small additive cross-reference note in
  `docs/evals/RESPONSE_QUALITY_RUBRIC.md` pointing to the new aids.
- Add docs-integrity tests.

Out of scope:

- The first (or any) scored or live Alpha-vs-plain differentiation run.
- Live provider runs or enabling OpenAI.
- Provider expert-pass behavior, clarify behavior, `/v1/solve`, preview UI
  rendering, dashboard auth, tool routing, effort toggle, persistent quota.
- `scripts/run_answer_quality_eval.py` and the multiple-choice answer-quality
  eval behavior.
- Rewriting the core rubric prose (only a small additive cross-reference note is
  permitted).
- Editing Google Sheets or backlog workbooks.

## Source hierarchy

1. Repo code and tests.
2. Repo specs and docs, including this spec, `docs/evals/ARTIFACT_PRESERVATION.md`,
   `docs/evals/RESPONSE_QUALITY_RUBRIC.md`, `docs/evals/LIFT_DECISION_RULE.md`, and
   `docs/evals/BLIND_SCORING_PROCEDURE.md`.
3. External planning/status ledgers, including Google Sheets.
4. AI outputs and chat summaries, advisory unless preserved with evidence.

## Fourteen-dimension capture contract

The comparison score table (`docs/evals/templates/comparison_score_table_template.csv`)
must capture, per comparison, a `dNN_plain` and `dNN_alpha` score for all
fourteen `RESPONSE_QUALITY_RUBRIC.md` dimensions (`d01_intent` … `d14_comparative_value`),
plus `plain_total`, `alpha_total`, `total_delta`, `lift_delta`, `polish_delta`,
`winning_surface`, `lift_qualified`, `material_constraint_verified`,
`polish_only_flag`, `output_a_len_words`, `output_b_len_words`, `length_ratio`,
defects, follow-ups, evidence strength, redactions performed, and
`non_claims_confirmed`.

## Expert-envelope capture contract

The paired-output capture template
(`docs/evals/templates/paired_output_capture_template.md`) must provide structured
fields for the Alpha expert envelope: considerations, assumptions (each tagged
material yes/no and correct yes/no), confidence, mode, clarifying questions, and
sanitized envelope metadata. The envelope is inherently Alpha-identifying and is
used in the unblinded analysis/lift-verification step, not shown during blinded
scoring.

## Sanitized paired-output handling

Paired-output capture may preserve re-scorable **sanitized answer text** for the
synthetic higher-headroom prompt set (which is secret-free by construction). It
must never store API keys, bearer tokens, cookies, CSRF tokens, session values,
dashboard passwords, auth headers, raw provider payloads, raw request/response
traces, provider account identifiers, environment dumps, private user data, or
any other secret or credential. Prefer the phrase "sanitized answer text" over
"raw provider output". If a safe summary cannot be produced, do not commit it.

## Blind / label-stripped scoring

Judge-facing scoring uses `Output A` and `Output B` only; Alpha/Plain brand labels
must be absent from the blinded score sheet
(`docs/evals/templates/blinded_score_sheet_template.csv`). The A/B → plain/alpha
mapping lives in a **separate** file
(`docs/evals/templates/blinding_map_template.csv`). The control is **procedural,
not cryptographic**: if committed to the repo the mapping is visible, so the
reviewer scores the blinded sheet before consulting or committing the map.
`docs/evals/BLIND_SCORING_PROCEDURE.md` documents the workflow and states honestly
that Alpha's envelope may remain a structural tell, so the procedure mitigates but
does not eliminate all expectancy bias.

## Length metric and control

Capture `output_a_len_words` and `output_b_len_words` and a `length_ratio`. When
the ratio is large, flag the comparison for length-bias scrutiny so that extra
length is judged on whether it adds a material constraint, not on volume. Length
is a measurement and review aid, not an automated gate.

## Lift decision rule (internal review decision aid)

`docs/evals/LIFT_DECISION_RULE.md` defines `lift_delta` over
{`d04_assumptions`, `d05_hidden_constraints`, `d06_risk_failure`,
`d14_comparative_value`} and `polish_delta` over
{`d03_structure`, `d10_next_actions`, `d12_brevity`}. Alpha earns
`lift_qualified = yes` only when the interrogation dimensions drive the win, at
least one materially correct surfaced constraint is verified, and no disqualifying
defect exists. A positive total driven by polish alone sets `polish_only_flag` and
caps the verdict at Tie/Inconclusive. `lift_qualified` is an internal review
decision aid only; it does not prove anything about product quality.

## Difficulty/headroom backfill

Every higher-headroom prompt (HHE-001 … HHE-016) gets a difficulty/headroom rating
(low/medium/high/stress with a one-line rationale), the field prescribed by
`docs/evals/templates/prompt_set_manifest_template.md` and `DISC-MRG-068`.

## Material that must never be stored

API keys, bearer tokens, dashboard passwords, cookies, CSRF tokens, session
values, auth headers, raw provider payloads, provider account identifiers, full
unredacted request/response traces, environment dumps, private user data, and any
other secrets or credentials.

## Strict non-claims

This lane is a measurement-hardening and internal review decision aid only. It:

- does not validate the MVP;
- does not prove Alpha Solver superiority;
- does not prove answer-quality superiority;
- does not prove production readiness;
- does not prove broad runtime readiness;
- does not prove benchmark success;
- does not prove exact billing accuracy;
- does not prove provider reasoning orchestration;
- does not implement the first differentiation run.

## Relationship to related work

- `DISC-MRG-069` — the rubric this lane hardens the measurement around.
- `EVAL-ARTIFACT-PRESERVE-001` — the artifact lane these templates extend.
- `DISC-MRG-068` — the scoring/regression harness that uses these templates.
- `HIGHER-HEADROOM-EVAL-001` — the prompt set this lane backfills.
- Future run lanes (e.g., a scored differentiation run and a side-by-side evidence
  packet) should consume these hardened artifacts; they are not implemented here.

## Validation expectations

```bash
git diff --check
python -m pytest tests/test_output_diff_measurement_hardening.py -q
python -m pytest -q
```

## Backlog impact

`OUTPUT-DIFF-MEASUREMENT-HARDENING-001` should be marked Done only if the PR
containing this spec, templates, docs, and tests is merged. This is a pre-run
measurement-hardening lane for `OUTPUT-DIFFERENTIATION-PHASE-001`. It prepares the
measurement layer before the first scored Alpha-vs-plain differentiation run and
does not implement that run. Backlog spreadsheets are not edited from this repo
task.
