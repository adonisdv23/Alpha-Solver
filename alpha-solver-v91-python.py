from __future__ import annotations

"""Alpha Solver v91 entrypoints."""

from alpha.reasoning.tot import TreeOfThoughtSolver


def _tree_of_thought(
    query: str,
    *,
    timeout: float = 1.0,
    max_nodes: int = 100,
    **kwargs,
):
    """Solve ``query`` using the deterministic Tree-of-Thought solver.

    Parameters ``timeout`` and ``max_nodes`` provide safeguards against runaway
    searches and are forwarded to :class:`TreeOfThoughtSolver`.
    """

    solver = TreeOfThoughtSolver(timeout=timeout, max_nodes=max_nodes, **kwargs)
    return solver.solve(query)
