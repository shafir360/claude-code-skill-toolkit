# Design Brief: deep-research skill
_Generated: 2026-03-15 | Sources: 30+_

## Prior Art

### Existing Deep Research Systems
- **OpenAI Deep Research**: ReAct Plan-Act-Observe loop trained via RL. 10-30+ minutes per session, dozens of searches. Produces 5,000-12,000 word reports with numbered citations and export options.
- **Gemini Deep Research**: Multi-agent orchestration with visible research plan for user review before execution. Two-panel UI separating process log from final report. Paragraph-level citations.
- **Perplexity Deep Research**: 3-stage retrieval-reasoning-refinement cycle. Hybrid model selection per sub-task. Inline numbered citations with source panel. Splits queries into subtopic dimensions with 3-5 searches per dimension.

### Key Architectural Pattern
All leading systems use iterative rounds (broad sweep → targeted deep dives). A "Global Research Context" pattern centralizes memory of prior searches to prevent redundant work.

## Domain Patterns

### Multi-Round Architecture
- Round 1 broad sweep identifies themes and collects initial data
- Gap analysis between rounds identifies weak spots, contradictions, and missing angles
- Round 2 targets specific gaps with focused queries
- Progressive knowledge accumulation (not a reset between rounds)

### Tiered Model Strategy
- Fast models for data collection (search, fetch, extract)
- Best models for analysis, synthesis, and adversarial review
- Heterogeneous agents achieve ~91% vs ~82% accuracy on reasoning tasks

### Adversarial/Skeptic Patterns
- D3 framework (Debate, Deliberate, Decide): Role-specialized agents with confidence-weighted verdicts
- Multi-turn escalation beats single-shot adversarial prompts
- Skeptic must challenge majority consensus regardless of confidence (minority correction asymmetry)

## Pitfalls to Avoid

1. **Citation hallucination** (60%+ failure rate): AI search engines fail to produce accurate citations in over 60% of tests. Citation mismatch (URL real, claim fabricated) is the sneakiest failure mode.
2. **Chat-Chamber effect**: AI systems confirm user assumptions rather than challenging them. Explicit counter-prompting and dedicated skeptic agents are required.
3. **AI-sourcing-AI feedback loop**: 85% of web content is machine-generated. Deep research tools may recycle AI-generated content as authoritative sources.
4. **Work redundancy**: Multi-agent systems exhibit 0.41-0.50 redundancy rates without explicit differentiation between agents.
5. **Decomposition unreliability**: Query decomposition causes 112% increase in output unreliability in multi-turn settings — careful sub-query design is critical.
6. **No explicit confidence scores**: None of the big 3 (OpenAI, Gemini, Perplexity) show numerical confidence — but 58% of skeptical users want explicit uncertainty visualization.
7. **Practical reasoning gap**: GPT-4 achieves only 15% accuracy vs 92% human on practical reasoning tasks — reports must flag when human verification is essential.

## Recommended Approach

1. **Two-round architecture** with gap analysis between rounds (proven by all leading systems)
2. **Tiered model strategy**: Sonnet for fast data collection, Opus for analysis/synthesis/skeptic
3. **Visible research plan** (Gemini pattern) — present to user before executing
4. **Dedicated Opus skeptic agent** in Round 2 that challenges strongest claims from Round 1
5. **Per-finding confidence levels** (High/Medium/Low) based on source count and agreement — addressing the gap none of the big 3 fill
6. **Mandatory contradiction section** — always present, even if "none found"
7. **Citation-mismatch mitigation**: Never generate URLs from memory, flag single-source claims, cross-validate across agents
8. **Human verification flags** for critical domains (medical, legal, financial, safety)

## Sources

| # | Source | URL | Credibility |
|---|--------|-----|-------------|
| 1 | OpenAI — Introducing Deep Research | https://openai.com/index/introducing-deep-research/ | HIGH |
| 2 | OpenAI — Deep Research System Card | https://cdn.openai.com/deep-research-system-card.pdf | HIGH |
| 3 | arXiv — Deep Researcher with Sequential Plan Reflection | https://arxiv.org/pdf/2601.20843 | HIGH |
| 4 | arXiv — Comprehensive Survey of Deep Research Systems | https://arxiv.org/pdf/2506.12594 | HIGH |
| 5 | arXiv — DR-Arena Evaluation Framework | https://arxiv.org/abs/2601.10504v1 | HIGH |
| 6 | arXiv — FlowSearch: Dynamic Structured Knowledge Flow | https://arxiv.org/html/2510.08521v1 | HIGH |
| 7 | arXiv — Can LLM Agents Really Debate? | https://arxiv.org/html/2511.07784v1 | HIGH |
| 8 | arXiv — D3: Debate, Deliberate, Decide | https://arxiv.org/abs/2410.04663 | HIGH |
| 9 | arXiv — How Far Are We from Useful Deep Research Agents? | https://www.arxiv.org/pdf/2512.01948 | HIGH |
| 10 | MDPI — Adversarial Debate and Voting Mechanisms | https://www.mdpi.com/2076-3417/15/7/3676 | HIGH |
| 11 | SAGE — Chat-Chamber Effect | https://journals.sagepub.com/doi/10.1177/20539517241306345 | HIGH |
| 12 | Frontiers — Uncertainty Visualization and Trust | https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1464348/full | HIGH |
| 13 | Nieman Lab — AI Citation Failure Rate 60%+ | https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/ | HIGH |
| 14 | Fortune — NeurIPS Hallucinated Citations | https://fortune.com/2026/01/21/neurips-ai-conferences-research-papers-hallucinations/ | HIGH |
| 15 | Springer — Adaptive Heterogeneous Multi-Agent Debate | https://link.springer.com/article/10.1007/s44443-025-00353-3 | HIGH |
| 16 | ByteByteGo — How OpenAI, Gemini, Claude Use Agents | https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use | MEDIUM |
| 17 | PromptLayer — How Deep Research Works | https://blog.promptlayer.com/how-deep-research-works/ | MEDIUM |
| 18 | Helicone — OpenAI vs Perplexity vs Gemini | https://www.helicone.ai/blog/openai-deep-research | MEDIUM |
| 19 | Francisco Moretti — Comparing Deep Research UIs | https://www.franciscomoretti.com/blog/comparing-deep-research-uis | MEDIUM |
| 20 | GPTZero — Perplexity Investigation | https://gptzero.me/news/gptzero-perplexity-investigation/ | MEDIUM |
| 21 | Sourcely — Automated Source Credibility Scoring | https://www.sourcely.net/resources/what-is-automated-source-credibility-scoring | MEDIUM |
| 22 | DataStudios — Perplexity Deep Research Overview | https://www.datastudios.org/post/perplexity-ai-deep-research-how-it-works-limitations-and-use-cases-for-professionals | MEDIUM |
| 23 | Dify — Deep Research Workflow Guide | https://dify.ai/blog/deep-research-workflow-in-dify-a-step-by-step-guide | MEDIUM |
| 24 | Substack — Perplexity Real Sources Fake Facts | https://andreafreund.substack.com/p/experimenting-with-perplexitys-deep | MEDIUM |
| 25 | OpenAI Community — Citation Bug Report | https://community.openai.com/t/deep-research-citation-links-to-unrelated-topics/1363823 | MEDIUM |
