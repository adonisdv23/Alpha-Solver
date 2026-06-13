# Methodology (reproducible, read-only)

1. **Enumerate**: list all `.specs/*.md` (83 files).
2. **Signature scan**: grep the Error-Taxonomy signature phrase
   `"Create a stable MCP error taxonomy"` → 23 files.
3. **Body normalization + hashing**: for each spec, drop the H1 title line and the
   `## Code Targets` section, normalize whitespace, SHA-1 hash, and cluster. This
   isolates *body* identity from the (legitimately file-specific) title + targets.
4. **Cluster analysis**: exactly **one** multi-file body cluster exists — the
   MCP-005 Error-Taxonomy body. 21 files share it byte-for-byte; `MCP-001` and
   `NEW-016` carry the same body plus a prior hygiene note (so hash differs). No
   other duplicate/near-duplicate body cluster exists among the remaining specs.
5. **Canonical identification**: `MCP-005 · Error Taxonomy (MCP)` is the single
   legitimate source (title, body, and `## Code Targets`
   `service/mcp/error_taxonomy.py` all agree).
6. **Code-target existence check**: for every contaminated spec, test whether its
   `## Code Targets` (impl + test files) exist in the repo — feeds the
   reconstruction-feasibility finding.
7. **Provenance (informational)**: `git log` shows the contaminated bodies and the
   two prior hygiene notes both present as of commit `a07d6b0` (#464).

## Reproduce

```bash
grep -rl "Create a stable MCP error taxonomy" .specs/ | sort   # 23 files
# MCP-005 is canonical; the other 22 are contaminated.
```

All steps are read-only over committed files. No spec content was inferred,
reconstructed, or invented during the audit.
