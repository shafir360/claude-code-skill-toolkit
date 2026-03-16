# Improvement Research Brief: exhaustive-research

_Generated: 2026-03-16 | Sources: 25+ | Rounds: 2 | Focus: Safety & Resilience_

## Research Summary

Two rounds of research across 5 themes (checkpointing, progress reporting, circuit breakers, graceful degradation, timeout strategies) with gap analysis and adversarial skeptic review.

## Key Findings Applied

### HIGH Confidence (3+ sources, survived skeptic)

1. **Phase-boundary checkpointing is sufficient** — per-agent overhead disproportionate for LLM agents costing seconds each. File-based output serves as implicit sub-phase checkpoint. (LangGraph superstep model, Ray distributed checkpointing, Spark stage-level patterns)
2. **Structural validation only for circuit breakers** — semantic quality detection is ~53% accurate (MAST paper). False positives cascade and can poison 87% of downstream decisions. Check format, not meaning. (arxiv 2503.13657, OWASP ASI08, Galileo)
3. **Skip-and-note over retry storms** — real incident: naive retries on 100K+ token Opus context caused $10+/day cost spikes. 3-tier retry across 80 agents could 2-4x costs. (openclaw issue, Portkey, Galileo)
4. **Plain text progress is sufficient** — users with any feedback waited 22.6s vs 9s with none. Rich UI not required. Ansible TASK/RECAP pattern works in CLI. (Evil Martians, Nielsen Norman Group)
5. **LLMs cannot self-enforce token budgets** — TALE framework proves models exceed budgets when constraints are tight. Hard enforcement at orchestration layer needed. (arxiv 2412.18547)

### MEDIUM Confidence (2 sources or counter-evidence)

6. **Early termination on bad query sets** — <20% screening pass rate signals query mismatch. Prevents wasting hours. (Derived from PICO recall research + STORM query diversification)
7. **>30% failure rate triggers user intervention** — no universal threshold exists (ReliabilityBench), but 30% balances coverage preservation with quality risk.

## Skeptic's Verdicts

| Assumption | Verdict | Impact on Skill |
|---|---|---|
| Semantic circuit breakers work | **Rejected** | Changed to structural-only validation gates |
| 3-tier retry fallback is practical | **Rejected** | Simplified to skip-and-note, max 1 retry for timeout only |
| Phase-boundary checkpointing is sufficient | **Confirmed** | Implemented phase-level JSON checkpoints + implicit file checkpoints |

## Top Sources

- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — HIGH
- [LangGraph Map-Reduce](https://langchain-ai.github.io/langgraphjs/how-tos/map-reduce/) — HIGH
- [Why Multi-Agent Systems Fail (MAST)](https://arxiv.org/abs/2503.13657) — HIGH
- [TALE Token Budget Framework](https://arxiv.org/abs/2412.18547) — HIGH
- [Evil Martians CLI UX Patterns](https://evilmartians.com/chronicles/cli-ux-best-practices-3-patterns-for-improving-progress-displays) — HIGH
- [Nielsen Norman Group: Designing for Waits](https://www.nngroup.com/articles/designing-for-waits-and-interruptions/) — HIGH
- [Retries/Fallbacks/Circuit Breakers - Portkey](https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/) — HIGH
- [Smashing Magazine: Agentic AI UX](https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/) — HIGH
- [Galileo: Multi-Agent Failures](https://galileo.ai/blog/multi-agent-llm-systems-fail) — MEDIUM
- [OWASP ASI08 Cascading Failures](https://adversa.ai/blog/cascading-failures-in-agentic-ai-complete-owasp-asi08-security-guide-2026/) — MEDIUM
- [ReliabilityBench](https://arxiv.org/abs/2601.06112) — HIGH
- [FAME: Taming Silent Failures](https://www.arxiv.org/pdf/2510.22224) — HIGH
