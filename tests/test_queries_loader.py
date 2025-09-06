from alpha.core.queries_loader import load_queries


def test_load_queries_with_comments_and_cycles(tmp_path):
    main = tmp_path / "main.txt"
    sub = tmp_path / "sub.txt"
    c1 = tmp_path / "c1.txt"
    c2 = tmp_path / "c2.txt"

    main.write_text("# comment\none\n@file sub.txt\n@file c1.txt\ntwo\n", encoding="utf-8")
    sub.write_text("three\n", encoding="utf-8")
    c1.write_text("@file c2.txt\n", encoding="utf-8")
    c2.write_text("@file c1.txt\nfour\n", encoding="utf-8")

    assert load_queries(str(main)) == ["one", "three", "four", "two"]

