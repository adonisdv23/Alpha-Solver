from alpha.eval.scorers import exact_match, f1_token, regex_pass, numeric_close


def test_exact_match():
    assert exact_match("foo", "foo") == 1.0
    assert exact_match("foo", "bar") == 0.0


def test_f1_token():
    assert f1_token("a b", "a b") == 1.0
    assert f1_token("a", "a b") < 1.0


def test_regex_pass():
    assert regex_pass("hello", "", {"regex": "^h"}) == 1.0
    assert regex_pass("world", "", {"regex": "^h"}) == 0.0


def test_numeric_close():
    assert numeric_close("1.0", "1.001", {"abs_tol": 0.01}) == 1.0
    assert numeric_close("1", "2") == 0.0
