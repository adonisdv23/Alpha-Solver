# Unacceptable UX

The earliest Self Operator MVP is not acceptable if any of the following UX patterns are present:

- Starts running without an explicit operator approval moment.
- Uses vague approval copy such as `continue` without naming the action and boundary.
- Hides or omits the no-provider-call boundary.
- Silently calls hosted providers, uses credentials, bills, or falls back to external models.
- Shows running status without a visible stop option or stop instruction.
- Fails to distinguish blocked, failed, stopped, and completed states.
- Omits artifact locations after completion, stop, or block when artifacts exist.
- Treats partial artifacts as final without review copy.
- Continues after a blocked preflight result.
- Uses implementation-success language for this docs-only packet.
- Implies dashboard, CLI, runtime, or Self Operator behavior has been implemented by this packet.
