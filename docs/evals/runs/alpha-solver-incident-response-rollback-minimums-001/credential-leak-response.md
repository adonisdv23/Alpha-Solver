# Credential leak response

## Trigger conditions

Use this response for any suspected exposure of provider keys, API keys, JWT signing material, dashboard signing secrets, dashboard passwords, OAuth secrets, session cookies, tenant credentials, local secret files, or secret-like values in logs, traces, screenshots, tickets, chats, commits, artifacts, or evidence packets.

## Immediate stop actions

1. Treat live or unknown-status credentials as compromised.
2. Declare SEV-0 when the credential may be live, public, externally shared, or provider-billable; otherwise declare at least SEV-1.
3. Revoke or disable the credential at the issuing system before continuing non-containment investigation.
4. Rotate replacement credentials through an approved secret channel only. Do not paste replacements into docs, chat, logs, PRs, or evidence.
5. Invalidate sessions or tokens derived from the leaked secret, including dashboard sessions if the dashboard signing secret or password may be involved.
6. Disable affected provider/runtime/dashboard/API surface until rotation and access review are complete.
7. Search only approved evidence stores for copies of the leaked value. Do not broaden exposure by pasting the secret into new search tools or tickets.

## Evidence preservation and redaction

Preserve:

- where the secret was observed, using a link or artifact ID where access-controlled;
- who could access the location, in role/group terms when possible;
- first-known exposure time and removal time;
- credential type, issuing system, and environment in redacted form;
- revocation, rotation, and session invalidation timestamps;
- confirmation that replacement credentials were not committed or printed.

Redact:

- all but the minimum non-sensitive identifier needed to distinguish the secret, such as provider name plus last four characters only when policy permits;
- screenshots before attaching them to evidence;
- logs with the repository redaction policy and an operator review for pattern-redaction misses.

Never preserve in this packet:

- full keys, tokens, cookies, JWTs, signing secrets, passwords, refresh tokens, private keys, or raw secret files.

## Repository-specific notes

- Existing credential-storage hardening evidence covers restrictive file modes for dashboard-managed provider keys, not encryption-at-rest or full migration of historical plaintext copies.
- Dashboard docs still identify default dashboard credential semantics as a public-exposure blocker until the default credential hardening lane is complete.
- OAuth scaffold docs describe test-only secret behavior and must not be treated as a production secret-management approval.
