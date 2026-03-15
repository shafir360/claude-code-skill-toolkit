# Example Skills — User's Preferred Patterns

These examples show the style and conventions to follow when generating new skills.

## Example 1: Research Skill (Complex, multi-agent)

```yaml
---
name: research
description: Conduct thorough multi-source research on any topic. Spawns parallel research agents, synthesizes findings, and produces a comprehensive cited report. Use when asked to research, investigate, or deeply analyze a topic.
argument-hint: <topic or question>
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch
---
```

**Why this description works:**
- Third person ("Conduct..." / "Spawns...")
- What: "Spawns parallel research agents, synthesizes findings, produces cited report"
- When: "Use when asked to research, investigate, or deeply analyze"
- Trigger keywords: research, investigate, deeply analyze
- 218 chars — well within 1024 limit

**Body pattern (phases):**
```markdown
# Deep Research: $ARGUMENTS

[1-sentence role statement with model strategy note]

## Phase 1: Scope
[Brief planning step — 3-5 themes, 30 seconds]

## Phase 2: Parallel Investigation
[Core work — spawns agents, includes verbatim instruction block for agents]

## Phase 3: Synthesize & Report
[Merge findings → exact output template with markdown structure]

## Phase 3b: Self-Check
[Quality gate — verify citations, remove unsupported claims]

## Phase 4: Output
[Ask user preference (save vs. chat)]

## Quality Standards
[5 specific rules — citations, sources, uncertainty, dates, URLs]
```

**Key patterns demonstrated:**
- H1 title: `# Action: $ARGUMENTS`
- Phases numbered sequentially
- Self-check phase before output (quality gate)
- Exact output template with markdown code block
- Rules section at end with specific, actionable constraints

---

## Example 2: Summarize Skill (Simple, single-step)

```yaml
---
name: summarize
description: Quick summary of a topic from web sources. Faster and lighter than /research - good for getting oriented on a topic or getting a brief overview. Use when asked for a brief summary, quick overview, or to get up to speed on something.
argument-hint: <topic>
allowed-tools: WebSearch, WebFetch, Read
---
```

**Why this description works:**
- Differentiates from sibling skill (/research) — "Faster and lighter"
- Multiple trigger phrases: "brief summary", "quick overview", "get up to speed"
- Clear positioning: when to use THIS skill vs alternatives

**Body pattern (numbered steps):**
```markdown
# Quick Summary: $ARGUMENTS

[1-sentence intro with positioning]

## Process

### 1. Search (3-5 queries)
[Specific search instructions with constraints]

### 2. Fetch Top Sources (2-3 pages)
[Fetch instructions with limits]

### 3. Summarize
[Output requirements: 300-500 words, inline citations, accessible language]

### 4. Learn More
[3-5 links for deeper reading]

## Output Format
[Exact template]

## Rules
[5 concise rules — keep it concise, cite claims, handle broad topics, no file save, suggest /research]
```

**Key patterns demonstrated:**
- Simpler numbered steps instead of phases (appropriate for lighter tasks)
- Word count constraints (300-500 words)
- Cross-references to other skills ("suggest /research")
- Minimal tool set (only 3 tools — simplest that works)

---

## Common Conventions

| Element | Convention |
|---------|-----------|
| Title | `# [Action Verb]: $ARGUMENTS` |
| Intro | 1-2 sentences, what this skill does |
| Steps/Phases | Numbered, imperative voice |
| Output | Exact markdown template in fenced code block |
| Rules | 5-8 specific constraints at the end |
| Tools | Only list tools actually needed in `allowed-tools` |
| Description | Third person, what + when, trigger keywords |
