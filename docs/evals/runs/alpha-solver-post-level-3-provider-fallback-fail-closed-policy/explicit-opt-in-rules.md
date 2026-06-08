# Explicit opt-in rules

Any future fallback behavior requires explicit operator opt-in before it can be used.

Minimum opt-in requirements for a future authorized lane:

- name the exact fallback transition being allowed;
- name whether the transition is local-to-local, local-to-hosted, hosted-to-hosted, or hosted-to-local;
- name the provider identities and capability boundaries involved;
- record credential boundary acknowledgement before provider use;
- record cost boundary acknowledgement before provider use;
- record provenance and audit fields required for reconstruction;
- record safety and claim-gate boundaries for outputs produced after fallback;
- record stop conditions that override the opt-in;
- require opt-in to be current, scoped, revocable, and auditable.

A broad setting, environment variable, provider registry entry, available API key, dashboard preference, CLI flag, or prior evidence packet must not count as opt-in unless a future authorized lane explicitly defines and accepts that mechanism.
