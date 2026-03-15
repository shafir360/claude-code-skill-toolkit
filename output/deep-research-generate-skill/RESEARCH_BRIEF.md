# Enhanced Design Brief: deep-research-generate-skill

_Generated: 2026-03-15 | Sources: 30+ | Rounds: 2 (from deep-research + research on the domain)_

## Prior Art

- **research-generate-skill**: Single-round Sonnet-only research before generation. Works well for familiar domains but insufficient for complex/unfamiliar ones. `[Confidence: HIGH]`
- **OpenAI Deep Research**: Uses ReAct Plan-Act-Observe loop with RL-trained reasoning, 10-30+ minutes per session, dozens of searches. Demonstrates the value of iterative research rounds. `[Confidence: HIGH]`
- **Gemini Deep Research**: Multi-agent orchestration with visible research plan for user review — a pattern worth adopting for research transparency. `[Confidence: HIGH]`
- **Perplexity Deep Research**: 3-stage retrieval-reasoning-refinement with hybrid model selection per sub-task — validates the tiered model approach. `[Confidence: HIGH]`

## Domain Patterns

- **Two-round architecture is standard**: All leading deep research tools use iterative rounds — broad sweep first, then targeted deep dives based on gaps. `[Confidence: HIGH]`
- **Tiered model strategy works**: Using fast models (Sonnet) for data collection and best models (Opus) for analysis achieves ~91% vs ~82% accuracy on reasoning tasks compared to single-model approaches. `[Confidence: HIGH]`
- **Heterogeneous agents outperform homogeneous**: Different model tiers provide architectural diversity that is the primary defense against shared blind spots. `[Confidence: HIGH]`
- **Global Research Context**: Centralizing prior search results prevents redundant work across rounds. `[Confidence: MEDIUM]`

## Pitfalls to Avoid

- **Citation hallucination**: AI citation failure rates exceed 60% (Tow Center/Columbia study). URLs may be real but claims attributed to them fabricated. `[Confidence: HIGH]` — **MUST be addressed in Rules**
- **Chat-Chamber effect**: AI confirms user assumptions rather than challenging them. Explicit counter-prompting needed. `[Confidence: HIGH]` — **MUST be addressed via skeptic agent**
- **Work redundancy**: Multi-agent systems exhibit 0.41-0.50 redundancy rates without explicit differentiation. Each agent needs non-overlapping focus. `[Confidence: HIGH]` — **MUST be addressed in agent dispatch**
- **Decomposition unreliability**: 112% increase in output unreliability in multi-turn settings. Careful sub-query design is critical. `[Confidence: MEDIUM]`
- **Minority correction asymmetry**: A confident-but-wrong agent can sway the group. Skeptic must challenge majority regardless of confidence. `[Confidence: HIGH]`

## Recommended Approach

1. Embed deep-research's two-round architecture directly into the skill generation pipeline
2. Use tiered models: Sonnet for R1/R2 data collection, Opus for gap analysis + skeptic + synthesis
3. Produce an Enhanced Design Brief (not just basic brief) with per-finding confidence levels
4. Rules section must address HIGH-confidence pitfalls (citation hallucination, Chat-Chamber, redundancy)
5. Include skeptic agent impact in the presentation to the user

## Contradictions & Open Questions

- **Research depth vs. generation speed**: Deeper research takes more time (15-17min vs 9min). Users wanting quick generation should use /research-generate-skill instead.
- **Skeptic value**: While research supports adversarial agents improving accuracy, there's debate about whether this matters for skill generation specifically (vs. factual research). Decision: include skeptic for domain research, as incorrect domain understanding leads to poorly designed skills.

## Knowledge Gaps

- **Optimal research-to-generation time ratio**: No clear evidence on exactly how much research time produces diminishing returns for code generation quality
- **Impact measurement**: No standardized way to measure whether deeper research produces measurably better skills

## Sources

| # | Source | URL | Credibility | Round |
|---|--------|-----|-------------|-------|
| 1 | Deep Research Survey (arXiv) | https://arxiv.org/pdf/2508.12752 | HIGH | 1 |
| 2 | FlowSearch Architecture (arXiv) | https://arxiv.org/html/2510.08521v1 | HIGH | 1 |
| 3 | DR-Arena Evaluation (arXiv) | https://arxiv.org/html/2601.10504v1 | HIGH | 1 |
| 4 | Multi-agent Debate (Springer) | https://link.springer.com/article/10.1007/s44443-025-00353-3 | HIGH | 2 |
| 5 | Adversarial Debate Voting (MDPI) | https://www.mdpi.com/2076-3417/15/7/3676 | HIGH | 2 |
| 6 | LLM Debate Study (arXiv) | https://arxiv.org/html/2511.07784v1 | HIGH | 2 |
| 7 | D3 Framework (arXiv) | https://arxiv.org/abs/2410.04663 | HIGH | 2 |
| 8 | GPT-Researcher Parallel Features (Dify) | https://dify.ai/blog/enhancing-gpt-researcher-with-parallel-and-advanced-iterative-features | MEDIUM | 1 |
| 9 | Automated Source Credibility (Sourcely) | https://www.sourcely.net/resources/what-is-automated-source-credibility-scoring | MEDIUM | 1 |
| 10 | Deep Research Workflow (Dify) | https://dify.ai/blog/deep-research-workflow-in-dify-a-step-by-step-guide | MEDIUM | 1 |
