from __future__ import annotations

import json
import logging

from alpha.reasoning.tot import TreeOfThoughtSolver


def test_multibranch_keeps_max_width(caplog):
    solver = TreeOfThoughtSolver(seed=42, multi_branch=True, max_width=2, max_nodes=20)
    with caplog.at_level(logging.INFO):
        solver.solve("test query")
    layers = [json.loads(r.message) for r in caplog.records if "tot_layer" in r.message]
    assert layers
    assert all(l["kept"] <= 2 for l in layers)


def test_multibranch_caps():
    solver = TreeOfThoughtSolver(seed=42, multi_branch=True, max_nodes=5)
    result = solver.solve("query")
    assert result["explored_nodes"] <= 5
    solver = TreeOfThoughtSolver(seed=42, multi_branch=True, max_depth=1)
    result = solver.solve("query")
    assert len(result["path"]) <= 2
    solver = TreeOfThoughtSolver(seed=42, multi_branch=True, timeout_s=0)
    result = solver.solve("query")
    assert result["reason"] == "timeout"

