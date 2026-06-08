# Allowed Local Actions

Lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-8-SELF-OPERATOR-NARROW-MVP-SCOPE-FREEZE-PACKET-001`

## Future MVP local action allowlist

A later implementation may include only the following local actions if Level 8 approval and a later accepted implementation lane explicitly authorize them:

| Action | Frozen boundary |
| --- | --- |
| Local task intake | Accept operator-provided local task text, scope constraints, and intended approved local artifact directory. |
| Local preflight checks | Inspect local repo state and confirm whether required docs/checker prerequisites are present. |
| Operator confirmation capture | Record explicit operator confirmation for the immediate local action only. |
| Allowlisted docs/checker command execution | Run only specifically allowlisted local documentation/checker commands. |
| Local artifact directory creation | Create only the approved local artifact directory for the operator-confirmed task. |
| Local stop-state artifacts | Write local stop-state notes only to the approved local artifact directory or explicitly authorized local metadata files when the MVP cannot safely continue. |
| Local summary generation | Write local summaries only to the approved local artifact directory or explicitly authorized local metadata files, covering intake, confirmations, commands run, artifacts created, blockers, and stop states. |

## Required guardrails

- No command is allowed unless it appears on a future explicit allowlist.
- No command is allowed without current operator confirmation for that specific command.
- No network or external side effect is allowed.
- No credential, secret, billing, provider, deployment, merge, or browser action is allowed.
- Future implementation may write only to an approved local artifact directory and explicitly authorized local metadata files.
- File writes outside the future approved local artifact boundary are forbidden for the narrow MVP unless a later separate scope-expansion packet supersedes this freeze. A normal implementation lane must not expand this boundary.
