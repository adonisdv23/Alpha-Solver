# Future Capture Instructions

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: future capture rules only. No capture is run by this packet.

## Pre-capture checklist

Before any later capture task starts, confirm all of the following:

- The frozen packet PR has been reviewed and merged.
- Capture is separately authorized after merge.
- The operator is using the merged repository version of `alpha_solver_portable.py`.
- The prompt text in `frozen-prompt-packet.md` is unchanged.
- The Alpha condition explicitly loads `alpha_solver_portable.py`.
- The plain condition excludes Alpha Solver context and the portable contract.
- Provider/model/tool settings are identical across conditions.
- No `/v1/solve` path is used unless separately proven and authorized.
- Raw output storage location is prepared.
- Operator-only map storage location is prepared separately from scorer-facing material.

## Model/provider parity requirement

Both conditions must use the same provider, model, temperature or equivalent sampling policy, tool policy, and any other generation setting authorized by the future capture task.

If parity cannot be confirmed, stop capture and document the mismatch.

## Raw output preservation rules

- Preserve each raw output exactly as returned.
- Do not edit, polish, normalize, summarize, score, or shorten raw outputs.
- Preserve empty, malformed, or unexpectedly structured outputs as-is.
- Preserve technical failure records separately from successful raw outputs.
- Do not commit raw provider payloads, secrets, request headers, cookies, account identifiers, or private runtime traces unless a later task explicitly defines a sanitized artifact path.

## Sanitized scorer-facing render

Raw output preservation and scorer-facing sanitization are separate artifacts. Raw outputs must remain exact and must never be edited. A later scoring-prep task may create a separate sanitized scorer-facing render only for blind scoring.

The sanitized render must follow `docs/evals/BLIND_SCORING_PROCEDURE.md`: strip brand and provider names, neutralize section headings, and preserve substantive content as plain prose. Sanitization may strip or neutralize direct brand, provider, route, condition, and obvious envelope or heading tells, including pipeline-confirmation branding.

Sanitization must not remove substantive content, caveats, reasoning, risks, assumptions, recommendations, or answer-quality defects. It must be applied symmetrically to both outputs. If direct tells cannot be removed without substantive rewriting, the scorer packet is invalid and the future task must stop before scoring.

The future capture or scoring-prep task must preserve a sanitization log or checklist outside the scorer-facing packet. That log is operator-only material and must not be sent to the blind scorer.

## During-capture prohibitions

- Do not score during capture.
- Do not unblind during capture.
- Do not update Google Sheets during capture.
- Do not start Batch C.
- Do not make broad validation, superiority, readiness, benchmark, billing, or provider-coordination claims.
- Do not change runtime, provider, model, routing, scoring rubric, capture script, or `/v1/solve` behavior.

## Technical failure retry rules

A retry is allowed only for documented technical failure, such as request timeout, provider outage, transport failure, or empty response caused by a confirmed platform error.

For every retry, record:

- comparison ID;
- prompt ID;
- condition slot before blinding, if known to operator-only records;
- failure timestamp;
- failure type;
- whether any partial output was received;
- retry timestamp;
- final output path or final failure note.

Do not retry for disliked content, weak quality, excessive length, inconvenient formatting, or scoring concerns.

## Future output filename conventions

Use these names only in a later authorized capture task:

```text
raw-outputs/<comparison_id>-<prompt_id>-alpha.txt
raw-outputs/<comparison_id>-<prompt_id>-plain.txt
technical-failures/<comparison_id>-<prompt_id>-<condition>-failure.md
operator-log.csv
```

The future blinded scorer packet should reference only `Output A` and `Output B`, not these condition filenames.

## Operator log fields

A future `operator-log.csv` should include:

```text
comparison_id,prompt_id,condition,captured_at,provider_or_model_label_for_operator_only,tool_policy,source_prompt_hash,raw_output_path,technical_failure,retry_count,operator_notes
```

If provider/model labels are considered scorer-contaminating, keep them operator-only and exclude them from scorer-facing material.

## Stop conditions for capture operator

Stop the future capture task if any of these occur:

- The frozen prompt text differs from this packet.
- The Alpha condition cannot load `alpha_solver_portable.py`.
- The plain condition includes Alpha context or improvement instructions.
- Provider/model parity cannot be confirmed.
- The task would require browsing or tools without explicit authorization.
- The task would score, unblind, or update Sheets during capture.
- The task would start Batch C.
- The task would depend on `/v1/solve` without approved proof that it consumes `alpha_solver_portable.py`.
- Raw output preservation is unavailable.
- A sanitized scorer-facing render cannot be produced without substantive rewriting.
- The scorer-facing packet contains direct condition labels, Alpha Solver branding, provider/model branding, route identity, runtime metadata, repo paths, raw output paths, pipeline confirmation branding, or unblinding-map details.
- Assignment or operator-only metadata leaks into scorer-facing material.
