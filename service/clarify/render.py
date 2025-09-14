"""Template renderer for clarification prompts."""
from __future__ import annotations

import hashlib
import json
import re
from typing import Dict, Any


def deck_sha(templates: Dict[str, Any]) -> str:
    """Return a stable SHA256 over the templates mapping."""
    canonical = json.dumps(templates, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


_PATTERN = re.compile(r"{{\s*(.*?)\s*}}")


def _evaluate(expr: str, context: Dict[str, Any]) -> str:
    if "|" in expr:
        var, filt = expr.split("|", 1)
        var = var.strip()
        filt = filt.strip()
        if filt.startswith("join"):
            m = re.match(r"join\((.*)\)", filt)
            delim = ", "
            if m:
                arg = m.group(1).strip()
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    delim = arg[1:-1]
                else:
                    delim = arg
            value = context.get(var, [])
            if isinstance(value, (list, tuple, set)):
                return delim.join(str(v) for v in value)
            return str(value)
    else:
        var = expr.strip()
        value = context.get(var, "")
        return str(value)
    return ""


def render(template_key: str, context: Dict[str, Any], templates: Dict[str, Any]) -> str:
    template = templates.get(template_key, "")
    def repl(match: re.Match) -> str:
        expr = match.group(1)
        return _evaluate(expr, context)
    return _PATTERN.sub(repl, template)
