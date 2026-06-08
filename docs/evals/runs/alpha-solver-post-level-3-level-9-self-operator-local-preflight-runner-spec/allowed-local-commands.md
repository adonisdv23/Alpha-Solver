# Allowed local commands

Future preflight may allow local inspection commands such as:

- `git status --short`
- `git branch --show-current`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git diff --check`
- `git diff --cached --check`
- `python --version`
- Existing local checker commands explicitly listed by the controlling packet.

Allowed commands must be read-only or validation-only and must not reach networks or mutate forbidden files.
