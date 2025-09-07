from __future__ import annotations

"""Deterministic Tree-of-Thought reasoning utilities."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple
import heapq
import logging
import time

from .cot import guidance_score


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
        max_nodes: int = 100,
        prune_threshold: float = 0.0,
    ) -> None:
        self.branching_factor = branching_factor
        self.score_threshold = score_threshold
        self.max_depth = max_depth
        self.timeout = timeout
        self.max_nodes = max_nodes
        self.prune_threshold = prune_threshold
        self.visited: set[tuple[str, ...]] = set()
        self.logger = logging.getLogger(__name__)

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
        """Score ``node`` using path and context guidance.

        The score combines a deterministic path-based component with guidance
        derived from Chain-of-Thought hints in ``node.context``. The result is
        normalized to ``[0, 1]``.
        """

        path_total = sum(ord(ch) for ch in "".join(node.path))
        path_score = (path_total % 100) / 100
        guidance = guidance_score(node.context)
        node.score = max(0.0, min(1.0, (path_score + guidance) / 2))
        return node.score

    def best_path_selector(self, frontier: List[Tuple[float, Node]]) -> Node:
        """Pop and return the highest scoring node from ``frontier``."""

        return heapq.heappop(frontier)[1]

    def _retrace_and_prune(self, node: Node) -> bool:
        """Return ``True`` if ``node`` should be pruned.

        Pruning occurs when a path has been visited before or the node's score
        falls below the configured ``prune_threshold``.
        """

        key = tuple(node.path)
        if key in self.visited:
            self.logger.info({"event": "prune", "reason": "visited", "path": node.path})
            return True
        if node.score < self.prune_threshold:
            self.logger.info(
                {
                    "event": "prune",
                    "reason": "low_score",
                    "path": node.path,
                    "score": node.score,
                    "threshold": self.prune_threshold,
                }
            )
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
        frontier: List[Tuple[float, Node]] = [(-root.score, root)]
        best = root
        nodes_expanded = 0

        while frontier:
            if time.monotonic() - start > self.timeout:
                break
            if nodes_expanded >= self.max_nodes:
                break

            current = self.best_path_selector(frontier)
            best = current

            if current.score >= self.score_threshold or current.depth >= self.max_depth:
                break

            for child in self.branch_generator(current):
                self.logger.info(
                    {"event": "branch", "parent": current.subquery, "child": child.subquery}
                )
                self.path_scorer(child)
                if self._retrace_and_prune(child):
                    continue
                heapq.heappush(frontier, (-child.score, child))

            nodes_expanded += 1

        return {"solution": best.subquery, "path": best.path, "score": best.score}
