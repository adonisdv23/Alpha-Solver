# Weight Tuning Harness

The lightweight harness in `service.tuning.weight_harness` performs a small
random search over weight vectors and reports the improvement over the current
configuration.  It is deterministic given a seed and requires only the standard
library.

## Running

```bash
python -m service.tuning.weight_harness \
  --scenarios data/datasets/routing/scenarios_routing.jsonl \
  --out artifacts/weights.json
```

The command prints a textual report and stores the normalised weights in the
specified output file.

## Choosing a search space

The harness samples the unit simplex uniformly.  Increase `--samples` to explore
more candidates or adjust the seed for different deterministic sequences.

## Interpreting output

The report displays BEFORE and AFTER accuracy as well as per-factor deltas.  If
the best candidate improves accuracy by less than five percentage points the
process terminates early and `no_gain: true` is returned.
