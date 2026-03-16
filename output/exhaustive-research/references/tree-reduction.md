# Tree-Reduction Algorithm & Agent Prompt Templates

## Algorithm Overview

The parent orchestrator manages a tree of agents iteratively. No agent spawns sub-agents.

```
Sources (N)
    |
    v
[Level 0] N/6 Sonnet reader agents (each reads 5-7 sources) → N/6 mini-reports
    |
    v
[Validation Gate] Sonnet agent checks mini-reports for hallucination/missing citations
    |
    v
[Level 1] ceil(N/30) Sonnet merge agents (each merges 5 mini-reports) → intermediate reports
    |
    v
[Validation Gate] (Deep/Exhaustive only)
    |
    v
[Level 2] (Exhaustive only) ceil(remaining/5) Sonnet agents → condensed reports
    |
    v
[Root] 1 Opus agent merges all remaining reports → final synthesis
```

## Group Sizing

- **Universal batch size**: 5-7 items per agent (sources or reports)
- If fewer than 5 items remain at any level, merge them directly at the next level
- If 6-7 items remain, use a single agent (no need for tree level)
- **Hard cap**: Tree depth never exceeds 3 levels regardless of source count

## Anti-Recursion Instruction

Include this in every agent prompt (Haiku, Sonnet, and Opus):

```
You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly.
```

## Level 0: Reader Agent Prompt Template

```
Topic: [TOPIC-SLUG]. Research question: [1-SENTENCE VERSION]

For each source URL in your batch:
1. WebFetch the 2 highest-scored sources by pre-screening composite score (max 2 WebFetch calls). Use search snippets for the remaining 3-5. If a WebFetch fails, continue with snippet only. Prioritize by: (1) highest composite score, (2) highest credibility domain.
2. Extract ONLY: key claims, data points, statistics, expert quotes, methodology descriptions
3. Ignore: navigation, ads, boilerplate, author bios, related articles, comment sections
4. Keep extracted content to ~400 words per source maximum

After reading all sources, produce a MINI-REPORT with these exact sections:

TOPIC_RELEVANCE: [How relevant is this batch to the research question? HIGH/MEDIUM/LOW]

KEY_CLAIMS:
- [Claim 1 — one sentence with inline citation URL]
- [Claim 2 — one sentence with inline citation URL]
- [up to 8 claims total]

CONTRADICTIONS_WITHIN_BATCH:
- [Source A says X, Source B says Y — or "None found"]

SOURCE_QUALITY:
- [URL] — [HIGH/MEDIUM/LOW credibility] — [one-line justification]

METADATA:
- sources_read: [N]
- sources_via_snippet_only: [N]
- confidence: [HIGH/MEDIUM/LOW]

Keep your entire response under 800 words.

You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly.
```

## Level 1: Merge Agent Prompt Template

```
Topic: [TOPIC-SLUG]. You are merging mini-reports from parallel research agents.

You will receive 5 mini-reports, each covering a different batch of sources.

Your tasks:
1. DEDUPLICATE: Identify claims that appear in multiple reports (same finding, different sources)
2. CROSS-REFERENCE: Note where reports agree (convergent evidence) or disagree (contradictions)
3. SYNTHESIZE: Combine into a single intermediate report, preserving citation URLs
4. INJECT CONTEXT: Where a claim from Report A illuminates or contradicts a claim from Report B, note the connection

Produce an INTERMEDIATE_REPORT with these sections:

CONVERGENT_FINDINGS:
- [Finding] — supported by [N] independent sources: [URL1], [URL2], ...

CONTRADICTIONS:
- [Claim disputed] — Position A: [source] says X; Position B: [source] says Y

UNIQUE_FINDINGS:
- [Findings that appear in only one report — flag as single-source]

CIRCULAR_SOURCING_CHECK:
- [Any cases where multiple reports cite the same original source? If so, that's 1 source not N]

METADATA:
- total_unique_sources: [N]
- convergent_claims: [N]
- contradictions: [N]
- confidence: [HIGH/MEDIUM/LOW]

Keep your entire response under 1500 words.

You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly.
```

## Validation Gate Prompt Template

Validation gates check STRUCTURAL properties only. Semantic quality detection is only ~53% accurate and false positives cascade — so we check format, not meaning.

```
You are a structural quality gate checking research outputs before they feed into the next pipeline stage.

Review each mini-report/intermediate report for STRUCTURAL compliance only:
1. CITATION_CHECK: Does every KEY_CLAIMS bullet contain at least one URL? Count: [N]/[total] have URLs.
2. FORMAT_CHECK: Are all expected sections present? (KEY_CLAIMS, SOURCE_QUALITY, METADATA for mini-reports; CONVERGENT_FINDINGS, CONTRADICTIONS, METADATA for intermediate reports)
3. LENGTH_CHECK: Is the response between 200-800 words (mini-report) or 400-1500 words (intermediate)?
4. METADATA_CHECK: Is the METADATA block present with sources_read, confidence fields?

Do NOT judge whether claims are true, whether confidence ratings are "correct," or whether the content seems "suspicious." Structural checks only.

For each report, return:
- PASS: All structural checks pass
- FLAG: 1-2 structural issues but report is usable (list which checks failed)
- REJECT: Missing >50% of expected sections, OR zero citation URLs, OR response under 100 words

Keep your response under 200 words per report reviewed.

You are a leaf-node agent. Do NOT use Agent or Skill tools — return your findings directly.
```

## Token Budget Per Agent

| Agent Type | Max Input | Max Output | Notes |
|---|---|---|---|
| Haiku screener | ~8K tokens | ~3K tokens | 40-50 snippets x ~150 tokens (condensed rubric) |
| Sonnet reader (L0) | ~12K tokens | ~1.2K tokens | 5-7 sources, 2 WebFetch + snippets |
| Sonnet merge (L1) | ~8K tokens | ~2.5K tokens | 5 mini-reports x ~1.5K each |
| Sonnet merge (L2) | ~15K tokens | ~3K tokens | 5 intermediate reports x ~3K |
| Sonnet validator | ~10K tokens | ~2K tokens | Checking 3-5 reports |
| Opus gap analysis | ~20K tokens | ~4K tokens | All intermediate reports |
| Opus skeptic | ~15K tokens | ~3K tokens | Claims + context |
| Opus synthesis | ~25K tokens | ~8K tokens | Everything merged |
