import os
from alpha.executors import math_exec


def test_evaluate_success():
    res = math_exec.evaluate("2+2")
    assert res["ok"]
    assert res["result"] == 4


def test_evaluate_invalid():
    res = math_exec.evaluate("2+")
    assert not res["ok"]
    assert res["error"]
