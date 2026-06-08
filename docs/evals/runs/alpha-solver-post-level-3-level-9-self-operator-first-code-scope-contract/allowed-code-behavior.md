# Allowed code behavior

The future first-code lane may introduce only the narrow code behavior described here. The default is static test scaffold only unless the controlling Level 9 packet explicitly says otherwise.

## Allowed behavior

- Add static tests that **detect prohibited Self Operator behavior** and fail if that behavior is present.
- Assert that prohibited surfaces are absent, refused, or not wired: no provider calls, no external API calls, no route exposure, no credential use, no browser automation, no deployment, no billing, and no fallback.
- Load and read **inert fixtures** to drive those assertions.
- Use deterministic, offline test logic only.
- Skip or mark expected-failure when a runtime surface is intentionally absent, rather than creating that surface.

## Behavior conditions

- Tests must not import or execute runtime Self Operator behavior in order to observe it.
- Tests must not reach the network, start a model, start a provider, or read secrets.
- Tests are scaffolding that observes boundaries from the outside; they do not implement the boundaries' runtime.

Anything beyond detecting prohibited behavior with static tests and inert fixtures is governed by `forbidden-code-behavior.md`.
