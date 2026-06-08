# Failure-state behavior

Future Self Operator code must fail closed. It must stop when approval is missing, scope is unclear, branch state is unsafe, changed files exceed allowed scope, or any forbidden surface is detected.

Failure must not trigger fallback, hosted fallback, retries against providers, browser automation, deployment, billing, route exposure, source-artifact mutation, or evidence promotion.
