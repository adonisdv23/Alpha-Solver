# First Cheap Test

## Test

Select one committed evidence packet and draft a one-page internal demo narrative using `demo-one-pager-template.md`. Then run a manual claim audit against `reviewer-checklist.md`, `forbidden-claims.md`, and `non-claims.md`.

## Pass condition

The test passes only if:

- every positive statement maps to a committed source path;
- every missing artifact or unsupported capability is disclosed;
- no forbidden claim appears directly or by implication;
- a reviewer can remove the source packet and immediately identify that the narrative would no longer be supported.

## Fail condition

The test fails if the one-pager can be read as proof of value, readiness, superiority, runtime capability, provider validation, local-model validation, dashboard readiness, public API readiness, `/v1/solve` readiness, or market/customer validation.

## Output

The output should be a redlined one-pager and a short reviewer note. No code, UI, runtime, model, provider, dashboard, API, or Google Sheets work is part of this test.
