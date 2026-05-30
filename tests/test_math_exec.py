import ast

import pytest

from alpha.executors import math_exec


def test_evaluate_success():
    res = math_exec.evaluate("2+2")
    assert res["ok"]
    assert res["result"] == 4


def test_evaluate_constant_numeric_literal_regression():
    parsed = ast.parse("3.5", mode="eval")
    assert isinstance(parsed.body, ast.Constant)

    res = math_exec.evaluate("3.5")

    assert res == {"ok": True, "result": 3.5, "error": None}


def test_evaluate_rejects_boolean_constant():
    res = math_exec.evaluate("True")

    assert not res["ok"]
    assert res["result"] is None
    assert res["error"] == "unsupported constant"


@pytest.mark.parametrize(
    "expr",
    [
        "__import__('os').system('echo unsafe')",
        "open('/etc/passwd').read()",
        "(1).__class__",
        "[1, 2, 3]",
        "[1][0]",
        "lambda: 1",
        "x + 1",
    ],
)
def test_evaluate_rejects_unsafe_constructs(expr):
    res = math_exec.evaluate(expr)

    assert not res["ok"]
    assert res["result"] is None
    assert res["error"]


def test_evaluate_invalid():
    res = math_exec.evaluate("2+")
    assert not res["ok"]
    assert res["error"]
