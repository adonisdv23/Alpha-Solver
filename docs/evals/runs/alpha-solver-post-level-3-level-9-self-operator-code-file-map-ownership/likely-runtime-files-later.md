# Likely runtime files for later explicit lanes

The following file areas may be relevant to later runtime work, but they are forbidden for the first-code static scaffold lane and remain inspect-only unless a separate explicit runtime lane authorizes them.

## Inspect-only until later runtime authorization

- `alpha_solver_entry.py`
- `alpha_solver_portable.py`
- `alpha-solver-v91-python.py`
- `src/`
- `alpha_solver/`
- `scripts/`
- API or route modules, including any file that could expose `/v1/solve`
- Dashboard modules and static dashboard assets
- CLI entrypoint modules
- Provider adapter modules

## Boundary

Later runtime lanes must restate their own allowed modification scope. This packet does not authorize runtime modification.
