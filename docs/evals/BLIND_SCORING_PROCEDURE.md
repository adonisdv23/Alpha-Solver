# Blind Scoring Procedure

This procedure reduces reviewer expectancy bias when scoring plain provider output
against Alpha Solver expert-preview output during `OUTPUT-DIFFERENTIATION-PHASE-001`.
It supports `OUTPUT-DIFF-MEASUREMENT-HARDENING-001` and is used before the first
scored Alpha-vs-plain differentiation run. It is documentation only and changes no
runtime, provider, dashboard, or eval-script behavior.

## Why

Judge-facing templates previously labeled outputs as Plain vs Alpha, which invites
brand expectancy bias. This procedure makes scoring use neutral `Output A` /
`Output B` labels and keeps the de-anonymizing mapping in a separate file.

## Honest limits

The control is **procedural, not cryptographic**. If the mapping file is committed
to the repository it is visible; the protection comes from the reviewer scoring the
blinded sheet before consulting or committing the mapping, not from hiding it.
Alpha's expert envelope (explicit considerations, assumptions, clarifying
questions) may remain a **structural tell** even after labels are stripped, so this
procedure mitigates but does not eliminate all bias. The lift decision rule
(`docs/evals/LIFT_DECISION_RULE.md`) is what gates a "win" on material content
rather than on the presence of an envelope or on output volume.

## Procedure

1. Generate the two outputs for a prompt under comparable configuration. (Running
   the comparison is out of scope for this lane.)
2. Assign `Output A` and `Output B` to plain/alpha by a recorded random method or
   seed. Record the assignment in `docs/evals/templates/blinding_map_template.csv`
   (a file kept separate from the judge-facing score sheet).
3. Normalize obvious tells: strip brand and provider names; neutralize section
   headings; keep the substance of any considerations/assumptions as plain prose so
   content — not format — is judged.
4. Capture sanitized answer text and length for each output using
   `docs/evals/templates/paired_output_capture_template.md`.
5. Score all 14 rubric dimensions for `Output A` and `Output B` using
   `docs/evals/templates/blinded_score_sheet_template.csv`. The judge-facing sheet
   must not contain Alpha or Plain labels.
6. Only after scores are recorded, unblind via the mapping file and transfer scores
   into `docs/evals/templates/comparison_score_table_template.csv`.
7. Apply `docs/evals/LIFT_DECISION_RULE.md` to compute `lift_delta`, `polish_delta`,
   `lift_qualified`, and `polish_only_flag`.

## Non-claims

This procedure is an internal review aid only. It:

- does not validate the MVP;
- does not prove Alpha Solver superiority;
- does not prove answer-quality superiority;
- does not prove production readiness;
- does not prove broad runtime readiness;
- does not prove benchmark success;
- does not prove exact billing accuracy;
- does not prove provider reasoning orchestration.
