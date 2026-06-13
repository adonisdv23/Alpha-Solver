# Marking actions (non-destructive)

Each of the 22 contaminated specs received a standardized banner immediately under
its H1 title; the contaminated body is preserved **unchanged** beneath it:

```text
> **⚠️ NON-AUTHORITATIVE — CONTAMINATED SPEC (do not implement from this).**
> The Goal / Acceptance Criteria / Design / Tests sections below are a verbatim
> copy of `MCP-005 · Error Taxonomy (MCP)` and do not describe this spec's titled
> feature or its own Code Targets. ... Body preserved unchanged for forensic /
> source-reconstruction purposes. Classification: SPEC_CONTAMINATED +
> SPEC_NEEDS_SOURCE_RECONSTRUCTION.
```

- `MCP-001` and `NEW-016` already had a weaker prior hygiene note; it was replaced
  by the standardized banner so all 22 are consistent. No information was lost.
- `MCP-005` (canonical) was **not** modified.
- `.specs/INDEX.md` gained a `Health` column and a pointer to the audit.
- No spec body text was added, removed, or rewritten (banner is metadata only).

## Verification

- `grep -rl "NON-AUTHORITATIVE — CONTAMINATED SPEC" .specs/` → 22 files.
- `grep -rl "Create a stable MCP error taxonomy" .specs/` → 23 files (22 + MCP-005):
  the contaminated bodies are still present (preserved), confirming non-destruction.
- `git diff --stat .specs/MCP-005.md` → empty (canonical untouched).
