#!/usr/bin/env python3
"""Reproduce the contaminated-body hash evidence for
ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001.

This is an offline evidence/reproduction helper. It is NOT runtime, product,
provider, model, test, or CI code. It reads only committed `.specs/*.md` files,
computes a normalized hash of the *copied contaminated body*, and asserts that
the legitimate `MCP-005` Error-Taxonomy body and every contaminated copy share
one hash. It calls no providers and uses no tokens.

Run from the repository root:

    python docs/evals/runs/alpha-solver-spec-contamination-reconciliation-001/reproduce-body-hash.py

Expected: all 23 taxonomy-bearing specs (canonical `MCP-005` + 22 contaminated)
print the single normalized body hash `a7c9ca95240e`.

Normalization rule (see contamination-evidence.md) — for each spec, remove:
  1. the H1 title line (first line starting with '# ');
  2. a leading blockquote block before the first '## ' section header — this is
     the non-authoritative banner OR any prior hygiene note;
  3. the '## Code Targets' section (header through the line before the next '## ');
then collapse blank-line runs, strip, and SHA-1 the remainder (first 12 hex).
Excluding the title, banner/note, and Code Targets isolates the body that was
actually copied from MCP-005, so the hash is stable before/after bannering.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

SIGNATURE = "Create a stable MCP error taxonomy"
EXPECTED_HASH = "a7c9ca95240e"


def normalize_contaminated_body(text: str) -> str:
    lines = text.split("\n")
    # 1. drop the H1 title line
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    # 2. drop a leading blockquote block (banner / prior hygiene note) before '## '
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith(">"):
        while i < len(lines) and (lines[i].lstrip().startswith(">") or lines[i].strip() == ""):
            if lines[i].startswith("## "):
                break
            i += 1
        lines = lines[i:]
    # 3. drop the '## Code Targets' section
    out: list[str] = []
    skip = False
    for ln in lines:
        if re.match(r"^##\s+Code Targets\b", ln):
            skip = True
            continue
        if skip:
            if re.match(r"^##\s+", ln):
                skip = False
            else:
                continue
        out.append(ln.rstrip())
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return body


def body_hash(text: str) -> str:
    return hashlib.sha1(normalize_contaminated_body(text).encode("utf-8")).hexdigest()[:12]


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[4]
    specs_dir = repo_root / ".specs"
    taxonomy_specs = sorted(
        p for p in specs_dir.glob("*.md")
        if SIGNATURE in p.read_text(encoding="utf-8")
    )
    hashes = {p.name: body_hash(p.read_text(encoding="utf-8")) for p in taxonomy_specs}
    distinct = sorted(set(hashes.values()))

    print(f"taxonomy-bearing specs: {len(taxonomy_specs)} "
          f"(canonical MCP-005 + {len(taxonomy_specs) - 1} contaminated)")
    print(f"distinct normalized body hashes: {distinct}")
    for name in sorted(hashes):
        print(f"  {name:16s} {hashes[name]}")

    ok = distinct == [EXPECTED_HASH]
    print("\nRESULT:", "PASS" if ok else "FAIL",
          f"- all share {EXPECTED_HASH}" if ok else f"- expected only [{EXPECTED_HASH}]")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
