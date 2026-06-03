from scripts.check_case_collisions import case_collision_groups


def test_case_collision_groups_detects_case_only_duplicates():
    collisions = case_collision_groups([
        "docs/Alpha.md",
        "docs/alpha.md",
        "service/Beta.py",
        "service/beta.py",
        "docs/README.md",
    ])

    assert collisions == {
        "docs/alpha.md": ["docs/Alpha.md", "docs/alpha.md"],
        "service/beta.py": ["service/Beta.py", "service/beta.py"],
    }


def test_tracked_paths_have_no_case_collisions():
    from scripts.check_case_collisions import tracked_paths

    assert case_collision_groups(tracked_paths()) == {}
