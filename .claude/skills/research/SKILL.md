---
name: research
description: Conduct thorough multi-source research on any topic. Spawns parallel research agents, synthesizes findings, and produces a comprehensive cited report. Use when the user says "research this", "look into", "find out about", "what do we know about", "dig into", or asks to investigate or deeply analyze a topic.
argument-hint: <topic or question>
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
---

# Deep Research: $ARGUMENTS

You are conducting a comprehensive research investigation. This skill uses **Sonnet for fast parallel research agents** (search, fetch, extract) and relies on the **parent model (Opus) for scoping, synthesis, and quality review**.

**Target: complete the entire pipeline in under 5 minutes.**

**Time budget**: Phase 1 ~30s | Phase 2 ~3 min | Phase 3 ~1.5 min

Rate source credibility using the framework in [references/source-evaluation.md](references/source-evaluation.md).

## Phase 1: Scope (~30 seconds)

Identify **3-5** distinct themes or angles to investigate. Keep scoping brief — spend under 30 seconds. List your themes, then immediately proceed to Phase 2.

## Phase 2: Parallel Investigation (~3 minutes)

Spawn one **deep-researcher** agent for EACH theme. Launch ALL agents in parallel in a single message. More agents = more coverage, and parallelism keeps it fast.

**Critical rules for EVERY agent:**
- Set `model: "sonnet"` on every agent (Sonnet handles search/fetch; Opus handles synthesis)
- Give each agent a slightly different research lens to maximize coverage diversity. For example:
  - Agent 1: Technical/factual deep-dive
  - Agent 2: Skeptic/critic angle — look for problems, limitations, criticisms
  - Agent 3: Industry/commercial perspective — who's using it, market trends
  - Agent 4+: Additional angles as needed (academic, historical, future outlook)
- Each agent's prompt MUST include this instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs."

Each agent's prompt must also include:
- The overall research topic
- Its specific assigned theme and research lens
- 2-3 sub-questions for that theme

Wait for all agents to return before proceeding.

**If an agent fails or returns empty**: Skip it and proceed with the remaining agents' findings. If fewer than 2 agents return usable results, note the coverage gap in the Knowledge Gaps section and consider launching 1-2 replacement agents with adjusted search terms.

## Phase 3: Synthesize & Report (~1.5 minutes)

Merge findings from all agents directly into the final report. Do NOT write a separate synthesis — go straight to the report. Combine overlapping findings, note agreements and conflicts, and produce:

**CRITICAL: Only use URLs that agents explicitly returned in their findings. Never generate a citation URL from memory or prior knowledge. If you cannot trace a claim to an agent-provided URL, do not include it.**

```markdown
# Research Report: [Topic]
_Generated: [today's date] | Sources: [count] | Confidence: [High/Medium/Low]_

## Executive Summary
[2-3 paragraphs: the answer to the research question, key takeaways, and overall confidence level]

## Key Findings
1. **[Finding]** - [One sentence detail] [Source](url)
2. ...
[8-12 numbered findings. Every finding must have a citation.]

## Conflicting Information
| Claim | Position A | Position B | Sources |
[Only include if contradictions were found across agents. Otherwise omit this section.]

## Knowledge Gaps
- [1-2 bullets: what couldn't be determined and why]

## Sources
| # | Source | URL | Credibility |
[Top 15-20 most important sources only. Do not list every source from every agent.]
```

## Phase 3b: Self-Check

Quick quality review before presenting to the user (this is fast — just scan, don't regenerate):
1. Does every finding have a citation URL that came from an agent? Remove any that don't.
2. Is any claim supported by only one LOW-credibility source? Mark it as "unverified" or remove it.
3. Are there any obvious contradictions between findings that aren't noted in the Conflicting Information section? Add them.

## Phase 4: Output

Ask the user: "Would you like me to save this report to a file or keep it in chat?"

## Quality Standards
- Every factual claim must have a citation
- Minimum 5 distinct sources
- Flag uncertainty explicitly
- Include publication dates where known
- Never fabricate or guess URLs — only use what agents returned
