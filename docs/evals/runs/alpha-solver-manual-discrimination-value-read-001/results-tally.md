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
| Scored tasks | 0 |

Simulation verdict: none captured in this commit.

## Runtime tally

Track R status: `not run / blocked`.

Reason: existing no-echo packet reports prompt echo, and no provider authorization was supplied.

| Metric | Count |
| --- | ---: |
| Alpha runtime wins | 0 |
| Baseline runtime wins | 0 |
| Ties | 0 |
| Scored tasks | 0 |

Runtime verdict: `BLOCKED_NO_ECHO_PROOF_MISSING` and `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`.

## Allowed future result labels

If a future operator run produces preserved outputs and scores, use only the allowed labels:

- `VALUE_READ_SIMULATION_CAPTURED_NON_DECISIVE`
- `VALUE_READ_RUNTIME_CAPTURED_NON_DECISIVE`
- `VALUE_READ_SIGNAL_FAVORS_DISCRIMINATION_NON_DECISIVE`
- `VALUE_READ_SIGNAL_WITHIN_NOISE`
- `BLOCKED_NO_ECHO_PROOF_MISSING`
- `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`
- `STOP_INCONCLUSIVE`
