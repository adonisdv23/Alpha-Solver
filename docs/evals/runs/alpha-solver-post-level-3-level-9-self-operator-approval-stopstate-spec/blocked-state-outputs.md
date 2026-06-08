# Blocked-state outputs

A blocked state should output only:

- Stop-state code.
- Local path or scope that triggered the block.
- Human-readable reason.
- Safe next action.
- Whether operator review is required.

Blocked-state outputs must not include secrets, provider outputs, external API responses, browser data, billing data, deployment output, or evidence-promotion labels.
