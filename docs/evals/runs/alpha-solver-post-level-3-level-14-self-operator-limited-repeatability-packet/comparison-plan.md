# Comparison plan

A future repeatability execution lane must compare its evidence against the
first supervised-use evidence packet without mutating either packet.

## Required comparison fields

| Field | Comparison requirement |
| --- | --- |
| `approval validation status` | Compare whether required labels and confirmation text were present and accepted. |
| `identity_match` | Compare whether operator identity checks matched the approved local-supervised boundary. |
| `gate_status` | Compare wrapper gate status to the first-use allowed local dry-run wrapper status. |
| `wrapper non-execution marker` | Compare proof that wrapper classified command text and did not execute it. |
| `command classification reason code` | Compare classification reason for the deterministic packet consistency checker command. |
| `release-gate checker exit` | Compare exit code and output presence. |
| `packet consistency checker exit` | Compare exit code and output presence. |
| `stop_state` | Compare stop-state result; successful repeatability expects no stop state. |
| `source-artifact mutation check` | Compare no-mutation proof. |
| `redaction review` | Compare redaction pass/fail and any findings. |
| `raw artifact inventory shape` | Compare presence and structure of required raw artifacts. |
| `forbidden-surface non-execution proof` | Compare proof that forbidden surfaces were not reached. |

## Allowed comparison outcomes

A future execution lane may report only one of these outcomes:

- `repeatability_comparable` — all required fields are present and materially
  comparable to the first supervised use within the same local-only boundary.
- `repeatability_blocked` — execution stopped, required evidence is missing, or
  a forbidden surface or mutation concern prevents comparison.
- `repeatability_inconclusive` — evidence exists but is insufficient to decide
  comparability without overclaiming.

## Non-claims

The comparison must not claim product readiness, runtime readiness, provider
readiness, external validation, superiority, or broader user suitability. It is
only a bounded repeatability comparison of a local evidence-review pattern.
