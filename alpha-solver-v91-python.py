from __future__ import annotations

"""Alpha Solver v91 entrypoints."""

from alpha.reasoning.tot import TreeOfThoughtSolver


def _tree_of_thought(query: str, **kwargs):
    """Solve ``query`` using the deterministic Tree-of-Thought solver."""

    solver = TreeOfThoughtSolver(**kwargs)
    return solver.solve(query)
