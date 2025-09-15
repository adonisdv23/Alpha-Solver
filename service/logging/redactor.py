import re
from copy import deepcopy
from typing import Any, Dict, Iterable
from pathlib import Path
import yaml
from service.metrics.exporter import Counter, _REGISTRY

# Counters for observability
APPLIED_COUNTER = Counter(
    "alpha_redaction_applied_total",
    "redactions applied",
    ["type"],
    registry=_REGISTRY,
)
ERROR_COUNTER = Counter(
    "alpha_redaction_errors_total",
    "redaction errors",
    registry=_REGISTRY,
)
# Simple integers for easy test inspection
APPLIED_TOTAL = 0
ERROR_TOTAL = 0

# Load configuration -------------------------------------------------------
_cfg_path = Path(__file__).resolve().parents[1] / "config" / "redaction.yaml"
try:
    with open(_cfg_path, "r", encoding="utf-8") as fh:
        _CONFIG = yaml.safe_load(fh) or {}
except Exception:  # pragma: no cover - file missing
    _CONFIG = {}

_ALLOWLIST: set[str] = set(_CONFIG.get("allowlist", []))
_DETECTORS: Dict[str, bool] = {
    "authorization": True,
    "api_key": True,
    "generic_token": True,
    "email": True,
    "phone": True,
}
_DETECTORS.update(_CONFIG.get("detectors", {}))

# Regular expressions ------------------------------------------------------
EMAIL_RE = re.compile(r"(?P<local>[A-Za-z0-9._%+-]+)@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{8,}\d")
AUTH_RE = re.compile(r"(Authorization[:\s]*Bearer\s+)([A-Za-z0-9._\-]+)", re.IGNORECASE)
API_KEY_RE = re.compile(r"(?:sk|xoxb)-[A-Za-z0-9\-]{8,}")
GENERIC_TOKEN_RE = re.compile(r"\b[A-Za-z0-9]{32,64}\b")

_COMBINED_RE = re.compile(
    "|".join(
        [
            AUTH_RE.pattern,
            API_KEY_RE.pattern,
            GENERIC_TOKEN_RE.pattern,
            EMAIL_RE.pattern,
            PHONE_RE.pattern,
        ]
    ),
    re.IGNORECASE,
)

# Mask helpers -------------------------------------------------------------

def _mask_email(local: str, domain: str) -> str:
    local_masked = local[0] + "***" if local else "***"
    domain_parts = domain.split(".")
    first = domain_parts[0]
    domain_parts[0] = first[0] + "***" if first else "***"
    return f"{local_masked}@{'.'.join(domain_parts)}"

def _mask_phone(s: str) -> str:
    digits = [c for c in s if c.isdigit()]
    last_four = digits[-4:]
    result: list[str] = []
    digit_index = 0
    for c in s:
        if c.isdigit():
            if digit_index < len(digits) - 4:
                result.append("*")
            else:
                result.append(last_four[digit_index - (len(digits) - 4)])
            digit_index += 1
        else:
            result.append(c)
    return "".join(result)

# Core redaction -----------------------------------------------------------

def _redact_str(text: str) -> str:
    if not _COMBINED_RE.search(text):
        return text
    try:
        if _DETECTORS.get("authorization", True):
            def repl_auth(m: re.Match) -> str:
                global APPLIED_TOTAL
                APPLIED_COUNTER.labels(type="authorization").inc()
                APPLIED_TOTAL += 1
                return m.group(1) + "***REDACTED***"
            text = AUTH_RE.sub(repl_auth, text)
        if _DETECTORS.get("api_key", True):
            def repl_api(m: re.Match) -> str:
                global APPLIED_TOTAL
                APPLIED_COUNTER.labels(type="api_key").inc()
                APPLIED_TOTAL += 1
                return "***REDACTED***"
            text = API_KEY_RE.sub(repl_api, text)
        if _DETECTORS.get("generic_token", True):
            def repl_token(m: re.Match) -> str:
                global APPLIED_TOTAL
                APPLIED_COUNTER.labels(type="token").inc()
                APPLIED_TOTAL += 1
                return "***REDACTED***"
            text = GENERIC_TOKEN_RE.sub(repl_token, text)
        if _DETECTORS.get("email", True):
            def repl_email(m: re.Match) -> str:
                global APPLIED_TOTAL
                APPLIED_COUNTER.labels(type="email").inc()
                APPLIED_TOTAL += 1
                return _mask_email(m.group("local"), m.group("domain"))
            text = EMAIL_RE.sub(repl_email, text)
        if _DETECTORS.get("phone", True):
            def repl_phone(m: re.Match) -> str:
                digits = [c for c in m.group(0) if c.isdigit()]
                if not (10 <= len(digits) <= 15):
                    return m.group(0)
                global APPLIED_TOTAL
                APPLIED_COUNTER.labels(type="phone").inc()
                APPLIED_TOTAL += 1
                return _mask_phone(m.group(0))
            text = PHONE_RE.sub(repl_phone, text)
    except Exception:
        global ERROR_TOTAL
        ERROR_COUNTER.inc()
        ERROR_TOTAL += 1
        return "[REDACTED]"
    return text


def _redact(obj: Any) -> Any:
    if isinstance(obj, str):
        return _redact_str(obj)
    if isinstance(obj, dict):
        out: Dict[Any, Any] = {}
        for k, v in obj.items():
            if isinstance(k, str) and k in _ALLOWLIST:
                out[k] = v
            else:
                out[k] = _redact(v)
        return out
    if isinstance(obj, list):
        return [_redact(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_redact(v) for v in obj)
    return obj


def redact(obj: Any, allowlist: Iterable[str] | None = None) -> Any:
    """Return a redacted copy of *obj* (string or dict)."""
    if allowlist is not None:
        global _ALLOWLIST
        prev = _ALLOWLIST
        _ALLOWLIST = set(allowlist)
        try:
            return _redact(deepcopy(obj))
        finally:
            _ALLOWLIST = prev
    return _redact(deepcopy(obj))

__all__ = [
    "redact",
    "APPLIED_COUNTER",
    "ERROR_COUNTER",
    "APPLIED_TOTAL",
    "ERROR_TOTAL",
]
