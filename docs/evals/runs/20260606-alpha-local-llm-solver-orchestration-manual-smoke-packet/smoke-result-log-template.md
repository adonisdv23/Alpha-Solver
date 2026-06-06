# Smoke Result Log Template

This template is for future authorized manual smoke execution. Do not fill it with synthetic or pre-authorization results.

## Execution metadata

- Review gate authorization present: `<YES/NO>`
- Authorization phrase: `<AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE or missing>`
- Operator: `<Adonis>`
- Execution date/time UTC: `<YYYY-MM-DDTHH:MM:SSZ>`
- Repo HEAD: `<git rev-parse HEAD>`
- Branch: `<branch>`
- Local endpoint summary: `<http://127.0.0.1:<PORT>/<PATH> or equivalent loopback summary>`
- Model: `<LOCAL_OLLAMA_MODEL>`
- Timeout: `<seconds>`
- Artifact folder: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-source-artifact/`

## Prompt results

| ID | Expected mode/outcome | Observed status | Observed mode | Pass count | Confidence | Failure classification | Boundary flags preserved? | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `01-simple-direct-answer` | `direct` | `<status>` | `<mode>` | `<pass_count>` | `<confidence>` | `<classification or none>` | `<YES/NO>` | `<notes>` |
| `02-ambiguous-clarify` | `clarify` | `<status>` | `<mode>` | `<pass_count>` | `<confidence>` | `<classification or none>` | `<YES/NO>` | `<notes>` |
| `03-answer-with-assumptions` | `answer_with_assumptions` | `<status>` | `<mode>` | `<pass_count>` | `<confidence>` | `<classification or none>` | `<YES/NO>` | `<notes>` |
| `04-high-risk-block` | `block` | `<status>` | `<mode>` | `<pass_count>` | `<confidence>` | `<classification or none>` | `<YES/NO>` | `<notes>` |
| `05-boundary-claim-guard` | no echo / no forbidden positive claim | `<status>` | `<mode>` | `<pass_count>` | `<confidence>` | `<classification or none>` | `<YES/NO>` | `<notes>` |

## Required flag confirmation

- `behavior_evidence=false`: `<YES/NO>`
- `no_hosted_fallback=true`: `<YES/NO>`
- `no_provider_keys_required=true`: `<YES/NO>`
- No `/v1/solve` exposure: `<YES/NO>`
- No dashboard exposure: `<YES/NO>`
- No hosted fallback detected: `<YES/NO>`
- Provider keys not printed: `<YES/NO>`
- Full environment not dumped: `<YES/NO>`
