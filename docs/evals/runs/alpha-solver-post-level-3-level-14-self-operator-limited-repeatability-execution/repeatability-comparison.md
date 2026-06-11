# Repeatability comparison

Outcome: `repeatability_comparable`.

| Field | First supervised use | Repeatability run | Decision |
| --- | --- | --- | --- |
| approval validation status | valid | valid | comparable |
| identity_match | true | true | comparable |
| gate_status | allowed_for_local_dry_run_wrapper | allowed_for_local_dry_run_wrapper | comparable |
| wrapper non-execution marker | present | present | comparable |
| command classification reason code | allowed_local_read_check | allowed_local_read_check | comparable |
| release-gate checker exit | 0 | 0 | comparable |
| full packet consistency checker exit | 0 | 0 | comparable |
| packet-scoped consistency checker exit | not required in first use | 0 | comparable for this packet's expanded plan |
| stop_state | none | none | comparable |
| source-artifact mutation check | pass | pass for prior source evidence, code, and tests | comparable |
| redaction review | pass | pass | comparable |
| raw artifact inventory shape | expected first-use shape | expected repeatability shape with both consistency outputs | comparable |
| forbidden-surface non-execution proof | present | present | comparable |

This comparison is bounded to repeatability of the local evidence-review pattern. It does not claim benchmark evidence, superiority, or readiness.
