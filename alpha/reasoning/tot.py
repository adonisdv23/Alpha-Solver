from __future__ import annotations

"""Deterministic Tree-of-Thought reasoning utilities."""

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Tuple
import heapq
import logging
import time

from .cot import guidance_score


@dataclass(frozen=True)
class Node:
    """Represents a node in the reasoning tree."""

    id: int
    subquery: str
    path: Tuple[str, ...]
    score: float
    depth: int
    context: Mapping[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:  # pragma: no cover - trivial
        object.__setattr__(self, "context", MappingProxyType(dict(self.context)))


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
        prune_ratio: float = 0.8,
    ) -> None:
        self.branching_factor = branching_factor
        self.score_threshold = score_threshold
        self.max_depth = max_depth
        self.timeout = timeout
        self.max_nodes = max_nodes
        self.prune_ratio = prune_ratio
        self.visited: set[tuple[str, Tuple[Tuple[str, Any], ...]]] = set()
        self.logger = logging.getLogger(__name__)
        self._counter = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    # ------------------------------------------------------------------
    # Core components
    # ------------------------------------------------------------------
    def branch_generator(self, node: Node) -> List[Node]:
        """Generate deterministic child branches for ``node``."""

        branches: List[Node] = []
        for i in range(self.branching_factor):
            subquery = f"{node.subquery}.{i + 1}"
            child = Node(
                id=self._next_id(),
                subquery=subquery,
                path=node.path + (subquery,),
                score=0.0,
                depth=node.depth + 1,
                context=dict(node.context),
            )
            score = self.path_scorer(child)
            child = replace(child, score=score)
            self.logger.info(
                {
                    "event": "branch",
                    "parent": node.id,
                    "child": child.id,
                    "step": i,
                    "subquery": child.subquery,
                    "score": child.score,
                }
            )
            branches.append(child)
        return branches

    def path_scorer(self, node: Node) -> float:
        """Score ``node`` using path and context guidance.

        The score combines deterministic path metrics, depth, path length, and
        Chain-of-Thought guidance hints stored in ``node.context``. The result is
        normalized to ``[0, 1]``.
        """

        path_total = sum((i + 1) * ord(ch) for i, ch in enumerate("".join(node.path)))
        path_score = (path_total % 50) / 50
        depth_score = 1.0 - (node.depth / max(self.max_depth, 1))
        length_score = len(node.path) / (self.max_depth + 1)
        guidance = guidance_score(node.context)
        return max(0.0, min(1.0, (path_score + depth_score + length_score + guidance) / 4))

    def best_path_selector(self, frontier: List[Tuple[float, Tuple[str, ...], int, Node]]) -> Node:
        """Pop and return the highest scoring node from ``frontier``."""

        return heapq.heappop(frontier)[3]

    def _retrace_and_prune(
        self, node: Node, best_score: float, *, threshold: float | None = None
    ) -> bool:
        """Return ``True`` if ``node`` should be pruned.

        ``threshold`` is the multiplier applied to ``best_score`` for pruning. If not
        provided, ``self.prune_ratio`` is used. Paths already visited are also
        pruned.
        """

        key = (node.subquery, tuple(sorted(node.context.items())))
        if key in self.visited:
            self.logger.info(
                {
                    "event": "prune",
                    "reason": "visited",
                    "node": node.id,
                    "score": node.score,
                }
            )
            return True

        ratio = threshold if threshold is not None else self.prune_ratio
        if node.score < best_score * ratio:
            self.logger.info(
                {
                    "event": "prune",
                    "reason": "threshold",
                    "node": node.id,
                    "score": node.score,
                    "best": best_score,
                    "ratio": ratio,
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
        root = Node(id=self._next_id(), subquery=query, path=(query,), score=0.0, depth=0)
        root = replace(root, score=self.path_scorer(root))
        frontier: List[Tuple[float, Tuple[str, ...], int, Node]] = [
            (-root.score, root.path, root.id, root)
        ]
        best = root
        nodes_expanded = 0

        while frontier:
            if time.monotonic() - start > self.timeout:
                self.logger.warning(
                    {"event": "abort", "reason": "timeout", "nodes": nodes_expanded}
                )
                break
            if nodes_expanded >= self.max_nodes:
                self.logger.warning(
                    {"event": "abort", "reason": "max_nodes", "nodes": nodes_expanded}
                )
                break

            current = self.best_path_selector(frontier)
            best = current

            if current.score >= self.score_threshold or current.depth >= self.max_depth:
                break

            for child in self.branch_generator(current):
                if self._retrace_and_prune(child, best.score):
                    continue
                heapq.heappush(frontier, (-child.score, child.path, child.id, child))

            nodes_expanded += 1

        return {"solution": best.subquery, "path": list(best.path), "score": best.score}
