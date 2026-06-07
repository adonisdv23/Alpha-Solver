# Decision Options Reviewed

## Option 1: ADD_STABLE_CLI_WRAPPER

Decision status: `SELECTED`.

This option adds a future stable operator-facing CLI wrapper for Level 2 local use. It is justified because the repository already has a non-production local orchestration module entry point and operator guide templates, but no stable command surface. A narrow wrapper can make operator use more repeatable while preserving the existing safety boundary.

The wrapper must remain local-only, default-off, explicit opt-in, loopback endpoint only, finite timeout, no hosted provider keys required, no hosted fallback, `behavior_evidence=false`, no `/v1/solve` exposure, no dashboard exposure, no provider fallback, and no evidence-model promotion.

## Option 2: KEEP_MODULE_ENTRYPOINT_ONLY

Decision status: `NOT_SELECTED`.

The module entry point is adequate for implementation tests and expert developer inspection, but it is not the best Level 2 operator surface because the current guide must provide a heredoc Python template instead of a stable command. Keeping only the module entry point would preserve safety, but it would leave the operator usability gap identified by the source guide unresolved.

## Option 3: ADD_OPERATOR_SCRIPT_TEMPLATE_ONLY

Decision status: `NOT_SELECTED`.

A script/template would be narrower than a formal CLI, but it would still leave command identity, argument shape, output formatting, and safety messaging less stable than a repository-owned wrapper. Because the allowed behavior can be tightly bounded and because the existing runner already centralizes the local safety gates, a stable wrapper is preferable to a reusable ad hoc template.

## Option 4: BLOCKED_REQUIRES_SPEC_OR_SURFACE_REVIEW

Decision status: `NOT_SELECTED`.

The repository has enough contract clarity to choose the CLI path safely. The runtime integration spec defines local-only, default-off, opt-in, loopback, finite-timeout, no-provider-key, no-hosted-fallback, and `behavior_evidence=false` requirements. The solver orchestration spec blocks `/v1/solve`, dashboard, hosted fallback, evidence-model promotion, model-quality claims, MVP adoption, production readiness claims, benchmark claims, Alpha superiority claims, provider-orchestration claims, and billing changes.
