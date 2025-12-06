"""
Alpha Solver v2.2.7-P3 — PORTABLE SPEC MONOLITH

This file is a self-contained representation of the Alpha Solver architecture,
derived from the modular code in this repo.
It is designed for AI-assisted editing environments (ChatGPT / Claude / DeepSeek).
Do NOT remove SAFE-OUT, routing, budget guard, determinism, observability,
or the envelope shape. Real production code also exists in modular form in
this repository.

LLM_PERSONA_PROTOCOL
--------------------
This file is intended to be loaded directly as a system prompt for web LLM chat
interfaces. The model MUST treat the content as an executable architecture
specification and must NOT simplify behavior to "just answer". All outputs must
be formatted as SolverEnvelope-shaped responses that mirror the pipeline below.

Activation phrase: "You are Alpha Solver v2.2.7-P3, running in PORTABLE-SPEC mode"

Pipeline to emulate (never skip steps): interpret → ToT → routing → SAFE-OUT → envelope
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

PORTABLE_VERSION = "2.2.7-P3-PORTABLE-SPEC"

# ---------------------------------------------------------------------------
# LLM guidance constants
# ---------------------------------------------------------------------------
EXAMPLE_QUERIES: List[Dict] = [
    {
        "query": "What is the capital of France?",
        "expected_route": "basic",
        "expected_confidence": 0.92,
        "reasoning_trace": "Interpret → brief ToT confirming Paris across recall and geography branches",
    },
    {
        "query": "Compare the economic impacts of carbon taxes versus cap-and-trade systems.",
        "expected_route": "structured",
        "expected_confidence": 0.60,
        "reasoning_trace": "Interpret → ToT branches: definitions, historical examples, trade-offs; synthesize contrasting outcomes",
    },
    {
        "query": "Give legal advice on forming a corporation without jurisdiction details.",
        "expected_route": "constrained",
        "expected_confidence": 0.38,
        "reasoning_trace": "Interpret → ToT considers ethics, jurisdiction gaps, safety; SAFE-OUT triggered to constrain guidance",
    },
]

LLM_REASONING_TEMPLATE: str = """
Tree-of-Thought execution guidance for LLMs:
- TEMPLATE_FUNCS (named strategies):
  1) Rephrase
  2) Decompose
  3) Edge Cases
  4) Counterpoints
  5) Synthesize
- Score each branch on relevance, completeness, and confidence. Average the three to produce the branch score.
- Continue exploring until a branch score >= 0.70 or depth >= 5; then select the best-scoring path.
- Prefer concise, evaluative notes over verbose narration.
"""

ENVELOPE_OUTPUT_EXAMPLE: str = """
solution: Provide a concise comparison of carbon taxes vs cap-and-trade with pros/cons and real-world examples.
confidence: 72%
route: SAFE-OUT (applied CoT fallback)
shortlist: [
  {"answer": "Initial ToT summary of carbon pricing mechanisms", "confidence": 0.58},
  {"answer": "Refined SAFE-OUT summary with cautions", "confidence": 0.72}
]
pending_questions: ["Which jurisdiction should the policy focus on?", "Is the audience policymakers or students?"]
notes: interpret → ToT → routing → SAFE-OUT → envelope
timestamp: 2024-05-01T12:00:00Z
version: 2.2.7-P3-PORTABLE-SPEC
"""

# ---------------------------------------------------------------------------
# Optional imports from the modular codebase. Everything here degrades
# gracefully so this file can run when copied into an isolated environment.
# ---------------------------------------------------------------------------
try:  # pragma: no cover - best effort
    from alpha.reasoning.tot import TreeOfThoughtSolver as ModularToTSolver  # type: ignore
except Exception:  # pragma: no cover
    ModularToTSolver = None  # type: ignore

try:  # pragma: no cover - best effort
    from alpha.policy.safe_out_sm import SafeOutStateMachine as ModularSafeOut  # type: ignore
    from alpha.policy.safe_out_sm import SOConfig as ModularSOConfig  # type: ignore
except Exception:  # pragma: no cover
    ModularSafeOut = None  # type: ignore
    ModularSOConfig = None  # type: ignore

# ---------------------------------------------------------------------------
# Lightweight observability primitives
# ---------------------------------------------------------------------------
@dataclass
class PortableEvent:
    """Structured event envelope used for logging and replay hints."""

    name: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: time.time())

    def serialize(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "payload": self.payload,
            "timestamp": datetime.fromtimestamp(self.timestamp, tz=timezone.utc).isoformat(),
        }


class PortableObservability:
    """Minimal observability collector.

    Keeps an in-memory log and exposes hook points used by the solver. The
    modular code writes JSONL, telemetry, and replay; here we keep enough shape
    to mirror that contract without external dependencies.
    """

    def __init__(self, session_id: Optional[str] = None) -> None:
        self.session_id = session_id or os.getenv("ALPHA_SESSION") or f"portable-{int(time.time())}"
        self.events: List[PortableEvent] = []

    def log_event(self, name: str, **payload: Any) -> None:
        event = PortableEvent(name=name, payload={"session_id": self.session_id, **payload})
        self.events.append(event)

    def export(self) -> List[Dict[str, Any]]:
        return [e.serialize() for e in self.events]


# ---------------------------------------------------------------------------
# Budget guard / accounting
# ---------------------------------------------------------------------------
@dataclass
class BudgetGuard:
    """Simulated budget guard inspired by ``alpha.observability.accounting.Accountant``."""

    max_expansions: int = 256
    max_sim_tokens: int = 4096
    expansions: int = 0
    sim_tokens: int = 0
    start: float = field(default_factory=time.time)

    def record(self, text: str) -> None:
        self.expansions += 1
        self.sim_tokens += len(text.split())

    @property
    def within_budget(self) -> bool:
        return self.expansions <= self.max_expansions and self.sim_tokens <= self.max_sim_tokens

    def summary(self) -> Dict[str, Any]:
        return {
            "expansions": self.expansions,
            "sim_tokens": self.sim_tokens,
            "elapsed_ms": int((time.time() - self.start) * 1000),
            "limits": {
                "max_expansions": self.max_expansions,
                "max_sim_tokens": self.max_sim_tokens,
            },
            "within_budget": self.within_budget,
        }


# ---------------------------------------------------------------------------
# Routing / policy gating
# ---------------------------------------------------------------------------
@dataclass
class RouteDecision:
    stage: str
    rationale: str
    profile: str
    escalations: List[str]


class PortableRouter:
    """Small deterministic router that mirrors ``alpha.router.ProgressiveRouter`` semantics."""

    def __init__(self, stages: Sequence[str] | None = None, min_progress: float = 0.3) -> None:
        self.stages = list(stages or ("basic", "structured", "constrained"))
        self.min_progress = min_progress
        self.stage = self.stages[0]
        self.progress = 0.0
        self.escalations: List[str] = []

    def decide(self, confidence: float) -> RouteDecision:
        self.progress = confidence
        while self.stages and self.progress < self.min_progress and len(self.escalations) + 1 < len(self.stages):
            next_stage = self.stages[len(self.escalations) + 1]
            self.escalations.append(next_stage)
        self.stage = self.escalations[-1] if self.escalations else self.stages[0]
        rationale = f"progress={self.progress:.2f} min={self.min_progress:.2f} stage={self.stage}"
        return RouteDecision(stage=self.stage, rationale=rationale, profile=self.stage, escalations=list(self.escalations))


# ---------------------------------------------------------------------------
# Deterministic reasoning core (portable ToT stub)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ToTNode:
    content: str
    path: Tuple[str, ...]
    depth: int
    score: float = 0.0
    id: int = 0


class PortableToTSolver:
    """Deterministic Tree-of-Thought stub.

    The modular solver lives in ``alpha.reasoning.tot``; this version mirrors
    the branching/score envelope shape and records budget events.
    """

    TEMPLATE_FUNCS: Tuple = (
        lambda q: f"Rephrase: {q}",
        lambda q: f"Decompose: {q}",
        lambda q: f"Edge cases: {q}",
        lambda q: f"Counterpoints: {q}",
        lambda q: f"Summarize: {q}",
    )

    def __init__(
        self,
        *,
        seed: int = 42,
        branching_factor: int = 3,
        score_threshold: float = 0.70,
        max_depth: int = 5,
        timeout_s: int = 8,
        budget_guard: Optional[BudgetGuard] = None,
    ) -> None:
        self.seed = seed
        self.branching_factor = branching_factor
        self.score_threshold = score_threshold
        self.max_depth = max_depth
        self.timeout_s = timeout_s
        self.rng = random.Random(seed)
        self.budget = budget_guard or BudgetGuard()
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _score(self, text: str, depth: int) -> float:
        base = self.rng.uniform(0.35, 0.95)
        depth_penalty = max(0.0, 0.1 * depth)
        return max(0.0, min(1.0, base - depth_penalty))

    def _expand(self, node: ToTNode) -> Iterable[ToTNode]:
        for tmpl in self.TEMPLATE_FUNCS[: self.branching_factor]:
            text = tmpl(node.content)
            self.budget.record(text)
            yield ToTNode(
                content=text,
                path=node.path + (text,),
                depth=node.depth + 1,
                score=self._score(text, node.depth + 1),
                id=self._next_id(),
            )

    def solve(self, query: str) -> Dict[str, Any]:
        start = time.time()
        root = ToTNode(content=query, path=(query,), depth=0, score=self._score(query, 0), id=self._next_id())
        best = root
        frontier: List[ToTNode] = [root]
        steps: List[Dict[str, Any]] = []
        while frontier and time.time() - start < self.timeout_s and self.budget.within_budget:
            node = frontier.pop(0)
            steps.append({"node": node.content, "score": node.score, "depth": node.depth})
            if node.score > best.score:
                best = node
            if node.score >= self.score_threshold or node.depth >= self.max_depth:
                continue
            for child in self._expand(node):
                frontier.append(child)
        return {
            "answer": best.content,
            "confidence": best.score,
            "steps": steps,
            "best_path": list(best.path),
            "best_path_hash": hash(best.path),
            "timed_out": time.time() - start >= self.timeout_s,
            "budget": self.budget.summary(),
        }


# ---------------------------------------------------------------------------
# SAFE-OUT / safety kernel
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PortableSOConfig:
    low_conf_threshold: float = 0.60
    enable_cot_fallback: bool = True
    seed: int = 42
    max_cot_steps: int = 4


class PortableSafeOut:
    """Safety kernel that mirrors ``alpha.policy.safe_out_sm.SafeOutStateMachine``."""

    def __init__(self, config: PortableSOConfig) -> None:
        self.config = config
        self.rng = random.Random(config.seed)

    def _cot(self, query: str) -> Dict[str, Any]:
        """LLM fallback playbook for CoT when confidence is low.

        - Re-examine the query from first principles and restate the goal.
        - Identify missing context or constraints that block a high-confidence answer.
        - Provide a best-effort response that marks uncertainty explicitly.
        - Offer concise follow-up questions to gather the missing details when doubt remains.
        """
        # Deterministic pseudo chain-of-thought fallback
        steps = [f"Step {i+1}: explore {query}" for i in range(self.config.max_cot_steps)]
        conf = min(0.65, 0.45 + 0.02 * len(query.split()))
        return {"answer": f"Clarify and refine: {query}", "confidence": conf, "steps": steps}

    def run(self, tot_result: Dict[str, Any], query: str) -> Dict[str, Any]:
        confidence = float(tot_result.get("confidence", 0.0))
        phases: List[str] = ["init"]
        if confidence >= self.config.low_conf_threshold:
            route = "tot"
            notes = "confidence above threshold"
            cot_result = None
        else:
            phases.append("fallback")
            cot_result = self._cot(query) if self.config.enable_cot_fallback else None
            if cot_result:
                route = "cot_fallback"
                confidence = cot_result.get("confidence", confidence)
                notes = "applied CoT fallback"
            else:
                route = "best_effort"
                notes = "no fallback available"
        phases.append("finalize")
        answer_src = cot_result or tot_result
        return {
            "final_answer": answer_src.get("answer", ""),
            "route": route,
            "confidence": confidence,
            "reason": tot_result.get("reason", "ok" if route == "tot" else "low_confidence"),
            "notes": f"{notes} | phases: {'->'.join(phases)}",
            "tot": tot_result,
            "cot": cot_result,
            "phases": phases,
            "recovery_notes": "" if route == "tot" else "used portable fallback",
        }


# ---------------------------------------------------------------------------
# Portable solver orchestration
# ---------------------------------------------------------------------------
@dataclass
class SolverDiagnostics:
    router: Dict[str, Any]
    safe_out: Dict[str, Any]
    tot: Dict[str, Any]
    observability_events: List[Dict[str, Any]]


@dataclass
class SolverEnvelope:
    solution: str
    confidence: float
    safe_out_state: Dict[str, Any]
    route_explain: str
    shortlist: List[Dict[str, Any]]
    pending_questions: List[str]
    diagnostics: SolverDiagnostics
    run_summary: Dict[str, Any]
    telemetry_contract: Dict[str, Any]
    timestamp: str
    version: str = PORTABLE_VERSION
    session_id: str = field(default_factory=lambda: f"portable-{int(time.time())}")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["diagnostics"] = asdict(self.diagnostics)
        return data

    def to_llm_response(self) -> str:
        shortlist_rendered = ", ".join(
            [f"{item.get('answer', '')} (conf={item.get('confidence', 0.0):.2f})" for item in self.shortlist]
        )
        confidence_pct = f"{self.confidence * 100:.0f}%"
        return (
            f"Solution: {self.solution}\n"
            f"Confidence: {confidence_pct}\n"
            f"Route: {self.safe_out_state.get('route')} | {self.route_explain}\n"
            f"Alternatives: {shortlist_rendered}\n"
            f"Pipeline: interpret → ToT → routing → SAFE-OUT → envelope"
        )


class PortableAlphaSolver:
    """Portable monolithic Alpha Solver.

    The architecture mirrors the modular engine: deterministic reasoning,
    SAFE-OUT kernel, routing/policy gating, budget guard, and observability.
    """

    def __init__(self, *, seed: int = 42, budget_guard: Optional[BudgetGuard] = None) -> None:
        self.seed = seed
        self.observability = PortableObservability()
        self.budget_guard = budget_guard or BudgetGuard()

    # ------------------------------------------------------------------
    # Component factories (allow modular reuse when present)
    # ------------------------------------------------------------------
    def _make_tot(self) -> Any:
        if ModularToTSolver is not None:  # pragma: no cover - modular path
            return ModularToTSolver(seed=self.seed, branching_factor=3, score_threshold=0.70, max_depth=5)
        return PortableToTSolver(seed=self.seed, budget_guard=self.budget_guard)

    def _make_safe_out(self) -> Any:
        if ModularSafeOut is not None and ModularSOConfig is not None:  # pragma: no cover
            return ModularSafeOut(ModularSOConfig(seed=self.seed))
        return PortableSafeOut(PortableSOConfig(seed=self.seed))

    def _make_router(self) -> PortableRouter:
        return PortableRouter()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def solve(self, query: str, *, deterministic: bool = False, context: Optional[Dict[str, Any]] = None) -> SolverEnvelope:
        context = context or {}
        seed = self.seed if deterministic else context.get("seed", self.seed)
        random.seed(seed)
        self.observability.log_event("solve_start", query=query, deterministic=deterministic)

        tot_solver = self._make_tot()
        router = self._make_router()
        tot_result = tot_solver.solve(query)

        route_decision = router.decide(confidence=float(tot_result.get("confidence", 0.0)))
        safe_out = self._make_safe_out()
        safe_out_state = safe_out.run(tot_result, query)

        shortlist = [
            {"answer": tot_result.get("answer", ""), "confidence": float(tot_result.get("confidence", 0.0))},
            {"answer": safe_out_state.get("final_answer", ""), "confidence": float(safe_out_state.get("confidence", 0.0))},
        ]

        run_summary = {
            "accounting": tot_result.get("budget", self.budget_guard.summary()),
            "deterministic": bool(deterministic),
            "seed": seed,
        }

        diagnostics = SolverDiagnostics(
            router={"stage": route_decision.stage, "rationale": route_decision.rationale, "escalations": route_decision.escalations},
            safe_out={"config": asdict(getattr(safe_out, "config", PortableSOConfig()))},
            tot={"steps": tot_result.get("steps", []), "best_path": tot_result.get("best_path", []), "timed_out": tot_result.get("timed_out", False)},
            observability_events=self.observability.export(),
        )

        envelope = SolverEnvelope(
            solution=safe_out_state.get("final_answer", tot_result.get("answer", "")),
            confidence=float(safe_out_state.get("confidence", tot_result.get("confidence", 0.0))),
            safe_out_state=safe_out_state,
            route_explain=route_decision.rationale,
            shortlist=shortlist,
            pending_questions=[],
            diagnostics=diagnostics,
            run_summary=run_summary,
            telemetry_contract={"observability": "portable"},
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=PORTABLE_VERSION,
            session_id=self.observability.session_id,
        )

        self.observability.log_event("solve_end", outcome="ok", confidence=envelope.confidence)
        return envelope


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Portable Alpha Solver")
    parser.add_argument("query", help="User query to solve")
    parser.add_argument("--json", dest="json_output", action="store_true", help="Emit full envelope JSON")
    parser.add_argument("--deterministic", action="store_true", help="Force deterministic seed")
    parser.add_argument("--seed", type=int, default=42, help="Seed override for deterministic replay")
    args = parser.parse_args()

    solver = PortableAlphaSolver(seed=args.seed)
    envelope = solver.solve(args.query, deterministic=args.deterministic)

    if args.json_output:
        print(json.dumps(envelope.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"Alpha Solver {envelope.version} | confidence={envelope.confidence:.2f}")
        print(f"Solution: {envelope.solution}")
        print(f"Route: {envelope.safe_out_state.get('route')} ({envelope.route_explain})")
        print(f"Budget: {envelope.run_summary['accounting']}")


if __name__ == "__main__":  # pragma: no cover
    _cli()

# PIPELINE CONFIRMATION FORMAT:
# "Alpha Solver v2.2.7-P3 (PORTABLE-SPEC) pipeline executed: interpret → ToT → routing → SAFE-OUT → envelope."
