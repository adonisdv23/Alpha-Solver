# Operator Behavioral Demo Evidence Template

## Purpose

Use this copyable template to record summarized evidence from the
[Operator Behavioral Demo Checklist](OPERATOR_BEHAVIORAL_DEMO_CHECKLIST.md) and
the [Operator Demo Run Packet](OPERATOR_DEMO_RUN_PACKET.md) for Alpha Solver MVP
preview runs. The template is for manual operator notes only.
It does not create storage, run automated evaluations, validate the MVP, prove
Alpha Solver superiority, prove production readiness, prove answer-quality
benchmark success, or prove provider reasoning orchestration.

## Safety and secret-handling rules

Do not store or paste any of the following in this template or in repo-tracked
evidence:

- raw provider request payloads;
- raw provider response payloads;
- full raw model outputs as required evidence;
- headers;
- cookies;
- session values;
- CSRF tokens;
- API keys;
- dashboard passwords;
- provider account identifiers;
- secrets, credentials, or token values of any kind.

Summarize behavior in your own words. Redact or summarize Cloud Run URLs when
needed, for example `https://alpha-solver-preview-...run.app` or
`preview service, project redacted`.

## Copyable evidence block

Copy one block per prompt or per prompt pair. Keep notes short and conservative.

```text
# Alpha Solver operator behavioral demo evidence

## 1. Run metadata

Run ID:
Date/time UTC:
Operator:
Environment:
Cloud Run URL or environment label, summarized/redacted if needed:
Mode: local-provider smoke / controlled live-provider / side-by-side comparison
Provider/model if known, otherwise unknown:
If live mode was used, service returned to MODEL_PROVIDER=local: yes / no / n/a

## 2. Prompt record

Prompt ID from checklist:
Prompt text or short prompt summary:
Reason this prompt was selected:
Expected behavior target:

## 3. Output summaries only

Plain provider output summary:
Alpha Solver expert preview summary:

Do not paste raw provider payloads, raw full outputs, headers, cookies, session
values, CSRF tokens, API keys, dashboard passwords, or secrets here.

## 4. Manual scoring table

Score each criterion from 0 to 2.
0 = missing, harmful, or materially misleading.
1 = partially useful but incomplete, noisy, vague, or weakly bounded.
2 = useful, concrete, bounded, and appropriate for the operator task.

| Criterion | Plain output score (0-2) | Alpha Solver score (0-2) | Notes |
| --- | --- | --- | --- |
| Hidden constraints |  |  |  |
| Intent preservation |  |  |  |
| Concrete next actions |  |  |  |
| Unsupported-claim avoidance |  |  |  |
| Clarifying-question discipline |  |  |  |
| Useful structure |  |  |  |
| Claim-boundary respect |  |  |  |
| Assumption visibility |  |  |  |
| Operator confidence |  |  |  |
| Practical usefulness |  |  |  |

Plain provider total: __ / 20
Alpha Solver total: __ / 20
Delta: __
Operator preference: plain / Alpha Solver / tie / inconclusive

## 5. Defects and follow-up

UI defect found? yes / no / unsure
Runtime defect found? yes / no / unsure
Prompt/routing weakness found? yes / no / unsure
Documentation confusion found? yes / no / unsure
Suggested backlog item:
Severity: low / medium / high / blocking / n/a
Evidence summary:
Owner or next reviewer, if known:

## 6. Conservative interpretation

Select one:
[ ] Inconclusive
[ ] Promising, needs more runs
[ ] Weak, needs prompt/routing improvement
[ ] Defect found, create ticket
[ ] Do not use for claims

Interpretation notes:

## 7. Claim boundaries

Confirm each statement remains true for this evidence:
[ ] One run is not validation.
[ ] This evidence does not prove Alpha Solver superiority.
[ ] This evidence does not prove MVP validation.
[ ] This evidence does not prove production readiness.
[ ] This evidence does not prove answer-quality benchmark success.
[ ] This evidence does not prove provider reasoning orchestration.
```

## Operator reminders

- Use this as a manual triage aid, not a benchmark result.
- Prefer short behavior summaries over copied output.
- If the run exposes a defect, create a ticket or backlog item outside this
  template and include only a safe summary.
- If live provider mode was used, confirm rollback to `MODEL_PROVIDER=local`
  before ending the run.
- Do not update Google Sheets or backlog workbooks from this repo task.
