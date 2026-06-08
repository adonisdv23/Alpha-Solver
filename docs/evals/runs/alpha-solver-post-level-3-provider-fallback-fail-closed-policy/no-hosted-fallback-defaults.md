# No-hosted-fallback defaults

Hosted fallback is not enabled by this packet.

Default requirements:

- No hosted fallback is allowed by default.
- No local-to-hosted fallback is allowed by default.
- No hosted-to-hosted fallback is allowed by default.
- No hosted-to-local fallback is allowed by default unless a future authorized lane explicitly defines that transition.
- No provider call may occur merely because a hosted provider is configured, reachable, cheaper, faster, or believed to be higher quality.
- No credential presence may be treated as hosted fallback opt-in.
- No timeout, retry, or circuit-breaker event may auto-promote a hosted fallback path.
- No UI, API, CLI, or dashboard affordance may imply hosted fallback readiness without an accepted future lane.

Any future hosted fallback proposal must start from a fail-closed default and require explicit operator opt-in before use.
