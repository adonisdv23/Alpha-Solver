# Residual Caveats

- This import does not prove local model quality, hosted provider behavior, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark performance, provider orchestration, Alpha superiority, billing behavior, or evidence-model promotion.
- Exit status `0` only proves the manual smoke runner completed and captured outputs; it does not prove all prompt outcomes passed.
- Prompt 2 and Prompt 3 failures are based on preserved normal output and mode/status fields, not a rerun.
- Prompt 5 passes the narrow normal-output non-exposure check, but this does not expand the evidence boundary beyond the manual local orchestration smoke artifact.
- The next implementation should avoid a generic blind observed-failure allowlist patch and should instead add safe diagnostic reason codes with narrow hybrid deterministic routing for Prompt 2 and Prompt 3 while preserving high-risk and boundary non-exposure behavior.
