# Telemetry Schema v1

All telemetry events emitted by Alpha Solver include the following base fields:

- `event`
- `ts`
- `run_id`
- `schema_version` (currently `1.0.0`)

Additional fields are required per event type:

| event              | required fields                                  |
|--------------------|--------------------------------------------------|
| `tot_layer`        | `layer`, `depth`                                 |
| `tot_candidate`    | `candidate`, `score`                             |
| `router_escalate`  | `from`, `to`                                     |
| `safe_out_decision`| `route`, `conf`, `threshold`, `reason`           |
| `run_summary`      | `counts`, `final_route`, `final_confidence`      |
| `error`            | `type`, `message`                                |

The helper `alpha.reasoning.logging.validate_event` can be used in tests to
verify that emitted events conform to this schema.
