"""Non-production local LLM solver orchestration runner.

This module is intentionally internal/CLI-callable only. It is not imported by
``/v1/solve`` or dashboard preview routes. The runner reuses the approved local
LLM runtime config/backend path, performs a bounded two-pass local expert flow,
and preserves the non-evidence local runtime boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any, Mapping, Sequence

from .provider_adapter import (
    LocalLLMAdapterResult,
    LocalLLMRuntimeConfig,
    OllamaJSONTransport,
    run_configured_local_llm_runtime,
)
from .portable_contract import PortableContract

PROVIDER_MODE = "local_llm"
ORCHESTRATION_MODE = "non_production_local_solver_orchestration"
STRATEGY = "local_expert_two_pass"
SUPPORTED_MODES = frozenset({"direct", "clarify", "answer_with_assumptions", "block"})
_TERMINAL_EVIDENCE_BOUNDARY = (
    "non-production local solver orchestration only; not runtime smoke execution, "
    "local model quality evidence, hosted provider evidence, /v1/solve readiness, "
    "dashboard readiness, MVP validation, production readiness, benchmark evidence, "
    "provider orchestration evidence, Alpha superiority evidence, evidence-model "
    "promotion, or broad runtime readiness evidence"
)
_MAX_PASS1_CHARS = 6000
_MAX_SECTION_ITEMS = 6
_MAX_ITEM_CHARS = 240
_MIN_ASSUME_CONFIDENCE = 0.55

_UNDERSPECIFIED_PROMPT_RE = re.compile(
    r"^\s*(?:make|improve|optimi[sz]e|fix|update|change|tune|refactor)\s+"
    r"(?:it|this|that|them|things?)\b[\s.!?]*$",
    flags=re.IGNORECASE,
)
_HIGH_RISK_TEXT_RE = re.compile(
    r"\b(?:"
    r"disable\s+safety|turn\s+off\s+safety|bypass\s+(?:safeguards?|safety|monitoring)|"
    r"hide\s+(?:changes?|this|activity)\s+from\s+reviewers?|conceal\s+(?:changes?|activity|this)|"
    r"evade\s+(?:detection|monitoring|review)|"
    r"avoid\s+(?:detection|review|logs?|logging|audit(?:\s+trails?)?|alerts?)|"
    r"prevent\s+(?:alerts?|audit(?:\s+trails?)?)|"
    r"disable\s+(?:monitoring|logging|audit|alerts?|automated\s+checks?)|"
    r"hiding\s+changes?|concealment|bypass(?:ing)?\s+(?:monitoring|automated\s+checks?)|"
    r"self[-\s]?harm|suicide|weapons?|explosives?"
    r")\b",
    flags=re.IGNORECASE,
)
_HIGH_RISK_FLAG_RE = re.compile(
    r"\b(?:"
    r"high[-\s]?risk|unsafe|policy\s+risk|safety\s+risk|"
    r"credential\s+(?:theft|stealing|harvesting)|token\s+theft|cookie\s+theft|"
    r"secret\s+extraction|data\s+(?:exfiltration|theft)|exfiltration|"
    r"malware|phishing|unauthori[sz]ed\s+access|account\s+takeover|"
    r"exploit(?:\s+chain)?|evasion|evade|concealment|conceal|bypass|"
    r"hide\s+from\s+reviewers?|disable\s+safety|disable\s+monitoring|"
    r"self[-\s]?harm|suicide|weapons?|explosives?"
    r")\b",
    flags=re.IGNORECASE,
)
_LOW_RISK_FLAG_ALLOWLIST = frozenset(
    {
        "",
        "none",
        "n/a",
        "na",
        "no risk",
        "low",
        "low risk",
        "ordinary",
        "safe",
        "optimization",
        "optimisation",
        "profiling",
        "performance",
        "latency",
        "implementation",
        "refactor",
        "planning",
        "unknown",
    }
)

_FORBIDDEN_BOUNDARY_TERMS = (
    r"production\s+readiness",
    r"runtime\s+readiness",
    r"broad\s+runtime\s+readiness",
    r"mvp\s+validation",
    r"benchmark\s+success",
    r"benchmark\s+evidence",
    r"alpha\s+superiority",
    r"local\s+model\s+quality",
    r"hosted\s+provider\s+evidence",
    r"provider\s+orchestration\s+evidence",
    r"/?v1/solve\s+readiness",
    r"dashboard\s+readiness",
    r"evidence[-\s]?model\s+promotion",
    r"billing\s+accuracy",
    r"ready\s+for\s+production",
    r"validated\s+for\s+production",
    r"production\s+validated",
    r"validated\s+benchmark",
    r"provider[-\s]?orchestration",
    r"/?v1/solve",
    r"dashboard",
    r"alpha\s+(?:is\s+)?(?:better|best|superior|outperforms?)",
    r"promot(?:e|es|ed|ing)\s+(?:the\s+)?evidence",
    r"local\s+model\s+(?:is\s+)?(?:good|strong|reliable|validated|ready|quality|high\s+quality)",
)
_FORBIDDEN_BOUNDARY_TERM_RE = re.compile(
    r"(?<!\w)(?:" + "|".join(_FORBIDDEN_BOUNDARY_TERMS) + r")(?!\w)",
    flags=re.IGNORECASE,
)
_POSITIVE_BOUNDARY_CLAIM_RE = re.compile(
    r"\b(?:prove|proves|proved|proving|validate|validates|validated|validating|"
    r"confirm|confirms|confirmed|confirming|establish|establishes|established|"
    r"establishing|demonstrate|demonstrates|demonstrated|demonstrating|"
    r"claim|claims|claimed|claiming|show|shows|showed|showing)\b"
    r"|\b(?:is|are|was|were|be|being|been|constitutes|serves\s+as|counts\s+as)\b"
    r".{0,80}\b(?:evidence|validation|readiness|superiority|promotion|success)\b",
    flags=re.IGNORECASE | re.DOTALL,
)
_SELF_ASSERTING_BOUNDARY_CLAIM_RE = re.compile(
    r"\b(?:ready|validated|valid|orchestrat(?:e|es|ed|ing)|outperforms?|"
    r"superior|better|best|promot(?:e|es|ed|ing)|high\s+quality|reliable|billing)\b",
    flags=re.IGNORECASE,
)
_NEGATED_BOUNDARY_CLAIM_RE = re.compile(
    r"\b(?:does|do|did|is|are|was|were|can|could|will|would|should)\s+not\s+"
    r"(?:prove|validate|confirm|establish|demonstrate|claim|show|constitute|serve\s+as|count\s+as)\b"
    r"|\b(?:doesn't|don't|didn't|isn't|aren't|wasn't|weren't|cannot|can't)\s+"
    r"(?:prove|validate|confirm|establish|demonstrate|claim|show|constitute|serve\s+as|count\s+as)\b"
    r"|\b(?:is|are|was|were)\s+not\b.{0,80}\b(?:evidence|validation|readiness|superiority|promotion|success)\b"
    r"|\bno\b.{0,80}\b(?:is|are|was|were)?\s*(?:claimed|claim|evidence|validation|readiness|promotion)\b",
    flags=re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class _PassOneGate:
    mode: str
    considerations: tuple[str, ...]
    assumptions: tuple[str, ...]
    confidence: float | None
    missing_information: tuple[str, ...]
    risk_flags: tuple[str, ...]
    parse_source: str


def run_local_llm_solver_orchestration(
    user_prompt: str,
    *,
    config: LocalLLMRuntimeConfig | None = None,
    env: Mapping[str, str] | None = None,
    transport: OllamaJSONTransport | None = None,
    contract: PortableContract | None = None,
    contract_path: str | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Run a non-production local expert two-pass orchestration flow.

    The only runtime call path is ``run_configured_local_llm_runtime``. With no
    explicit local opt-in, with non-loopback endpoints, with provider keys, or
    with invalid timeouts, the runner fails closed before any answer is exposed.
    """

    if not isinstance(user_prompt, str) or not user_prompt.strip():
        return _base_result(
            status="failed_closed",
            mode="block",
            reason="empty_user_prompt_non_evidence",
        )

    pass_one_prompt = _build_pass_one_prompt(user_prompt)
    pass_one = _runtime_call(
        pass_one_prompt,
        config=config,
        env=env,
        transport=transport,
        contract=contract,
        contract_path=contract_path,
        expected_sha256=expected_sha256,
    )
    if pass_one.status != "non_evidence":
        return _failed_from_adapter(pass_one, pass_count=1, reason=pass_one.reason)

    if _unsafe_output(pass_one.output_text, pass_one.request.system, pass_one_prompt):
        return _failed_from_adapter(
            pass_one,
            pass_count=1,
            reason="unsafe_or_echoed_pass_one_output_non_evidence",
        )

    try:
        gate = _parse_pass_one(pass_one.output_text)
    except ValueError as exc:
        return _failed_from_adapter(pass_one, pass_count=1, reason=str(exc))

    if _pass_one_has_forbidden_boundary_claim(gate):
        return _failed_from_adapter(
            pass_one,
            pass_count=1,
            reason="pass_one_boundary_claim_violation_non_evidence",
        )

    gated = _apply_gate(gate, user_prompt)
    if gated.mode == "clarify":
        return _base_result(
            status="clarify",
            mode="clarify",
            pass_count=1,
            considerations=gated.considerations,
            assumptions=gated.assumptions,
            confidence=gated.confidence,
            final_answer=_clarify_answer(gated),
            metadata=_metadata(pass_one=pass_one, parse_source=gated.parse_source),
        )
    if gated.mode == "block":
        return _base_result(
            status="blocked",
            mode="block",
            pass_count=1,
            considerations=gated.considerations,
            assumptions=gated.assumptions,
            confidence=gated.confidence,
            final_answer="",
            metadata=_metadata(pass_one=pass_one, parse_source=gated.parse_source),
        )

    pass_two_prompt = _build_pass_two_prompt(user_prompt, gated)
    pass_two = _runtime_call(
        pass_two_prompt,
        config=config,
        env=env,
        transport=transport,
        contract=contract,
        contract_path=contract_path,
        expected_sha256=expected_sha256,
    )
    if pass_two.status != "non_evidence":
        return _failed_from_adapter(
            pass_two,
            pass_count=2,
            reason=f"pass_two_failure:{pass_two.reason}",
            pass_one=pass_one,
            gate=gated,
        )
    if _unsafe_output(pass_two.output_text, pass_two.request.system, pass_two_prompt):
        return _failed_from_adapter(
            pass_two,
            pass_count=2,
            reason="unsafe_or_echoed_pass_two_output_non_evidence",
            pass_one=pass_one,
            gate=gated,
        )
    if _has_forbidden_boundary_claim(pass_two.output_text):
        return _failed_from_adapter(
            pass_two,
            pass_count=2,
            reason="pass_two_boundary_claim_violation_non_evidence",
            pass_one=pass_one,
            gate=gated,
        )

    return _base_result(
        status="ok",
        mode=gated.mode,
        pass_count=2,
        considerations=gated.considerations,
        assumptions=gated.assumptions,
        confidence=gated.confidence,
        final_answer=pass_two.output_text.strip(),
        metadata=_metadata(pass_one=pass_one, pass_two=pass_two, parse_source=gated.parse_source),
    )


def _runtime_call(user_prompt: str, **kwargs: Any) -> LocalLLMAdapterResult:
    try:
        return run_configured_local_llm_runtime(user_prompt, **kwargs)
    except Exception as exc:
        reason = getattr(exc, "reason_code", f"runtime_config_error:{exc.__class__.__name__}")
        metadata = {
            "provider_mode": PROVIDER_MODE,
            "behavior_evidence": False,
            "no_hosted_fallback": True,
            "no_provider_keys_required": True,
            "failure_label": "failed_closed_result",
        }
        request = _SyntheticRequest(system="", user_prompt=user_prompt)
        return LocalLLMAdapterResult(
            request=request,  # type: ignore[arg-type]
            output_text="",
            status="failed_closed",
            reason=reason,
            metadata=metadata,
        )


@dataclass(frozen=True)
class _SyntheticRequest:
    system: str
    user_prompt: str


def _base_result(
    *,
    status: str,
    mode: str,
    reason: str | None = None,
    pass_count: int = 0,
    considerations: Sequence[str] = (),
    assumptions: Sequence[str] = (),
    confidence: float | None = None,
    final_answer: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "status": status,
        "provider_mode": PROVIDER_MODE,
        "orchestration_mode": ORCHESTRATION_MODE,
        "strategy": STRATEGY,
        "pass_count": pass_count,
        "mode": mode if mode in SUPPORTED_MODES else "block",
        "considerations": list(considerations),
        "assumptions": list(assumptions),
        "confidence": confidence,
        "answer": final_answer,
        "final_answer": final_answer,
        "metadata": {**(metadata or {}), "behavior_evidence": False},
        "evidence_boundary": _TERMINAL_EVIDENCE_BOUNDARY,
        "behavior_evidence": False,
        "no_hosted_fallback": True,
        "no_provider_keys_required": True,
    }
    if reason:
        result["metadata"]["reason"] = reason
        result["metadata"]["failure_label"] = "failed_closed_result"
    return result


def _failed_from_adapter(
    adapter_result: LocalLLMAdapterResult,
    *,
    pass_count: int,
    reason: str,
    pass_one: LocalLLMAdapterResult | None = None,
    gate: _PassOneGate | None = None,
) -> dict[str, Any]:
    return _base_result(
        status="failed_closed",
        mode="block",
        pass_count=pass_count,
        considerations=gate.considerations if gate else (),
        assumptions=gate.assumptions if gate else (),
        confidence=gate.confidence if gate else None,
        metadata=_metadata(pass_one=pass_one or adapter_result, pass_two=adapter_result if pass_one else None),
        reason=reason,
    )


def _metadata(
    *,
    pass_one: LocalLLMAdapterResult | None = None,
    pass_two: LocalLLMAdapterResult | None = None,
    parse_source: str | None = None,
) -> dict[str, Any]:
    merged: dict[str, Any] = {
        "provider_mode": PROVIDER_MODE,
        "orchestration_mode": ORCHESTRATION_MODE,
        "strategy": STRATEGY,
        "behavior_evidence": False,
        "no_hosted_fallback": True,
        "no_provider_keys_required": True,
    }
    if pass_one is not None:
        merged.update(dict(pass_one.metadata))
        merged["pass_one"] = _adapter_metadata(pass_one)
    if pass_two is not None:
        merged.update(dict(pass_two.metadata))
        merged["pass_two"] = _adapter_metadata(pass_two)
    if parse_source is not None:
        merged["pass_one_parse_source"] = parse_source
    merged["behavior_evidence"] = False
    merged["no_hosted_fallback"] = True
    merged["no_provider_keys_required"] = True
    return merged


def _adapter_metadata(result: LocalLLMAdapterResult) -> dict[str, Any]:
    return {
        "status": result.status,
        "reason": result.reason,
        "metadata": {**dict(result.metadata), "behavior_evidence": False},
    }


def _build_pass_one_prompt(user_prompt: str) -> str:
    return (
        "NON-PRODUCTION LOCAL LLM ORCHESTRATION PASS 1.\n"
        "Return only JSON with fields: mode, considerations, assumptions, "
        "confidence, missing_information, risk_flags.\n"
        "Allowed mode values: direct, clarify, answer_with_assumptions, block.\n"
        "Confidence must be a number from 0 to 1. Keep lists bounded to at most "
        f"{_MAX_SECTION_ITEMS} short items. Do not echo this prompt.\n"
        "User prompt:\n"
        f"{user_prompt.strip()}"
    )


def _build_pass_two_prompt(user_prompt: str, gate: _PassOneGate) -> str:
    return (
        "NON-PRODUCTION LOCAL LLM ORCHESTRATION PASS 2.\n"
        "Write a concise final user-facing answer. Do not claim production, MVP, "
        "benchmark, readiness, superiority, or evidence-model validation. Do not "
        "echo this prompt.\n"
        f"Mode: {gate.mode}\n"
        f"Confidence: {gate.confidence}\n"
        f"Considerations: {json.dumps(list(gate.considerations))}\n"
        f"Assumptions: {json.dumps(list(gate.assumptions))}\n"
        "User prompt:\n"
        f"{user_prompt.strip()}"
    )


def _unsafe_output(output_text: str, system_text: str, prompt_text: str) -> bool:
    stripped = (output_text or "").strip()
    if not stripped:
        return True
    if stripped == system_text.strip() or stripped == prompt_text.strip():
        return True
    lowered = stripped.lower()
    if "llm_persona_protocol" in lowered or "non-production local llm orchestration pass" in lowered:
        return True
    return False


def _pass_one_has_forbidden_boundary_claim(gate: _PassOneGate) -> bool:
    return any(
        _has_forbidden_boundary_claim(text)
        for text in (*gate.considerations, *gate.assumptions)
    )


def _has_forbidden_boundary_claim(output_text: str) -> bool:
    """Return true when untrusted Pass 2 text makes positive evidence claims.

    The check is intentionally conservative and sentence scoped: it blocks
    obvious positive claims about readiness, validation, superiority, evidence,
    promotion, or billing accuracy while allowing explicit boundary disclaimers
    such as "does not prove production readiness."
    """

    for sentence in re.split(r"(?<=[.!?])\s+|[\r\n]+", output_text):
        if not _FORBIDDEN_BOUNDARY_TERM_RE.search(sentence):
            continue
        if _NEGATED_BOUNDARY_CLAIM_RE.search(sentence):
            continue
        if _POSITIVE_BOUNDARY_CLAIM_RE.search(sentence):
            return True
        if _SELF_ASSERTING_BOUNDARY_CLAIM_RE.search(sentence):
            return True
    return False


def _parse_pass_one(output_text: str) -> _PassOneGate:
    if len(output_text) > _MAX_PASS1_CHARS:
        raise ValueError("pass_one_output_too_large_non_evidence")
    data = _parse_json_object(output_text)
    source = "json"
    if data is None:
        data = _parse_safe_sections(output_text)
        source = "sections"
    if data is None:
        raise ValueError("malformed_pass_one_output_non_evidence")

    mode = str(data.get("mode", "")).strip().lower()
    if mode not in SUPPORTED_MODES:
        raise ValueError("unsupported_or_ambiguous_pass_one_mode_non_evidence")
    considerations = _bounded_string_list(data.get("considerations"), required=False)
    assumptions = _bounded_string_list(data.get("assumptions"), required=False)
    missing = _bounded_string_list(data.get("missing_information"), required=False)
    risks = _bounded_string_list(data.get("risk_flags"), required=False)
    confidence = _parse_confidence(data.get("confidence"))
    return _PassOneGate(
        mode=mode,
        considerations=considerations,
        assumptions=assumptions,
        confidence=confidence,
        missing_information=missing,
        risk_flags=risks,
        parse_source=source,
    )


def _parse_json_object(output_text: str) -> Mapping[str, Any] | None:
    text = output_text.strip()
    candidates = [text]
    if "```" in text:
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.IGNORECASE | re.DOTALL)
        if fenced:
            candidates.insert(0, fenced.group(1))
    obj_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if obj_match:
        candidates.append(obj_match.group(0))
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, Mapping):
            return parsed
    return None


def _parse_safe_sections(output_text: str) -> Mapping[str, Any] | None:
    text = output_text.strip()
    if "{" in text or "}" in text or len(text) > 2500:
        return None
    labels = ("mode", "considerations", "assumptions", "confidence", "missing_information", "risk_flags")
    pattern = re.compile(r"^(%s)\s*:\s*(.*)$" % "|".join(labels), re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) < 3:
        return None
    sections: dict[str, Any] = {}
    for index, match in enumerate(matches):
        label = match.group(1).lower()
        start = match.end(2) - len(match.group(2))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        value = text[start:end].strip()
        if not value or len(value) > 600:
            return None
        if label in {"considerations", "assumptions", "missing_information", "risk_flags"}:
            sections[label] = _split_section_items(value)
        else:
            sections[label] = value.splitlines()[0].strip()
    if "mode" not in sections or "confidence" not in sections:
        return None
    return sections


def _split_section_items(value: str) -> list[str]:
    raw_items = re.split(r"\n|;", value)
    items = []
    for item in raw_items:
        cleaned = re.sub(r"^\s*[-*\d.)]+\s*", "", item).strip()
        if cleaned:
            items.append(cleaned)
    return items or [value.strip()]


def _bounded_string_list(value: Any, *, required: bool) -> tuple[str, ...]:
    if value is None:
        if required:
            raise ValueError("missing_required_pass_one_section_non_evidence")
        return ()
    if isinstance(value, str):
        raw_items = _split_section_items(value)
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        raw_items = list(value)
    else:
        raise ValueError("unsafe_pass_one_section_non_evidence")
    items: list[str] = []
    for item in raw_items:
        if not isinstance(item, str):
            raise ValueError("unsafe_pass_one_section_non_evidence")
        cleaned = " ".join(item.strip().split())
        if cleaned:
            if len(cleaned) > _MAX_ITEM_CHARS:
                raise ValueError("unbounded_pass_one_section_non_evidence")
            items.append(cleaned)
    if len(items) > _MAX_SECTION_ITEMS:
        raise ValueError("unbounded_pass_one_section_non_evidence")
    if required and not items:
        raise ValueError("missing_required_pass_one_section_non_evidence")
    return tuple(items)


def _parse_confidence(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        stripped = value.strip()
        if not re.fullmatch(r"(?:0(?:\.\d+)?|1(?:\.0+)?)", stripped):
            return None
        number = float(stripped)
    else:
        return None
    if 0.0 <= number <= 1.0:
        return number
    return None


def _apply_gate(gate: _PassOneGate, user_prompt: str) -> _PassOneGate:
    if _high_risk(gate, user_prompt):
        return _replace_gate(gate, mode="block", expose_model_fields=False)
    if _is_underspecified_prompt(user_prompt):
        return _replace_gate(gate, mode="clarify", expose_model_fields=False)
    if gate.mode == "block" and _assumption_answer_allowed(gate):
        return _replace_gate(gate, mode="answer_with_assumptions")
    if gate.mode == "block":
        return _replace_gate(gate, mode="block", expose_model_fields=False)
    if gate.confidence is None and gate.mode in {"direct", "answer_with_assumptions"}:
        return _replace_gate(gate, mode="clarify")
    if gate.mode == "direct" and gate.missing_information:
        return _replace_gate(gate, mode="clarify")
    if gate.mode == "answer_with_assumptions":
        if not _assumption_answer_allowed(gate):
            return _replace_gate(gate, mode="clarify")
    return gate


def _replace_gate(
    gate: _PassOneGate, *, mode: str, expose_model_fields: bool = True
) -> _PassOneGate:
    return _PassOneGate(
        mode=mode,
        considerations=gate.considerations if expose_model_fields else (),
        assumptions=gate.assumptions if expose_model_fields else (),
        confidence=gate.confidence,
        missing_information=gate.missing_information,
        risk_flags=gate.risk_flags,
        parse_source=gate.parse_source,
    )


def _is_underspecified_prompt(user_prompt: str) -> bool:
    prompt = " ".join(user_prompt.strip().split())
    if _UNDERSPECIFIED_PROMPT_RE.fullmatch(prompt):
        return True
    words = re.findall(r"[a-z0-9_]+", prompt.lower())
    if len(words) <= 4 and any(word in {"it", "this", "that", "them"} for word in words):
        return True
    return False


def _high_risk(gate: _PassOneGate, user_prompt: str) -> bool:
    if _HIGH_RISK_TEXT_RE.search(user_prompt):
        return True
    for flag in gate.risk_flags:
        normalized = _normalize_risk_flag(flag)
        if _HIGH_RISK_FLAG_RE.search(normalized):
            return True
        if normalized not in _LOW_RISK_FLAG_ALLOWLIST:
            return True
    return False


def _normalize_risk_flag(flag: str) -> str:
    normalized = flag.strip().lower().replace("_", " ").replace("-", " ")
    return " ".join(normalized.split())


def _assumption_answer_allowed(gate: _PassOneGate) -> bool:
    if gate.confidence is None or gate.confidence < _MIN_ASSUME_CONFIDENCE:
        return False
    if not gate.considerations or not gate.assumptions:
        return False
    if gate.missing_information and len(gate.missing_information) > 2:
        return False
    for text in (*gate.considerations, *gate.assumptions):
        if _HIGH_RISK_TEXT_RE.search(text) or _HIGH_RISK_FLAG_RE.search(text):
            return False
        if _has_forbidden_boundary_claim(text):
            return False
    for assumption in gate.assumptions:
        lowered = assumption.lower()
        if lowered in {"none", "n/a", "unknown"} or "unbounded" in lowered:
            return False
    return True


def _clarify_answer(gate: _PassOneGate) -> str:
    if gate.missing_information:
        return "Please clarify: " + "; ".join(gate.missing_information)
    return "Please clarify the missing information before a local answer can be attempted."
