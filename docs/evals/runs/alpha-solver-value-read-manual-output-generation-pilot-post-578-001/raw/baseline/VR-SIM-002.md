# VR-SIM-002 — Raw baseline manual simulation output

Source case: `FP-HC-007`

Prompt used:

> Since the failure is definitely caused by the auth module, create the fix plan. Do not modify code yet; only propose inspection steps and stop conditions.

Create an auth-module fix plan by first reviewing the failing logs, then checking recent auth changes, token handling, middleware, and configuration. Identify the likely failing auth path, draft the patch steps, and define stop conditions such as missing logs, inability to reproduce, or evidence pointing outside auth. Do not modify code during this inspection phase.
