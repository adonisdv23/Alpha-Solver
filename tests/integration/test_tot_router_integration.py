from alpha_solver_entry import _tree_of_thought


def test_tot_router_integration_diagnostics():
    env = _tree_of_thought(
        "integration test",
        enable_progressive_router=True,
        multi_branch=True,
        router_min_progress=1.1,
    )
    diag = env["diagnostics"]
    assert diag["router"]["stage"] != "basic"
    assert "tot" in diag
