# Enhanced Design Brief: deep-research-improve-skill

_Generated: 2026-03-15 | Sources: 30+ | Rounds: 2 (from deep-research + research on the domain)_

## Prior Art

- **research-improve-skill**: Single-round Sonnet-only research before improvement. Works well for familiar domains but misses nuanced best practices in complex domains. `[Confidence: HIGH]`
- **improve-skill**: No research at all — relies on built-in best practices only. Fast but may miss domain-specific improvements. `[Confidence: HIGH]`
- **D3 Framework (Debate, Deliberate, Decide)**: Role-specialized agents with confidence-weighted verdicts — directly applicable to improvement synthesis. `[Confidence: HIGH]`

## Domain Patterns

- **Research-backed improvements are more durable**: Improvements grounded in domain research are less likely to be reverted or cause regressions. `[Confidence: MEDIUM]`
- **Skeptic agent is especially valuable for improvement**: Sometimes the current approach is already optimal. A skeptic that defends the status quo prevents unnecessary churn. `[Confidence: HIGH]`
- **Confidence tagging aids user decision-making**: Users can prioritize HIGH-confidence improvements and defer LOW-confidence ones. 58% of skeptical users want explicit uncertainty visualization. `[Confidence: MEDIUM]`
- **Tiered model strategy**: Fast models for data collection, best models for analysis — same pattern as deep-research. `[Confidence: HIGH]`

## Pitfalls to Avoid

- **Improvement bias**: AI systems tend to suggest changes even when none are needed. Explicit "if high quality, say so" instruction needed. `[Confidence: HIGH]` — **MUST be addressed in Rules**
- **Citation hallucination**: Same as generate skill — 60%+ AI citation failure rate. `[Confidence: HIGH]` — **MUST be addressed in Rules**
- **Complexity creep**: Research may suggest adding features that increase complexity without proportional benefit. Skeptic should evaluate complexity-benefit ratio. `[Confidence: HIGH]` — **MUST be addressed via skeptic**
- **Loss of skill identity**: Over-improvement can change a skill's personality and purpose. Must preserve intent. `[Confidence: HIGH]` — **MUST be addressed in Rules**
- **Outdated suggestions**: Research may find "best practices" that are already outdated. Domain evolution lens helps but isn't foolproof. `[Confidence: MEDIUM]`

## Recommended Approach

1. Embed deep-research's two-round architecture into the improvement pipeline
2. Skeptic agent should specifically challenge improvement assumptions — defend the status quo
3. Tag every research-backed improvement with confidence level
4. Always create backup before modifications
5. Present skeptic's assessment prominently so users can make informed decisions
6. Never write to the skill directory before user approval

## Contradictions & Open Questions

- **Depth vs. speed tradeoff**: Deep research improvement takes ~15-17min vs ~7.5min for research-improve-skill. For quick fixes, the lighter skill is better.
- **Skeptic for improvements**: Strong evidence that adversarial review improves factual research. Less clear that it helps improvement suggestions specifically. Decision: include because preventing unnecessary changes is high-value.

## Knowledge Gaps

- **Measuring improvement quality**: No standardized metric for "improvement quality" — hard to objectively measure whether deeper research produces better improvements
- **User preference for confidence tags**: Anecdotal that users want transparency, but no rigorous study on how confidence tags affect improvement acceptance rates

## Sources

| # | Source | URL | Credibility | Round |
|---|--------|-----|-------------|-------|
| 1 | Deep Research Survey (arXiv) | https://arxiv.org/pdf/2508.12752 | HIGH | 1 |
| 2 | FlowSearch Architecture (arXiv) | https://arxiv.org/html/2510.08521v1 | HIGH | 1 |
| 3 | Multi-agent Debate (Springer) | https://link.springer.com/article/10.1007/s44443-025-00353-3 | HIGH | 2 |
| 4 | Adversarial Debate Voting (MDPI) | https://www.mdpi.com/2076-3417/15/7/3676 | HIGH | 2 |
| 5 | LLM Debate Study (arXiv) | https://arxiv.org/html/2511.07784v1 | HIGH | 2 |
| 6 | D3 Framework (arXiv) | https://arxiv.org/abs/2410.04663 | HIGH | 2 |
| 7 | DR-Arena Evaluation (arXiv) | https://arxiv.org/html/2601.10504v1 | HIGH | 1 |
| 8 | GPT-Researcher Features (Dify) | https://dify.ai/blog/enhancing-gpt-researcher-with-parallel-and-advanced-iterative-features | MEDIUM | 1 |
| 9 | Red Teaming Guide (Promptfoo) | https://www.promptfoo.dev/docs/red-team/ | MEDIUM | 2 |
| 10 | Source Credibility Scoring (Sourcely) | https://www.sourcely.net/resources/what-is-automated-source-credibility-scoring | MEDIUM | 1 |
