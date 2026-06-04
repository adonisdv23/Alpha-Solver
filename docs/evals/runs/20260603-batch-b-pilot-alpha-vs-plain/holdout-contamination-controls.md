# Holdout Contamination Controls

Status: future evaluation planning only

Lane: `OUTPUT-DIFF-COMPLEXITY-GRADIENT-HOLDOUT-PLAN-001`

This document defines controls for a possible future complexity-gradient holdout. It does not create final prompts, run capture, score outputs, rescore existing outputs, change runtime behavior, call providers, update external planning ledgers, or start Batch C.

## Why prompt exposure matters

A future holdout is only useful if the exact prompt text is not used to tune, rehearse, or optimize Alpha before capture. Exposing final prompts too early can blur the difference between general behavior improvement and overfit to the evaluation packet. The current task therefore uses prompt-free slot planning only.

## Prompt-free slot planning

The companion slot matrix describes:

- headroom level;
- prompt family;
- target capability;
- risk flags;
- expected Alpha engagement;
- diagnostic question;
- scorer bias risk;
- contamination control.

It does not include final user prompts, final scorer prompts, final expected outputs, provider payloads, request metadata, response metadata, credentials, or raw captures.

## Freeze-before-capture rule

Before any future capture:

1. Create a separate frozen prompt-packet PR.
2. Include final prompt text only in that frozen packet.
3. Record prompt IDs, prompt-family metadata, and headroom metadata in an operator-only map if metadata could bias scoring.
4. Review and approve the packet before any capture begins.
5. Do not edit prompt text after capture starts except through a new approved freeze.

## Scorer blinding rule

A future scorer-facing packet should preserve blinded candidate labels and avoid revealing whether an output came from Alpha or plain. If headroom level or prompt family metadata could bias scoring, keep that metadata out of the scorer packet until scoring is complete.

## Unblinding separation rule

Do not unblind candidate identity before scoring is complete. Preserve the scorer-facing packet, score sheet, defects, and blinding map separately. Unblinding should be a separate post-scoring step with a recorded check that totals and preferences were computed from committed artifacts.

## No training or tuning on future prompt text

Do not train, tune, manually optimize, or implement prompt-specific behavior against the exact future holdout prompts. Planning may define families, risks, and slot properties, but final prompt text must not become behavior-development input before the frozen evaluation.

## No raw provider payload leakage

Do not include raw provider payloads in planning, scorer-facing, or public evaluation artifacts. If future capture is approved, preserve sanitized outputs and the minimum metadata needed for reproducibility while excluding raw payload material, credentials, private identifiers, and provider-internal metadata.

## No Sheet-as-proof issue

External spreadsheets may be planning ledgers, but they are not proof of implementation or scoring. Future evaluation claims must cite committed repository artifacts, including the frozen prompt packet, captured outputs, blinded score sheet, score table, defects, and preservation checks.

## Final packet creation requirements

A later frozen prompt-packet PR should include:

- final prompt text;
- prompt IDs;
- scorer-facing packet;
- operator-only mapping file;
- artifact preservation checklist;
- blinding procedure;
- stop conditions;
- confirmation that no capture has started;
- confirmation that no scoring has started;
- non-claims and scope limits.

The final packet should not be created by the same task that performs scoring. Prompt writing and scoring should remain separate responsibilities.

## Stop conditions

Stop before creating or running a future holdout if any of the following are true:

- required committed evidence cannot be inspected;
- Batch B or A3-1 score math cannot be recomputed from committed CSVs;
- final prompt text would be exposed before an approved freeze;
- capture would need to begin before the frozen packet is approved;
- scorer blinding cannot be preserved;
- unblinding would happen before scoring is complete;
- the task would require live provider calls without explicit authorization;
- the task would require rescoring existing outputs;
- the task would require runtime, provider, model, routing, or scoring-rubric changes;
- the task would require external spreadsheet updates as implementation proof;
- the task would require Batch C;
- the task would require broad validation, superiority, benchmark, production-readiness, exact-billing, or provider-orchestration claims.
