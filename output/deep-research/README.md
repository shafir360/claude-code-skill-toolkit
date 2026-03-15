# deep-research

> Exhaustive, two-round research on any topic — with adversarial review, per-finding confidence levels, and source credibility assessment.

Claude Code's built-in web search gives you quick answers. `/research` gives you a synthesized report from multiple sources. `/deep-research` goes further: it runs two rounds of parallel investigation, uses an Opus-powered skeptic agent to challenge the strongest findings, and produces a comprehensive report where every claim has a confidence level and citation.

## Why Use This

- **Two research rounds** — Broad sweep first, then targeted deep dives on gaps and weak spots
- **Adversarial review** — A dedicated Opus skeptic agent actively tries to disprove the strongest findings, so you know which claims actually hold up
- **Per-finding confidence** — Every finding is tagged HIGH/MEDIUM/LOW based on independent source count and counter-evidence
- **Contradiction analysis** — Always included, even if no contradictions are found — so you know the research checked

## Quick Start

```
/deep-research What are the security implications of WebAssembly in production?
```

## Usage

```
/deep-research <topic or question>
```

### Examples

- `/deep-research How do distributed consensus algorithms compare for financial systems?`
- `/deep-research State of AI code generation tools in 2026 — capabilities, limitations, and enterprise adoption`
- `/deep-research What evidence exists for or against microservices at small team scale?`
- `/deep-research Compare React Server Components vs traditional SSR — performance, DX, and ecosystem maturity`

## How It Works

The skill runs a 7-phase pipeline in ~10-12 minutes:

| Phase | Time | Model | What Happens |
|-------|------|-------|-------------|
| 1. Scope & Plan | ~1 min | Parent | Decomposes topic into 4-6 themes, presents research plan for your review |
| 2. Broad Sweep (Round 1) | ~3 min | Sonnet | 4-6 parallel agents collect data using structured output (FINDINGS/SOURCES/SURPRISES) |
| 3. Gap Analysis | ~1 min | **Opus** | Identifies gaps, contradictions, single-source claims, and 2-3 claims to challenge |
| 4. Deep Dives (Round 2) | ~3 min | Sonnet + **Opus** | 3-4 collectors target gaps (WebFetch 3) + 1 Opus skeptic challenges with cited evidence |
| 5. Cross-Reference | ~2 min | **Opus** | Merges all findings, assigns per-finding confidence, resolves contradictions |
| 5b. Refinement | ~1 min | Sonnet | Self-critique pass; spawns 1-2 gap-fill agents if needed (skipped if synthesis is clean) |
| 6. Report | ~1 min | Parent | Generates full report from template |
| 7. Self-Check | ~30s | Parent | Audits citations, flags single-source claims, verifies completeness |

## Example Output

The report follows this structure (abbreviated):

```markdown
# Deep Research Report: [Topic]
_Generated: 2026-03-15 | Sources: 24 | Rounds: 2 | Agents: 9 | Overall Confidence: Medium_

## Executive Summary
[2-3 paragraphs with direct answer and confidence assessment]

## Key Findings
1. **[Finding]** `[Confidence: HIGH]` — [Detail with evidence] [Source](url)
2. **[Finding]** `[Confidence: MEDIUM]` — [Detail] [Source](url)
3. **[Finding]** `[Confidence: LOW]` — [Detail] [Source](url) ⚠️ Single source

## Deep Dives
### [Theme from Round 2]
[Detailed analysis from targeted research]

## Contradictions & Debates
| Claim | Position A | Position B | Resolution |
[Always present — even if "No major contradictions found"]

### Skeptic's Assessment
[Which claims survived scrutiny, which were nuanced]

## Knowledge Gaps
- [What couldn't be determined and why]

## Source Quality Assessment
| # | Source | URL | Credibility | Used By |
[Top 20-30 sources with ratings]
```

## When to Use This vs Alternatives

| Need | Use | Time |
|------|-----|------|
| Quick answer to a question | Regular Claude Code chat | ~30s |
| Brief overview of a topic | `/summarize` | ~2 min |
| Multi-source cited report | `/research` | ~5 min |
| **Exhaustive investigation with adversarial review** | **`/deep-research`** | **~12 min** |

Use `/deep-research` when you need to make a decision based on the research, when the topic is controversial or has conflicting information, or when you need confidence levels on each finding.

## Tools Used

| Tool | Purpose |
|------|---------|
| WebSearch | Search the web across multiple queries per theme |
| WebFetch | Fetch full page content for detailed reading (max 2 per agent) |
| Read | Load reference files (credibility framework, report template) |
| Write | Save the final research report |
| Grep | Search within fetched content |
| Glob | Find relevant local files |

## Safety: Anti-Recursion Guards

All sub-agents are spawned as `deep-researcher` type (never `general-purpose`), which restricts their tool access to WebSearch, WebFetch, Read, Write, Grep, and Glob. This structurally prevents agents from spawning further sub-agents or invoking skills. Every agent prompt also includes an explicit anti-recursion instruction as defense-in-depth.

## Limitations & Edge Cases

- **Time cost**: ~10-12 minutes is significantly slower than a quick web search. Use `/research` or `/summarize` for simple questions.
- **Internet required**: Both WebSearch and WebFetch need internet access.
- **Citation quality**: While the skill mitigates AI citation failure (60%+ failure rate in studies), some citation mismatches may still occur. LOW-confidence findings are flagged.
- **Recency**: Web search results may not include the very latest information on fast-moving topics.
- **Depth vs breadth**: The 4-6 theme decomposition favors breadth. For narrow, deeply technical questions, a manual deep dive may be more effective.

## Sources & References

The design of this skill is informed by research on how leading AI research systems work:

- [Deep Research: A Survey of Autonomous Research Agents (arXiv)](https://arxiv.org/pdf/2508.12752) — Survey of architectures used by OpenAI, Gemini, and Perplexity deep research systems
- [FlowSearch: Dynamic Structured Knowledge Flow (arXiv)](https://arxiv.org/html/2510.08521v1) — Progressive knowledge accumulation across research rounds
- [DR-Arena: Automated Evaluation of Deep Research Agents (arXiv)](https://arxiv.org/html/2601.10504v1) — Quality gate framework using examiner components
- [Heterogeneous Multi-Agent Debate (Springer)](https://link.springer.com/article/10.1007/s44443-025-00353-3) — ~91% vs ~82% accuracy with diverse model tiers
- [Minimizing Hallucinations via Adversarial Debate (MDPI)](https://www.mdpi.com/2076-3417/15/7/3676) — Cross-verification through voting mechanisms
- [Can LLM Agents Really Debate? (arXiv)](https://arxiv.org/html/2511.07784v1) — "Minority correction asymmetry" — why skeptic must challenge majority
- [D3: Debate, Deliberate, Decide (arXiv)](https://arxiv.org/abs/2410.04663) — Role-specialized adversarial evaluation with confidence-weighted verdicts
- [GPT-Researcher Parallel Features (Dify)](https://dify.ai/blog/enhancing-gpt-researcher-with-parallel-and-advanced-iterative-features) — Iterative research with reflection loops
- [Automated Source Credibility Scoring (Sourcely)](https://www.sourcely.net/resources/what-is-automated-source-credibility-scoring) — Multi-signal credibility assessment framework

## Installation

```bash
cp -r output/deep-research ~/.claude/skills/deep-research
```

Or use the toolkit:

```
/implement-skill deep-research
```

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Internet access (WebSearch and WebFetch tools)

---

_Generated by [Claude Code Skill Toolkit](https://github.com/shafir360/claude-code-skill-toolkit)_
