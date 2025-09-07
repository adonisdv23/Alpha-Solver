from alpha_solver_entry import _tree_of_thought


def main() -> None:
    queries = ["solve x", "count primes under 10"]
    total_nodes = 0
    total_conf = 0.0
    for q in queries:
        result = _tree_of_thought(q)
        total_nodes += result["tot"]["explored_nodes"]
        total_conf += result["confidence"]
    avg_conf = total_conf / len(queries)
    print(f"explored_nodes={total_nodes}")
    print(f"avg_confidence={avg_conf:.3f}")


if __name__ == "__main__":
    main()
