from __future__ import annotations

"""Deterministic Tree-of-Thought reasoning utilities."""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import time


@dataclass
class Node:
    """Represents a node in the reasoning tree."""

    subquery: str
    path: List[str]
    score: float
    depth: int
    context: Dict[str, Any] = field(default_factory=dict)


class TreeOfThoughtSolver:
    """Simple deterministic Tree-of-Thought solver.

    The solver performs a greedy best-first traversal of a reasoning tree with
    deterministic branching and scoring. It stops when the score threshold,
    maximum depth, or timeout is reached.
    """

    def __init__(
        self,
        *,
        branching_factor: int = 2,
        score_threshold: float = 0.9,
        max_depth: int = 3,
        timeout: float = 1.0,
    ) -> None:
        self.branching_factor = branching_factor
        self.score_threshold = score_threshold
        self.max_depth = max_depth
        self.timeout = timeout
        self.visited: set[tuple[str, ...]] = set()

    # ------------------------------------------------------------------
    # Core components
    # ------------------------------------------------------------------
    def branch_generator(self, node: Node) -> List[Node]:
        """Generate deterministic child branches for ``node``."""

        branches: List[Node] = []
        for i in range(self.branching_factor):
            subquery = f"{node.subquery}.{i + 1}"
            child = Node(
                subquery=subquery,
                path=node.path + [subquery],
                score=0.0,
                depth=node.depth + 1,
                context=dict(node.context),
            )
            branches.append(child)
        return branches

    def path_scorer(self, node: Node) -> float:
        """Score ``node`` based on its path.

        The score is a normalized value in ``[0, 1]`` derived from the ASCII
        values of the characters along the path. This keeps scoring deterministic
        yet non-trivial.
        """

        total = sum(ord(ch) for ch in "".join(node.path))
        node.score = (total % 100) / 100
        return node.score

    def best_path_selector(self, nodes: List[Node]) -> Node:
        """Select the highest scoring node from ``nodes``."""

        return max(nodes, key=lambda n: n.score)

    def _retrace_and_prune(self, node: Node) -> bool:
        """Return ``True`` if ``node`` has been visited previously."""

        key = tuple(node.path)
        if key in self.visited:
            return True
        self.visited.add(key)
        return False

    # ------------------------------------------------------------------
    # Solver entry point
    # ------------------------------------------------------------------
    def solve(self, query: str) -> Dict[str, Any]:
        """Solve ``query`` using deterministic Tree-of-Thought reasoning."""

        start = time.monotonic()
        root = Node(subquery=query, path=[query], score=0.0, depth=0)
        self.path_scorer(root)
        frontier: List[Node] = [root]
        best = root

        while frontier:
            if time.monotonic() - start > self.timeout:
                break

            current = self.best_path_selector(frontier)
            frontier.remove(current)
            best = current

            if current.score >= self.score_threshold or current.depth >= self.max_depth:
                break

            for child in self.branch_generator(current):
                if self._retrace_and_prune(child):
                    continue
                self.path_scorer(child)
                frontier.append(child)

        return {"solution": best.subquery, "path": best.path, "score": best.score}
