import re
import time
from typing import Dict, Tuple

EMAIL_REGEX = re.compile(r"(?P<local>[A-Za-z0-9._%+-]+)@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
PHONE_REGEX = re.compile(r"\+?\d[\d\s\-]{8,}\d")


def _mask_email(local: str, domain: str) -> str:
    local_masked = local[0] + "***" if local else "***"
    domain_parts = domain.split('.')
    first = domain_parts[0]
    domain_parts[0] = (first[0] + "***") if first else "***"
    return f"{local_masked}@{'.'.join(domain_parts)}"


def _mask_phone(s: str) -> str:
    digits = [c for c in s if c.isdigit()]
    last_four = digits[-4:]
    result = []
    digit_index = 0
    for c in s:
        if c.isdigit():
            if digit_index < len(digits) - 4:
                result.append('*')
            else:
                result.append(last_four[digit_index - (len(digits) - 4)])
            digit_index += 1
        else:
            result.append(c)
    return ''.join(result)


def redact(text: str, detectors: Dict[str, bool]) -> Tuple[str, Dict[str, float]]:
    """Redact PII in *text* according to *detectors* configuration.

    Returns redacted text and stats including latency_ms and hit counts.
    """
    start = time.perf_counter()
    stats: Dict[str, float] = {"email": 0, "phone": 0}

    def repl_email(match: re.Match) -> str:
        local = match.group('local')
        domain = match.group('domain')
        stats['email'] += 1
        return _mask_email(local, domain)

    def repl_phone(match: re.Match) -> str:
        s = match.group(0)
        digits = [c for c in s if c.isdigit()]
        # basic E.164 length check 10-15 digits
        if not (10 <= len(digits) <= 15):
            return s
        stats['phone'] += 1
        return _mask_phone(s)

    try:
        if detectors.get('email', True):
            text = EMAIL_REGEX.sub(repl_email, text)
        if detectors.get('phone', True):
            text = PHONE_REGEX.sub(repl_phone, text)
    except Exception as exc:  # fail-closed on detector errors  # pragma: no cover
        stats['error'] = str(exc)
        text = '[REDACTED]'
    finally:
        stats['latency_ms'] = (time.perf_counter() - start) * 1000.0

    return text, stats
