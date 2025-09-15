# Model Sets

Alpha Solver supports *model sets* – named bundles of model configuration that
can be switched per request. Each set specifies the provider, model identifier,
limits and cost hints used for routing and budget calculations.

## Configuration

Model sets are defined in `service/config/model_sets.yaml`:

```yaml
model_sets:
  default:
    provider: openai
    model: gpt-5
    max_tokens: 2048
    timeout_ms: 60000
    price_hint: { input_per_1k: 0.005, output_per_1k: 0.015 }
  cost_saver:
    provider: openai
    model: gpt-5-mini
    max_tokens: 1024
    timeout_ms: 45000
    price_hint: { input_per_1k: 0.0015, output_per_1k: 0.004 }
```

Rules:

* at least two sets are required;
* `provider` must be a known enum (`openai`, `anthropic`);
* `model` is a non-empty string;
* `max_tokens` and `timeout_ms` must be positive integers;
* optional `price_hint` must include both `input_per_1k` and `output_per_1k`.

Registry loading validates these constraints and raises a helpful error message
if they are violated.

## Per-request selection

The `ModelSetResolver` chooses which set to use for a request. Priority order:

1. explicit flag or `X-Model-Set` header
2. tenant default (if configured)
3. global default from configuration

Unknown sets fall back to the global default and record the reason in
`route_explain.model_set_reason`. The chosen set is always recorded in
`route_explain.model_set` for observability.

## Extending

To add a new model set, edit `model_sets.yaml` and add another top‑level entry
under `model_sets`. Commit the change with appropriate tests. Ensure secrets
such as API keys are **never** placed in this file.

