# Example Skills Reference

These examples demonstrate preferred style and conventions for generated skills.

## Example 1: Deep Research Skill (Complex, Multi-Agent, Two-Round)

```yaml
---
name: deep-research
description: 'Conducts exhaustive, multi-layered research using two rounds of parallel investigation with tiered model strategy. Round 1 spawns broad-sweep Sonnet agents across 5-7 themes. An Opus gap-analysis identifies weak spots, then Round 2 launches targeted collectors plus a dedicated Opus skeptic agent that challenges majority findings. Produces comprehensive cited reports with per-finding confidence levels, contradiction analysis, and source credibility assessment. Use when the user says "deep research", "exhaustive research", "thorough investigation", "deep dive into", "comprehensive analysis", or needs research that goes beyond a quick overview.'
argument-hint: <topic or question>
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Deep Research: $ARGUMENTS

You are conducting an exhaustive, multi-layered research investigation...

## Phase 1: Scope & Plan (~1 minute)
[Decompose topic into 4-6 themes, present research plan]

## Phase 2: Broad Sweep — Round 1 (~3 minutes)
[Spawn Sonnet agents in parallel, one per theme]

## Phase 3: Gap Analysis & Round 2 Planning (~1 minute)
[Opus agent analyzes gaps, plans Round 2]

## Phase 4: Targeted Deep Dives — Round 2 (~3 minutes)
[Sonnet collectors + Opus skeptic in parallel]

## Phase 5: Cross-Reference & Synthesize (~2 minutes)
[Opus agent merges all findings, assigns confidence]

## Phase 6: Report Generation (~1 minute)
[Generate structured report]

## Phase 7: Self-Check & Output (~30 seconds)
[Citation audit, quality review, present]

## Rules
1. NEVER generate citation URLs from memory
2. Every Round 2 agent MUST seek contradictory evidence
3. Opus skeptic MUST challenge strongest claims
4. Each agent has distinct, non-overlapping focus
5. Use tiered models: Sonnet for data, Opus for analysis
```

**Key patterns**: Two-round architecture, tiered model strategy, dedicated skeptic agent, per-finding confidence levels, mandatory contradiction section.

## Example 2: Research Skill (Standard, Multi-Agent, Single-Round)

```yaml
---
name: research
description: 'Conduct thorough multi-source research on any topic. Spawns parallel research agents, synthesizes findings, and produces a comprehensive cited report. Use when the user says "research this", "look into", "find out about", "what do we know about", "dig into", or asks to investigate or deeply analyze a topic.'
argument-hint: <topic or question>
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Deep Research: $ARGUMENTS

## Phase 1: Scope
[3-5 themes]

## Phase 2: Parallel Investigation
[Sonnet agents, single round]

## Phase 3: Synthesize & Report
[Merge findings, produce report]

## Phase 4: Self-Check
[Quality review]

## Rules
[5 specific constraints]
```

**Key patterns**: Single-round, all-Sonnet agents, simpler report format.

## Example 3: Summarize Skill (Simple, Single-Step)

```yaml
---
name: summarize
description: 'Quick summary of a topic from web sources. Faster and lighter than /research. Use when asked for a brief summary, quick overview, or to get up to speed on something.'
argument-hint: <topic>
allowed-tools: WebSearch, WebFetch, Read
---

# Quick Summary: $ARGUMENTS

1. Search for the topic
2. Read top 3-5 results
3. Synthesize into 300-500 word summary
4. Include 3-5 source URLs
5. Present to user
```

**Key patterns**: Numbered steps instead of phases, word count constraints, minimal tool set.

## Common Conventions

| Element | Convention |
|---------|-----------|
| Title | `# [Action Verb]: $ARGUMENTS` |
| Intro | 1-2 sentences, what it does |
| Steps | Numbered phases, imperative voice |
| Output | Exact markdown template in code block |
| Rules | 5-10 specific constraints at end |
| Tools | Only list actually-used tools |
| Description | Third person, what + when + trigger phrases |
