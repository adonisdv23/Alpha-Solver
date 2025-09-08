from __future__ import annotations

import importlib.util
from pathlib import Path

ENTRY = Path(__file__).with_name("alpha-solver-v91-python.py")
if not ENTRY.exists():
    raise ImportError(f"Expected entrypoint file not found: {ENTRY}")

_spec = importlib.util.spec_from_file_location("alpha_solver_v91_impl", ENTRY)
if _spec is None or _spec.loader is None:
    raise ImportError("Could not load alpha-solver-v91-python.py via importlib")

_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)  # type: ignore[attr-defined]

AlphaSolver = _module.AlphaSolver  # type: ignore[attr-defined]
_tree_of_thought = _module._tree_of_thought  # type: ignore[attr-defined]


def get_solver() -> AlphaSolver:
    """Return a new :class:`AlphaSolver` instance.

    This helper mirrors the minimal factory expected by tests and scripts
    while deferring all heavy lifting to the lazily-loaded implementation.
    """

    return AlphaSolver()

__all__ = ["AlphaSolver", "_tree_of_thought", "get_solver"]
