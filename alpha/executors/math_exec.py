"""Deterministic local math evaluator."""
import ast
import json
from typing import Any, Dict

TOOL_ID = "local.math.eval"

_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
    ast.Mod: lambda a, b: a % b,
    ast.FloorDiv: lambda a, b: a // b,
}

_ALLOWED_UNARY = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("unsupported constant")
    if isinstance(node, ast.Num):  # pragma: no cover
        return float(node.n)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError("unsupported operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_BINOPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY:
            raise ValueError("unsupported operator")
        operand = _eval(node.operand)
        return _ALLOWED_UNARY[op_type](operand)
    raise ValueError("unsupported expression")


def evaluate(expr: str) -> Dict[str, Any]:
    """Safely evaluate a math expression."""
    try:
        parsed = ast.parse(expr, mode="eval")
        result = _eval(parsed)
        return {"ok": True, "result": result, "error": None}
    except Exception as exc:  # pragma: no cover - deterministic message
        return {"ok": False, "result": None, "error": str(exc)}


if __name__ == "__main__":  # pragma: no cover - CLI helper
    import sys

    expression = sys.argv[1] if len(sys.argv) > 1 else ""
    out = evaluate(expression)
    print(json.dumps(out))
