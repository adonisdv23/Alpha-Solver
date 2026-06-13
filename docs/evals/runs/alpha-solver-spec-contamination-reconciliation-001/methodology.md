# Methodology (reproducible, read-only)

1. **Enumerate**: list all `.specs/*.md` (83 files).
2. **Signature scan**: grep the Error-Taxonomy signature phrase
   `"Create a stable MCP error taxonomy"` → 23 files.
3. **Body normalization + hashing**: for each spec, drop (a) the H1 title line,
   (b) a leading blockquote block before the first `## ` header — the
   non-authoritative banner or any prior hygiene note — and (c) the
   `## Code Targets` section; normalize whitespace; SHA-1 hash; cluster. Excluding
   the title, banner/note, and targets isolates the *copied body* and keeps the
   hash stable before and after bannering. The exact rule and a runnable
   implementation are in [`contamination-evidence.md`](contamination-evidence.md)
   and [`reproduce-body-hash.py`](reproduce-body-hash.py).
4. **Cluster analysis**: exactly **one** multi-file body cluster exists — the
   MCP-005 Error-Taxonomy body. Under the rule above, **all 23 taxonomy-bearing
   specs (canonical `MCP-005` + 22 contaminated) hash to `a7c9ca95240e`** in the
   committed state (`MCP-001` and `NEW-016` included — the rule excludes their
   replaced hygiene note). No other duplicate/near-duplicate body cluster exists
   among the remaining specs.
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
python docs/evals/runs/alpha-solver-spec-contamination-reconciliation-001/reproduce-body-hash.py
# -> all 23 share normalized body hash a7c9ca95240e; RESULT: PASS
```

All steps are read-only over committed files. No spec content was inferred,
reconstructed, or invented during the audit.
