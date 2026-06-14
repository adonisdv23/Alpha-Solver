# Local-Only Runbook

This runbook is for a future implementation lane. It is not evidence that a bridge exists today.

## Preconditions

- Workstation is trusted by the operator.
- Repository checkout is clean and on the intended branch.
- Bridge implementation has an explicit spec and tests.
- No remote exposure has been enabled.

## Future smoke flow

1. Start the bridge with loopback binding only.
2. Confirm the bind address is `127.0.0.1` or equivalent local-only loopback.
3. Capture the short-lived startup token from the local terminal.
4. Connect the operator console from the same host.
5. Submit one allowlisted read-only request.
6. Verify non-allowlisted requests fail closed.
7. Verify missing or invalid credentials fail closed.
8. Stop the bridge and confirm credentials expire.

## Required future artifacts

- command transcript with secrets redacted;
- bridge bind-address evidence;
- allowlist pass/fail evidence;
- credential failure evidence;
- stop-condition evidence.
