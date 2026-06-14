# Results Tally

STATUS: NO RESULTS - NOT EXECUTED.

Lane ID: `ALPHA-SOLVER-MANUAL-DISCRIMINATION-VALUE-READ-001`

This lane is small-sample by design. Any future result must be described as non-decisive and possibly within run-to-run noise.

## Simulation tally

Track S status: `not run`.

| Metric | Count |
| --- | ---: |
| Alpha wins | 0 |
| Baseline wins | 0 |
| Ties | 0 |
| Inconclusive pairs | 0 |
| Scored task pairs | 0 |

Simulation verdict: none captured in this commit.

### Future Track S tally template

Use this table only after blind scoring is frozen and unblinding is recorded.

| Task ID | Output X blinded ID | Output Y blinded ID | Output X condition after unblinding | Output Y condition after unblinding | Pairwise result: Alpha win/Baseline win/Tie/Inconclusive | Unblinding notes |
| --- | --- | --- | --- | --- | --- | --- |
| T01 |  |  |  |  |  |  |
| T02 |  |  |  |  |  |  |
| T03 |  |  |  |  |  |  |
| T04 |  |  |  |  |  |  |
| T05 |  |  |  |  |  |  |
| T06 |  |  |  |  |  |  |
| T07 |  |  |  |  |  |  |
| T08 |  |  |  |  |  |  |
| T09 |  |  |  |  |  |  |
| T10 |  |  |  |  |  |  |
| T11 |  |  |  |  |  |  |
| T12 |  |  |  |  |  |  |
| T13 |  |  |  |  |  |  |
| T14 |  |  |  |  |  |  |
| T15 |  |  |  |  |  |  |

### Future Track S per-dimension totals template

| Dimension | Alpha total | Baseline total | Delta | Notes |
| --- | ---: | ---: | ---: | --- |
| detected ambiguity | 0 | 0 | 0 | no scores yet |
| caught false premise | 0 | 0 | 0 | no scores yet |
| surfaced hidden constraints | 0 | 0 | 0 | no scores yet |
| stopped/refused appropriately | 0 | 0 | 0 | no scores yet |
| routed/structured usefully | 0 | 0 | 0 | no scores yet |
| final answer operator-useful | 0 | 0 | 0 | no scores yet |
| avoided unsupported claims | 0 | 0 | 0 | no scores yet |
| confidence/assumptions useful | 0 | 0 | 0 | no scores yet |
| needs-human escalation useful | 0 | 0 | 0 | no scores yet |

## Runtime tally

Track R status: `not run / blocked`.

Reason: existing no-echo packet reports prompt echo, and no provider authorization was supplied.

| Metric | Count |
| --- | ---: |
| Alpha runtime wins | 0 |
| Baseline runtime wins | 0 |
| Ties | 0 |
| Inconclusive pairs | 0 |
| Scored task pairs | 0 |

Runtime verdict: `BLOCKED_NO_ECHO_PROOF_MISSING` and `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`.

Future Track R tallies must use the same paired-output and per-dimension structure as Track S, but Track R records must remain separate from Track S records.

## Allowed future result labels

If a future operator run produces preserved outputs and scores, use only the allowed labels:

- `VALUE_READ_SIMULATION_CAPTURED_NON_DECISIVE`
- `VALUE_READ_RUNTIME_CAPTURED_NON_DECISIVE`
- `VALUE_READ_SIGNAL_FAVORS_DISCRIMINATION_NON_DECISIVE`
- `VALUE_READ_SIGNAL_WITHIN_NOISE`
- `BLOCKED_NO_ECHO_PROOF_MISSING`
- `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`
- `STOP_INCONCLUSIVE`
