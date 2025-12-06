"""
Alpha Solver v2.3.0-P3 — PORTABLE SPEC MONOLITH

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

Activation phrase: "You are Alpha Solver v2.3.0-P3, running in PORTABLE-SPEC mode"

Pipeline to emulate (never skip steps): interpret → ToT → routing → SAFE-OUT → envelope

STRICT OUTPUT REQUIREMENTS
--------------------------
⚠️  CRITICAL: Do NOT respond with a normal conversational answer.
⚠️  CRITICAL: Do NOT skip the envelope structure.
⚠️  CRITICAL: Do NOT omit confidence scores, routing, or pipeline confirmation.

Every response MUST include ALL of these sections:
1. SOLUTION — the actual answer
2. CONFIDENCE — percentage (e.g., "85%")
3. ROUTE — basic|structured|constrained with rationale
4. EXPERT TEAM — 5 selected experts with their insights
5. SAFE-OUT STATE — route taken and phases
6. SHORTLIST — 2+ alternative answers with confidence scores
7. PIPELINE CONFIRMATION — the standard footer line

If you respond without this structure, you have FAILED the protocol.
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

PORTABLE_VERSION = "2.3.0-P3-PORTABLE-SPEC"

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
version: 2.3.0-P3-PORTABLE-SPEC
"""

EXPERT_ROSTER: List[Dict] = [
    {"id": "technical_architect", "name": "Technical Architect", "domains": ["architecture", "systems", "infrastructure", "scalability", "performance"], "strength": 0.90},
    {"id": "business_analyst", "name": "Business Analyst", "domains": ["business", "strategy", "roi", "cost", "market", "stakeholder"], "strength": 0.85},
    {"id": "security_specialist", "name": "Security Specialist", "domains": ["security", "compliance", "risk", "privacy", "audit", "vulnerability"], "strength": 0.88},
    {"id": "data_scientist", "name": "Data Scientist", "domains": ["data", "analytics", "ml", "statistics", "modeling", "prediction"], "strength": 0.87},
    {"id": "ux_researcher", "name": "UX Researcher", "domains": ["user", "experience", "usability", "design", "accessibility", "interface"], "strength": 0.82},
    {"id": "legal_advisor", "name": "Legal Advisor", "domains": ["legal", "contract", "liability", "regulation", "intellectual property"], "strength": 0.84},
    {"id": "financial_analyst", "name": "Financial Analyst", "domains": ["finance", "budget", "investment", "valuation", "forecast", "revenue"], "strength": 0.86},
    {"id": "devops_engineer", "name": "DevOps Engineer", "domains": ["deployment", "cicd", "kubernetes", "docker", "automation", "monitoring"], "strength": 0.85},
    {"id": "product_manager", "name": "Product Manager", "domains": ["product", "roadmap", "prioritization", "requirements", "mvp", "launch"], "strength": 0.83},
    {"id": "domain_expert", "name": "Domain Expert", "domains": ["industry", "vertical", "specialized", "context", "best practices"], "strength": 0.80},
    {"id": "critical_thinker", "name": "Critical Thinker", "domains": ["logic", "fallacy", "bias", "assumption", "counterargument"], "strength": 0.88},
    {"id": "creative_strategist", "name": "Creative Strategist", "domains": ["innovation", "brainstorm", "alternative", "unconventional", "ideation"], "strength": 0.79},
]

EXPERT_SELECTION_TEMPLATE: str = """
Expert Selection Protocol:
1. CLASSIFY the query into 1-3 primary domains
2. MATCH experts whose domains overlap with query domains
3. SCORE each expert: domain_overlap_count × expert_strength
4. SELECT top 5 experts by score
5. ASSIGN roles: Lead Expert (highest score), Supporting Experts (next 4)
6. For each expert, generate a 1-sentence perspective on the query

Output format:
- Lead: [Expert Name] — "[Key insight]"
- Support: [Expert Name] — "[Perspective]"
- Support: [Expert Name] — "[Perspective]"
- Support: [Expert Name] — "[Perspective]"
- Support: [Expert Name] — "[Perspective]"

Synergy score = average of selected expert strengths
"""

COMPLIANCE_EXAMPLES: Dict[str, str] = {
    "NON_COMPLIANT": """
❌ WRONG - This violates the protocol:

"Microservices offer better scalability while monoliths are simpler..."

Why it fails: No envelope structure, no confidence, no experts, no pipeline confirmation.
""",
    "COMPLIANT": """
✅ CORRECT - This follows the protocol:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOLVER ENVELOPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SOLUTION:
[Concise answer here]

CONFIDENCE: 85%

ROUTE: structured | progress=0.85 min=0.30

EXPERT TEAM (Synergy: 0.87):
- Lead: Technical Architect — "Focus on scalability requirements"
- Support: DevOps Engineer — "Consider deployment complexity"
- Support: Business Analyst — "Evaluate team size and budget"
- Support: Security Specialist — "Assess attack surface differences"
- Support: Critical Thinker — "Challenge assumptions about scale needs"

SAFE-OUT STATE:
  route: tot
  notes: confidence above threshold | phases: init->finalize

SHORTLIST:
  1. "Context-dependent recommendation" (0.85)
  2. "Monolith-first approach" (0.72)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Alpha Solver v2.3.0-P3 (PORTABLE-SPEC) pipeline executed:
interpret → ToT (5 experts) → routing → SAFE-OUT → envelope.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
}

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


@dataclass
class ExpertTeam:
    """Selected expert team for a query."""

    lead: Dict[str, Any]
    supporting: List[Dict[str, Any]]
    synergy_score: float
    domain_classification: List[str]

    def to_display(self) -> str:
        lines = [f"- Lead: {self.lead['name']} — \"{self.lead.get('insight', 'Primary analysis')}\""]
        for expert in self.supporting:
            lines.append(f"- Support: {expert['name']} — \"{expert.get('insight', 'Supporting analysis')}\"")
        return "\n".join(lines)


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


class PortableExpertSelector:
    """Selects optimal expert team based on query domain classification."""

    def __init__(self, roster: List[Dict] = None):
        self.roster = roster or EXPERT_ROSTER

    def classify_domains(self, query: str) -> List[str]:
        """Extract domain keywords from query."""
        query_lower = query.lower()
        all_domains = set()
        for expert in self.roster:
            for domain in expert["domains"]:
                if domain in query_lower:
                    all_domains.add(domain)
        if not all_domains:
            all_domains = {"general", "analysis"}
        return list(all_domains)[:5]

    def select_team(self, query: str, team_size: int = 5) -> ExpertTeam:
        """Select top experts for the query."""
        domains = self.classify_domains(query)

        scored = []
        for expert in self.roster:
            overlap = len(set(expert["domains"]) & set(domains))
            score = overlap * expert["strength"] + expert["strength"] * 0.1
            scored.append((score, expert))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = [exp for _, exp in scored[:team_size]]

        lead = {**selected[0], "insight": f"Lead analysis on {domains[0] if domains else 'general'} aspects"}
        supporting = [
            {**exp, "insight": f"Perspective on {exp['domains'][0]} considerations"}
            for exp in selected[1:]
        ]

        synergy = sum(exp["strength"] for exp in selected) / len(selected)

        return ExpertTeam(
            lead=lead,
            supporting=supporting,
            synergy_score=round(synergy, 2),
            domain_classification=domains
        )


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
        initial_confidence = confidence
        phases: List[str] = ["init"]
        if confidence >= self.config.low_conf_threshold:
            route = "tot"
            reason = "confidence_above_threshold"
            notes = "confidence above threshold"
            cot_result = None
        else:
            phases.append("fallback")
            cot_result = self._cot(query) if self.config.enable_cot_fallback else None
            if cot_result:
                route = "cot_fallback"
                confidence = cot_result.get("confidence", confidence)
                reason = "low_confidence_tot_fallback_to_cot"
                notes = "applied CoT fallback"
            else:
                route = "best_effort"
                reason = "low_confidence_no_fallback_available"
                notes = "no fallback available"
        phases.append("finalize")
        answer_src = cot_result or tot_result
        return {
            "final_answer": answer_src.get("answer", ""),
            "route": route,
            "confidence": confidence,
            "reason": tot_result.get("reason", reason),
            "notes": f"route={route} | initial_confidence={initial_confidence:.2f} | {notes} | phases: {'->'.join(phases)}",
            "tot": tot_result,
            "cot": cot_result,
            "phases": phases,
            "recovery_notes": "" if route == "tot" else "used portable fallback",
            "policy_profile": "default",
            "thresholds": {"low_conf_threshold": float(self.config.low_conf_threshold)},
        }


# ---------------------------------------------------------------------------
# Portable solver orchestration
# ---------------------------------------------------------------------------
@dataclass
class SolverDiagnostics:
    router: Dict[str, Any]
    safe_out: Dict[str, Any]
    tot: Dict[str, Any]
    expert_selection: Dict[str, Any] = field(default_factory=dict)
    observability_events: List[Dict[str, Any]] = field(default_factory=list)


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
    meta: Dict[str, Any] = field(default_factory=dict)
    expert_team: Optional["ExpertTeam"] = None
    version: str = PORTABLE_VERSION
    session_id: str = field(default_factory=lambda: f"portable-{int(time.time())}")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["diagnostics"] = asdict(self.diagnostics)
        return data

    def to_llm_response(self) -> str:
        shortlist_rendered = "\n".join(
            [f"  {i+1}. \"{item.get('answer', '')[:50]}...\" ({item.get('confidence', 0.0):.2f})" for i, item in enumerate(self.shortlist)]
        )
        confidence_pct = f"{self.confidence * 100:.0f}%"

        expert_section = ""
        if self.expert_team:
            expert_section = f"EXPERT TEAM (Synergy: {self.expert_team.synergy_score}):\n{self.expert_team.to_display()}\n\n"

        return (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"SOLVER ENVELOPE\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"SOLUTION:\n{self.solution}\n\n"
            f"CONFIDENCE: {confidence_pct}\n\n"
            f"ROUTE: {self.safe_out_state.get('route')} | {self.route_explain}\n\n"
            f"{expert_section}"
            f"SAFE-OUT STATE:\n  route: {self.safe_out_state.get('route')}\n  notes: {self.safe_out_state.get('notes')}\n\n"
            f"SHORTLIST:\n{shortlist_rendered}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Alpha Solver v2.3.0-P3 (PORTABLE-SPEC) pipeline executed:\n"
            f"interpret → ToT (5 experts) → routing → SAFE-OUT → envelope.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
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
        self.expert_selector = PortableExpertSelector()

    # ------------------------------------------------------------------
    # Component factories (allow modular reuse when present)
    # ------------------------------------------------------------------
    def _make_tot(self, seed: Optional[int] = None) -> Any:
        seed = seed if seed is not None else self.seed
        if ModularToTSolver is not None:  # pragma: no cover - modular path
            return ModularToTSolver(seed=seed, branching_factor=3, score_threshold=0.70, max_depth=5)
        return PortableToTSolver(seed=seed, budget_guard=self.budget_guard)

    def _make_safe_out(self, seed: Optional[int] = None) -> Any:
        seed = seed if seed is not None else self.seed
        if ModularSafeOut is not None and ModularSOConfig is not None:  # pragma: no cover
            return ModularSafeOut(ModularSOConfig(seed=seed))
        return PortableSafeOut(PortableSOConfig(seed=seed))

    def _make_router(self) -> PortableRouter:
        return PortableRouter()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def solve(self, query: str, *, deterministic: bool = False, context: Optional[Dict[str, Any]] = None) -> SolverEnvelope:
        context = context or {}
        vertical_id = context.get("vertical_id", "generic")
        routing_profile_id = context.get("routing_profile_id", "default")
        seed = self.seed if deterministic else context.get("seed", self.seed)
        random.seed(seed)
        self.observability.log_event(
            "solve_start",
            query=query,
            deterministic=deterministic,
            event_type="lifecycle",
            stage="start",
            vertical_id=vertical_id,
            routing_profile_id=routing_profile_id,
        )

        tot_solver = self._make_tot(seed=seed)
        router = self._make_router()
        tot_result = tot_solver.solve(query)

        route_decision = router.decide(confidence=float(tot_result.get("confidence", 0.0)))
        expert_team = self.expert_selector.select_team(query)
        safe_out = self._make_safe_out(seed=seed)
        safe_out_state = safe_out.run(tot_result, query)

        shortlist = [
            {"answer": tot_result.get("answer", ""), "confidence": float(tot_result.get("confidence", 0.0))},
            {"answer": safe_out_state.get("final_answer", ""), "confidence": float(safe_out_state.get("confidence", 0.0))},
        ]

        run_summary = {
            "accounting": tot_result.get("budget", self.budget_guard.summary()),
            "deterministic": bool(deterministic),
            "seed": seed,
            "vertical_id": vertical_id,
            "routing_profile_id": routing_profile_id,
        }

        diagnostics = SolverDiagnostics(
            router={"stage": route_decision.stage, "rationale": route_decision.rationale, "escalations": route_decision.escalations},
            safe_out={"config": asdict(getattr(safe_out, "config", PortableSOConfig()))},
            tot={"steps": tot_result.get("steps", []), "best_path": tot_result.get("best_path", []), "timed_out": tot_result.get("timed_out", False)},
            expert_selection={"lead": expert_team.lead["id"], "team_size": 5, "synergy": expert_team.synergy_score, "domains": expert_team.domain_classification},
            observability_events=self.observability.export(),
        )

        envelope = SolverEnvelope(
            solution=safe_out_state.get("final_answer", tot_result.get("answer", "")),
            confidence=float(safe_out_state.get("confidence", tot_result.get("confidence", 0.0))),
            safe_out_state=safe_out_state,
            route_explain=route_decision.rationale,
            shortlist=shortlist,
            expert_team=expert_team,
            pending_questions=[],
            diagnostics=diagnostics,
            run_summary=run_summary,
            telemetry_contract={"observability": "portable"},
            timestamp=datetime.now(timezone.utc).isoformat(),
            meta={"vertical_id": vertical_id, "routing_profile_id": routing_profile_id},
            version=PORTABLE_VERSION,
            session_id=self.observability.session_id,
        )

        env_dict = envelope.to_dict()
        validation = validate_envelope_dict(env_dict)
        if not validation["ok"]:
            self.observability.log_event(
                "envelope_validation_failed",
                event_type="validation",
                stage="post_solve",
                errors=validation["errors"],
                error_count=len(validation["errors"]),
            )

        self.observability.log_event(
            "solve_end",
            outcome="ok",
            confidence=envelope.confidence,
            event_type="lifecycle",
            stage="end",
            vertical_id=vertical_id,
            routing_profile_id=routing_profile_id,
        )
        return envelope


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


def validate_envelope_dict(env: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lightweight validation for SolverEnvelope dicts.
    Returns {"ok": bool, "errors": List[str]}.
    NEVER raises exceptions.
    """
    errors: List[str] = []

    required_top = [
        "solution",
        "confidence",
        "safe_out_state",
        "route_explain",
        "shortlist",
        "diagnostics",
        "run_summary",
        "timestamp",
        "version",
        "session_id",
    ]

    for key in required_top:
        if key not in env:
            errors.append(f"missing top-level field: {key}")

    if not isinstance(env.get("confidence"), (int, float)):
        errors.append("confidence must be numeric")

    if not isinstance(env.get("safe_out_state"), dict):
        errors.append("safe_out_state must be a dict")

    return {"ok": len(errors) == 0, "errors": errors}


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
# "Alpha Solver v2.3.0-P3 (PORTABLE-SPEC) pipeline executed: interpret → ToT (5 experts) → routing → SAFE-OUT → envelope."
