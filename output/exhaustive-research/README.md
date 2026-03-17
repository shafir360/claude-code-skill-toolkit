# exhaustive-research

> Massively scaled multi-agent research that processes hundreds of sources through hierarchical tree-reduction with 3-tier model strategy.

When `/deep-research` isn't enough, `/exhaustive-research` scales up by 10-100x. It pre-screens hundreds of candidate sources using cheap Haiku models, deeply reads the top-scoring ones with Sonnet agents, merges findings through a tree of progressively higher-level summaries, and synthesizes everything with Opus. The result is a comprehensive, cited report with per-finding confidence levels and contradiction analysis.

## Why Use This

- **Scale**: Process 30-400 sources (vs ~20-30 in /deep-research) with configurable depth levels
- **Cost-efficient**: 3-tier model strategy puts 70-80% of API calls on Haiku, saving 15-50x vs using Opus for everything
- **No overload**: Hierarchical tree-reduction means no single agent ever sees more than 5-7 sources
- **Quality-gated**: Structural validation gates between every tree level prevent error cascading — the #1 failure mode in multi-agent systems
- **Safe**: Multi-layer anti-recursion defense (expanded CRITICAL blocks on every agent prompt, explicit per-tool restrictions); no agent can spawn sub-agents; every phase has hard timeouts
- **Resilient**: Phase-boundary checkpointing with wave-level recovery and per-agent retry tracking; skip-and-note over retry storms; early termination on bad query sets
- **Transparent**: Phase Recap blocks show progress after every phase — agents completed, sources processed, elapsed time, next steps
- **Context-aware**: Save-and-release streaming prevents context window overflow (~1M token limit) during Exhaustive runs; load-on-demand pattern keeps orchestrator under 700K tokens
- **Wave-batched**: Large agent spawns are broken into bounded waves (max 10) so one silent agent never blocks the entire phase

## Quick Start

```
/exhaustive-research climate change impact on agriculture
```

## Usage

```
/exhaustive-research <topic or question> [depth: standard|deep|exhaustive]
```

### Examples

- `/exhaustive-research deep: quantum computing applications in drug discovery`
- `/exhaustive-research exhaustive: comprehensive analysis of remote work productivity research`
- `/exhaustive-research standard: current state of carbon capture technology`

### With Deep-Research Bootstrap

For best results, run `/deep-research` first, then feed its output into `/exhaustive-research`:

```
/deep-research quantum computing in drug discovery
# ... wait for report ...
/exhaustive-research deep: quantum computing in drug discovery
# When prompted, paste or point to the deep-research report
```

## How It Works

| Phase | Time (Standard) | Time (Exhaustive) | What Happens |
|-------|----------------|-------------------|-------------|
| 0. Bootstrap | ~1 min | ~1 min | Ingest optional /deep-research output as "Round 0" |
| 1. Clarify | ~2 min | ~5 min | Confirm depth, save location, research objective |
| 2. Search | ~3 min | ~10 min | Sonnet agents generate diverse queries; execute searches |
| 3. Screen | ~5 min | ~20 min | Haiku agents score snippets for relevance/credibility |
| 4. Read | ~10 min | ~40 min | Sonnet agents deeply read top-scoring sources (5 per agent) |
| 5. Merge | ~5 min | ~20 min | Tree reduction: Level 0 → Level 1 → (Level 2) → Root |
| 6. Gap Analysis | ~3 min | ~10 min | Sonnet identifies contradictions, thin coverage, circular sourcing |
| 7. Round 2 | ~10 min | ~40 min | Sonnet collectors fill gaps; Opus skeptic challenges claims |
| 8. Synthesize | ~5 min | ~15 min | Opus merges everything into final synthesis |
| 9. Report | ~5 min | ~15 min | Generate report, self-check, save to confirmed location |

## Example Output

```markdown
# Exhaustive Research Report: Impact of Remote Work on Productivity

_Generated: 2026-03-16 | Depth: Deep | Sources Screened: 247 | Sources Read: 89 |
Rounds: 2 | Agents: 34 | Tree Levels: 2 | Time: ~95 min | Overall Confidence: Medium_

## Executive Summary

Remote work productivity effects are nuanced and context-dependent...

## Key Findings

1. **Knowledge workers show 13-24% productivity gains** `[Confidence: HIGH]` `[Sources: 7]`
   — Meta-analysis of 38 studies... [Source1](url) [Source2](url)

2. **Collaborative tasks show 5-15% decline** `[Confidence: MEDIUM]` `[Sources: 3]`
   — Microsoft Research and Nature study... [Source](url)

3. **Junior employees disproportionately affected** `[Confidence: LOW]` `[Sources: 1]`
   — Single McKinsey survey... [Source](url) — Single source, verify independently
...
```

## Deep Research Insights

These findings from the Enhanced Design Brief directly shaped the skill's architecture:

- **Error cascading is the #1 failure mode** in multi-agent systems — unstructured topologies amplify errors 17.2x `[Confidence: HIGH]` [Source](https://galileo.ai/blog/multi-agent-llm-systems-fail)
- **Hierarchical merging produces fewer omissions but more inconsistency** than flat summarization `[Confidence: HIGH]` [Source](https://arxiv.org/abs/2310.00785)
- **LLMs achieve ~0.95 sensitivity** for title/abstract screening, outperforming traditional ML tools `[Confidence: HIGH]` [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC12657656/)
- **Multi-agent debate does NOT beat simpler baselines** and introduces sycophancy risk `[Confidence: HIGH]` [Source](https://arxiv.org/abs/2502.08788)
- **LLMs are poor self-assessors** (<30% calibration accuracy, anti-Bayesian behavior) — source-agreement counting is more reliable `[Confidence: HIGH]` [Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC12249208/)
- **Difficulty-aware model routing** saves 36% cost while improving accuracy 11.21% `[Confidence: HIGH]` [Source](https://arxiv.org/html/2509.11079v1)
- **STORM's persona-based query diversification** is the best-validated approach for broad coverage `[Confidence: MEDIUM]` [Source](https://arxiv.org/abs/2402.14207)
- **Validation gates between agent layers** prevent the "silent downstream contamination" failure mode `[Confidence: HIGH]` [Source](https://futureagi.substack.com/p/how-tool-chaining-fails-in-production)

## When to Use This vs Alternatives

| Need | Use This | Use Instead |
|------|----------|-------------|
| Quick overview of a topic | | `/summarize` (~2 min) |
| Solid multi-source research | | `/research` (~5 min) |
| Thorough 2-round investigation | | `/deep-research` (~15 min) |
| **Hundreds of sources, comprehensive coverage** | **Yes** | |
| **Building on prior /deep-research** | **Yes** | |
| **Hours-long exhaustive investigation** | **Yes** | |
| Simple factual question | | Just ask Claude directly |

## Tools Used

| Tool | Purpose |
|------|---------|
| WebSearch | Execute search queries across all research themes |
| WebFetch | Read full source pages for extraction |
| Read | Load reference files, bootstrap reports |
| Write | Save final report, sources, methodology |
| Agent (deep-researcher) | All sub-agents for screening, reading, merging, analysis |

## Resilience Features

| Feature | What It Does | Research Backing |
|---------|-------------|-----------------|
| Phase checkpointing | JSON checkpoint after every phase; resume on failure | LangGraph superstep model, Ray distributed checkpointing |
| Implicit file checkpoints | Each agent's output file = sub-phase recovery point | LangGraph fan-out pattern |
| Structural-only validation | Format/citation/length checks, not semantic judgment | MAST: semantic detection only 53% accurate |
| Skip-and-note policy | Max 1 retry (timeout only); never retry bad output | Portkey: naive retries caused $10+/day cost explosions |
| Early termination | Pause on <20% screen pass rate or >30% agent failure | ReliabilityBench: small failures compound quickly |
| Phase Recaps | Text progress block after every phase | Nielsen Norman: any feedback > no feedback |
| Wave-batching | Max 10 agents per wave; timed-out agents skipped immediately | Prevents single silent agent from blocking entire phase |
| Context streaming | Save-and-release pattern; load-on-demand from disk | Prevents 1M token context overflow on Exhaustive runs |
| Per-agent retry tracking | Checkpoint tracks retries per agent; max 1 retry ever | Prevents infinite re-run loops on resume |

## Limitations & Edge Cases

- **Time cost**: Standard takes ~1 hour; Exhaustive can take ~4 hours. Use `/deep-research` for faster results.
- **Token cost**: Exhaustive depth may consume 4-8M tokens across all agents. Standard is 500K-1M.
- **Haiku screening accuracy**: ~95% sensitivity, ~5% false positive rate. Some relevant sources will be missed; some irrelevant ones will be read.
- **Information loss in tree reduction**: Each level retains ~50-80% of detail. 3-level trees retain 12-51% of original detail.
- **No real-time sources**: Cannot access paywalled content, databases, or real-time data feeds.
- **Domain limitations**: Best for topics with substantial public web coverage. Niche domains with few online sources may underperform.
- **LLM query expansion failure**: On ambiguous or highly specialized topics, query diversification may narrow rather than broaden coverage.

## Sources & References

- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Production patterns for Opus+Sonnet orchestration
- [NexusSum (ACL 2025)](https://arxiv.org/abs/2505.24575) — Hierarchical multi-agent summarization achieving 30% BERTScore gain
- [BooookScore (ICLR 2024)](https://arxiv.org/abs/2310.00785) — Hierarchical vs incremental summarization tradeoffs
- [STORM (Stanford NAACL 2024)](https://arxiv.org/abs/2402.14207) — Persona-based query diversification
- [From Spark to Fire (2026)](https://arxiv.org/abs/2603.04474v1) — Error cascading in multi-agent collaboration
- [MAST: Why Multi-Agent Systems Fail](https://arxiv.org/abs/2503.13657) — Failure taxonomy, 41-86.7% failure rates
- [Stop Overvaluing Multi-Agent Debate (2025)](https://arxiv.org/abs/2502.08788) — Debate doesn't beat simpler baselines
- [Galileo: Multi-Agent Failure Analysis](https://galileo.ai/blog/multi-agent-llm-systems-fail) — 17.2x error amplification
- [LLM Calibration in Biomedical NLP](https://pmc.ncbi.nlm.nih.gov/articles/PMC12249208/) — <30% calibration accuracy
- [JudgeRank: Decomposed Relevance Scoring](https://arxiv.org/html/2412.05579v2) — 3-step scoring outperforms flat
- [Chain of Agents (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/ee71a4b14ec26710b39ee6be113d7750-Paper-Conference.pdf) — Sequential vs parallel tree tradeoffs
- [RA-RAG: Source Reliability Weighting](https://arxiv.org/abs/2410.22954) — Weighted aggregation for confidence

## Installation

```bash
cp -r output/exhaustive-research ~/.claude/skills/exhaustive-research
```

Or: `/implement-skill exhaustive-research`

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- WebSearch and WebFetch tools enabled
- Sufficient API usage budget for the selected depth level

---

_Generated by [Claude Code Skill Toolkit](https://github.com/shafir360/claude-code-skill-toolkit) (deep-research mode)_
