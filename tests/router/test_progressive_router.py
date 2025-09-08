from __future__ import annotations

from alpha.router import ProgressiveRouter
from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_router_escalation_deterministic():
    router = ProgressiveRouter(["basic", "structured", "constrained"])
    assert router.profile() == "basic"
    router.observe(1, 0.5)
    assert router.profile() == "structured"
    router.observe(2, 0.5)
    assert router.profile() == "constrained"


def test_branch_order_changes():
    solver = TreeOfThoughtSolver(seed=42)
    node = Node(content="q", path=("q",), depth=0, id=0)
    basic = solver.branch_generator(node, "basic")
    structured = solver.branch_generator(node, "structured")
    assert [c.content for c in basic] != [c.content for c in structured]

