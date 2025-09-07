from alpha.reasoning.tot import TreeOfThoughtSolver, Node


def test_branch_generator_deterministic():
    solver = TreeOfThoughtSolver(seed=42, branching_factor=3)
    parent = Node(content="check determinism", path=("check determinism",), depth=0)
    solver._query_tokens = set(parent.content.lower().split())

    runs = [solver.branch_generator(parent) for _ in range(3)]
    contents = [[n.content for n in run] for run in runs]

    assert all(len(run) == solver.branching_factor for run in runs)
    assert contents[0] == contents[1] == contents[2]
