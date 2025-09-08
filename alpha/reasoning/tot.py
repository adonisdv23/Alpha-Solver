from __future__ import annotations

"""Deterministic Tree-of-Thought solver."""

from dataclasses import dataclass, field, replace
from typing import Dict, List, Tuple
import heapq
import random
import time

from .logging import log_event


@dataclass(frozen=True)
class Node:
    """Immutable node in the reasoning tree."""

    content: str
    path: Tuple[str, ...]
    depth: int
    score: float = field(default=0.0, compare=False)
    id: int = field(default=0, compare=False)


TEMPLATE_FUNCS = (
    lambda q: f"Rephrase: {q}",
    lambda q: f"Decompose: {q}",
    lambda q: f"Edge cases: {q}",
    lambda q: f"Counterpoints: {q}",
    lambda q: f"Summarize: {q}",
)


class TreeOfThoughtSolver:
    """Deterministic Tree-of-Thought solver.

    Provides optional multi-branch search.
    """

    def __init__(
        self,
        *,
        seed: int = 42,
        branching_factor: int = 3,
        score_threshold: float = 0.70,
        max_depth: int = 5,
        timeout_s: int = 10,
        dynamic_prune_margin: float = 0.15,
        multi_branch: bool = False,
        max_width: int = 3,
        max_nodes: int = 100,
    ) -> None:
        self.seed = seed
        self.branching_factor = branching_factor
        self.score_threshold = score_threshold
        self.max_depth = max_depth
        self.timeout_s = timeout_s
        self.dynamic_prune_margin = dynamic_prune_margin
        self.multi_branch = multi_branch
        self.max_width = max_width
        self.max_nodes = max_nodes
        self.rng = random.Random(seed)
        self.visited: Dict[Node, float] = {}
        self._id_counter = 0
        self._query_tokens: set[str] = set()
        self._frontier: List[
            Tuple[float, int, Tuple[str, ...], int, Node]
        ] = []
        self._explored_nodes = 0
        self._timed_out = False

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def _next_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def _priority(
        self, node: Node
    ) -> Tuple[float, int, Tuple[str, ...], int, Node]:
        return (-node.score, node.depth, node.path, node.id, node)

    def _config_dict(self) -> Dict[str, float | int]:
        return {
            "seed": self.seed,
            "branching_factor": self.branching_factor,
            "score_threshold": self.score_threshold,
            "max_depth": self.max_depth,
            "timeout_s": self.timeout_s,
            "dynamic_prune_margin": self.dynamic_prune_margin,
            "multi_branch": int(self.multi_branch),
            "max_width": self.max_width,
            "max_nodes": self.max_nodes,
        }

    # ------------------------------------------------------------------
    # Core components
    # ------------------------------------------------------------------
    def branch_generator(self, parent: Node) -> List[Node]:
        """Generate deterministic child branches for ``parent``."""
        children: List[Node] = []
        for tmpl in TEMPLATE_FUNCS[: self.branching_factor]:
            text = tmpl(parent.content)
            node = Node(
                content=text,
                path=parent.path + (text,),
                depth=parent.depth + 1,
                id=self._next_id(),
            )
            score = self.path_scorer(node)
            node = replace(node, score=score)
            children.append(node)
        children.sort(key=lambda n: n.content)
        return children

    def path_scorer(self, node: Node) -> float:
        """Score ``node`` using simple deterministic heuristics."""
        tokens = set(node.content.lower().split())
        relevance = len(self._query_tokens & tokens) / max(
            len(self._query_tokens), 1
        )

        progress = max(0.0, 1 - (node.depth / max(self.max_depth, 1)))

        text = " ".join(node.path).lower()
        contradictions = {"contradiction", "inconsistent", "impossible"}
        consistency = (
            0.0 if any(term in text for term in contradictions) else 1.0
        )

        score = 0.4 * relevance + 0.3 * progress + 0.3 * consistency
        return round(max(0.0, min(1.0, score)), 3)

    def best_path_selector(self, root: Node) -> Node:
        """Greedy best-first search starting from ``root``."""
        start = time.time()
        self._frontier = [self._priority(root)]
        self.visited = {root: root.score}
        best = root
        while self._frontier:
            if time.time() - start > self.timeout_s:
                self._timed_out = True
                break
            current = heapq.heappop(self._frontier)[-1]
            log_event(
                "expand",
                node_id=current.id,
                depth=current.depth,
                score=current.score,
                path=list(current.path),
                seed=self.seed,
            )
            if current.score > best.score:
                best = current
                self._retrace_and_prune(best.score)
            if (
                current.score >= self.score_threshold
                or current.depth >= self.max_depth
            ):
                continue
            for child in self.branch_generator(current):
                prev = self.visited.get(child)
                if prev is not None and prev >= child.score:
                    continue
                self.visited[child] = child.score
                heapq.heappush(self._frontier, self._priority(child))
            self._explored_nodes += 1
        return best

    def beam_search(
        self, root: Node, *, router: "ProgressiveRouter" | None = None
    ) -> Node:
        """Deterministic breadth-limited multi-branch exploration."""
        start = time.time()
        frontier: List[Node] = [root]
        best = root
        explored = 0
        while frontier and explored < self.max_nodes:
            if time.time() - start > self.timeout_s:
                self._timed_out = True
                break
            depth = frontier[0].depth
            route = router.stage if router else "basic"
            log_event(
                "tot_layer",
                depth=depth,
                size=len(frontier),
                route=route,
                seed=self.seed,
            )
            frontier.sort(key=lambda n: (-round(n.score, 3), n.path))
            layer = frontier[: self.max_width]
            for node in layer:
                log_event(
                    "tot_candidate",
                    depth=node.depth,
                    score=node.score,
                    path=list(node.path),
                    route=route,
                    seed=self.seed,
                )
            next_frontier: List[Node] = []
            for node in layer:
                if node.score > best.score:
                    best = node
                if (
                    node.score >= self.score_threshold
                    or node.depth >= self.max_depth
                ):
                    continue
                for child in self.branch_generator(node):
                    next_frontier.append(child)
                explored += 1
                if explored >= self.max_nodes:
                    break
                if time.time() - start > self.timeout_s:
                    self._timed_out = True
                    break
            frontier = next_frontier
            if router:
                router.route(best.score)
        self._explored_nodes = explored
        return best

    def _retrace_and_prune(self, active_best_score: float) -> None:
        """Prune frontier nodes far from ``active_best_score``."""
        threshold = active_best_score - self.dynamic_prune_margin
        kept = [item for item in self._frontier if item[-1].score >= threshold]
        if len(kept) != len(self._frontier):
            self._frontier[:] = kept
            heapq.heapify(self._frontier)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def solve(
        self, query: str, *, router: "ProgressiveRouter" | None = None
    ) -> Dict[str, object]:
        """Solve ``query`` using deterministic Tree-of-Thought search."""
        self._query_tokens = set(query.lower().split())
        self._explored_nodes = 0
        self._timed_out = False

        root = Node(content=query, path=(query,), depth=0, id=self._next_id())
        root = replace(root, score=self.path_scorer(root))

        log_event("config", config=self._config_dict(), seed=self.seed)

        if self.multi_branch:
            best = self.beam_search(root, router=router)
        else:
            best = self.best_path_selector(root)

        reason = (
            "timeout"
            if self._timed_out
            else (
                "ok"
                if best.score >= self.score_threshold
                else "below_threshold"
            )
        )

        log_event(
            "summary",
            reason=reason,
            explored=self._explored_nodes,
            best_score=best.score,
            seed=self.seed,
        )

        return {
            "answer": best.content,
            "confidence": best.score,
            "path": list(best.path),
            "explored_nodes": self._explored_nodes,
            "config": self._config_dict(),
            "reason": reason,
        }
