# Forbidden first-code files

The first-code static test lane must not modify:

- runtime files under `alpha/`, `service/`, or `cli/`;
- provider code under `alpha/providers/`;
- API or dashboard routes;
- CLI entrypoints;
- checker scripts under `scripts/`;
- `Makefile`;
- `.github/workflows/`;
- `.env.example` or credential-related files;
- source-artifact directories or preserved run payloads;
- backlog workbooks or registry exports;
- non-target docs outside the authorized Level 10 packet.

Files that must never be modified by Self Operator implementation lanes without separate authorization include `alpha_solver_portable.py`, `alpha-solver-v91-python.py`, `alpha_solver_entry.py`, source artifacts, credential files, backlog workbooks, and registry export artifacts.
