# Artifact File Inventory Schema

## Purpose

Future quality eval execution packets should include an inventory that makes every artifact discoverable and classifies each file as raw, derived, decision, check, or administrative content.

## Required inventory columns

| Field | Required | Description |
| --- | --- | --- |
| `artifact_id` | Yes | Stable unique identifier for the file within the packet. |
| `relative_path` | Yes | Repo-relative path or packet-relative path to the artifact. |
| `artifact_type` | Yes | One of `raw_output`, `reviewer_note`, `scoring_record`, `redaction_log`, `final_decision`, `checks_run`, `metadata`, or `non_action`. |
| `source_raw_output_id` | Conditional | Required for reviewer notes, scoring records, redaction logs, and final decisions that cite specific raw outputs. |
| `created_by_role` | Yes | Operator, reviewer, scorer, automation, or Level 5 approver role. |
| `created_at_utc` | Yes | UTC timestamp in ISO 8601 format. |
| `sha256` | Conditional | Required for immutable raw outputs and recommended for final decision files. |
| `redaction_state` | Yes | `none`, `redacted_derivative`, `raw_sensitive_restricted`, or `not_applicable`. |
| `validity_state` | Yes | `valid`, `invalid`, `incomplete`, `superseded`, `blocked`, or `quarantined`. |
| `notes` | Optional | Short inventory-specific notes; not a substitute for reviewer notes. |

## Required future artifact files

A future packet adopting this schema should inventory at least these file groups:

1. Packet overview and run metadata.
2. Raw output captures in `raw-outputs/`.
3. Raw-output preservation ledger.
4. Reviewer notes.
5. Scoring records or explicit no-scoring record.
6. Invalid-result marker ledger.
7. Redaction log.
8. Final decision file.
9. Checks-run file.
10. Non-actions confirmation.

## Inventory rules

- Raw outputs must be inventoried before scoring records claim them as source material.
- Derived artifacts must refer to raw outputs by `artifact_id` and path.
- Invalid and blocked artifacts remain in the inventory with their invalid-result markers.
- Deleted or replaced files must be recorded as `superseded` rather than disappearing from the inventory.
