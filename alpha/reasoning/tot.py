from __future__ import annotations

"""Deterministic Tree-of-Thought solver."""

from dataclasses import dataclass, field, replace
from typing import Dict, List, Tuple, Any
import heapq
import random
import time

from .logging import log_event
from .scoring import SCORERS, PathScorer
from .cache import make_key, get as cache_get, put as cache_put
from alpha.observability.accounting import Accountant

# --- Router type guard for lint/type checking (avoid F821) ---
# We want a symbol named `ProgressiveRouter` in module scope so Ruff doesn't flag it,
# without introducing hard import errors if the router package is refactored.
try:  # pragma: no cover - best effort import guard
    # Prefer package re-export
    from alpha.router import ProgressiveRouter  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    try:
        # Fallback to direct module import
        from alpha.router.progressive import ProgressiveRouter  # type: ignore
    except Exception:  # pragma: no cover
        # Final minimal stub satisfies Ruff & type checkers; not used at runtime.
        class ProgressiveRouter:  # type: ignore
            pass


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
        scorer: str = "composite",
        scorer_weights: Dict[str, float] | None = None,
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
        self.scorer_name = scorer
        self.scorer_weights = scorer_weights or {"lexical": 0.6, "constraint": 0.4}
        factory = SCORERS.get(self.scorer_name, SCORERS["lexical"])
        self._scorer: PathScorer = (
            factory(self.scorer_weights)  # type: ignore[misc]
            if self.scorer_name == "composite"
            else factory()
        )
        self.rng = random.Random(seed)
        self.visited: Dict[Node, float] = {}
        self._id_counter = 0
        self._query_tokens: set[str] = set()
        self._frontier: List[
            Tuple[float, int, Tuple[str, ...], int, Node]
        ] = []
        self._explored_nodes = 0
        self._timed_out = False
        self.accounting = Accountant()

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
            self.accounting.record(text)
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
        """Score ``node`` using the configured scorer."""

        context = {
            "query_tokens": self._query_tokens,
            "depth": node.depth,
            "max_depth": self.max_depth,
        }
        return self._scorer.score(node_text=node.content, context=context)

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
                layer="tot",
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
                layer="tot",
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
                    layer="tot",
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
        self,
        query: str,
        *,
        router: "ProgressiveRouter" | None = None,
        cache: Dict[str, Any] | None = None,
    ) -> Dict[str, object]:
        """Solve ``query`` using deterministic Tree-of-Thought search."""

        self.accounting = Accountant()
        self._query_tokens = set(query.lower().split())
        self._explored_nodes = 0
        self._timed_out = False

        key = make_key(query, 0, (), "0")
        if cache is not None:
            hit = cache_get(cache, key)
            if hit is not None:
                return {
                    "answer": hit.get("answer", query),
                    "confidence": float(hit.get("score", 0.0)),
                    "path": [query],
                    "explored_nodes": 0,
                    "config": self._config_dict(),
                    "reason": "ok",
                }

        root = Node(content=query, path=(query,), depth=0, id=self._next_id())
        root = replace(root, score=self.path_scorer(root))

        log_event("config", layer="tot", config=self._config_dict(), seed=self.seed)

        if self.multi_branch:
            best = self.beam_search(root, router=router)
        else:
            best = self.best_path_selector(root)

        reason = (
            "timeout"
            if self._timed_out
            else ("ok" if best.score >= self.score_threshold else "below_threshold")
        )

        log_event(
            "summary",
            layer="tot",
            reason=reason,
            explored=self._explored_nodes,
            best_score=best.score,
            seed=self.seed,
        )

        result = {
            "answer": best.content,
            "confidence": best.score,
            "path": list(best.path),
            "explored_nodes": self._explored_nodes,
            "config": self._config_dict(),
            "reason": reason,
        }

        if cache is not None:
            cache_put(
                cache,
                key,
                {"score": best.score, "answer": best.content, "ts": 0},
            )

        return result
