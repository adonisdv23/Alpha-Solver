# First-use review input

The controlling input is the first supervised-use review packet:

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-review/`

Key first-use review inputs for repeatability comparison:

| Field | First-use value to compare later |
| --- | --- |
| Review decision | `accepted_for_limited_repeatability_review` |
| Selected next lane | `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-LIMITED-REPEATABILITY-PACKET-001` |
| P0/P1/P2 status | none unresolved |
| Wrapper result | wrapper classified the proposed command text and did not execute it |
| Gate status | `allowed_for_local_dry_run_wrapper` in imported dry-run/gate artifacts |
| Command classification reason | local deterministic packet consistency checker classification in imported artifacts |
| Release-gate checker | exited 0 in first supervised-use execution evidence |
| Packet consistency checker | exited 0 in first supervised-use execution evidence |
| Stop state | `none` |
| Source-artifact mutation | none recorded |
| Forbidden-surface proof | non-execution proof recorded no forbidden surface execution |
| Redaction | redaction review passed |
| Raw artifact inventory | raw output index and imported artifact index preserved |

The future repeatability execution lane must compare against these reviewed
first-use values without changing the first-use packet.
