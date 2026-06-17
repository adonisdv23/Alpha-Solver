# Security and redaction

- No API key input field was added.
- Preview output is rendered through HTML escaping.
- Existing sanitized JSON copy behavior remains scoped to the sanitized JSON panel.
- Preview is local-only and guarded by the console loopback request check.
- Preview treats task text as untrusted input and relies on existing tool-router warnings for prompt-injection or authority-escalation text.
