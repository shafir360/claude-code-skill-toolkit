# Deep Research Report Template

Use this template for the final report output. All sections are required unless marked optional.

```markdown
# Deep Research Report: [Topic]

_Generated: [today's date] | Sources: [count] | Rounds: 2 | Agents: [count] | Overall Confidence: [High/Medium/Low]_

## Executive Summary

[2-3 paragraphs. Lead with the direct answer to the research question. State the overall confidence level and what it's based on. Highlight the most important findings and any significant contradictions or uncertainties. If human expert verification is recommended for any aspect, mention it here.]

## Key Findings

1. **[Finding title]** `[Confidence: HIGH]` — [One sentence detail with evidence] [Source](url)
2. **[Finding title]** `[Confidence: MEDIUM]` — [One sentence detail with evidence] [Source](url)
3. **[Finding title]** `[Confidence: LOW]` — [One sentence detail with evidence] [Source](url) ⚠️ _Single source — verify independently_
...

[12-20 numbered findings. Every finding MUST have:
- A confidence tag: `[Confidence: HIGH]`, `[Confidence: MEDIUM]`, or `[Confidence: LOW]`
- At least one citation URL that came from a research agent
- LOW confidence findings must be flagged with ⚠️ warning]

## Deep Dives

### [Theme 1 from Round 2]
[2-3 paragraphs of detailed analysis from targeted Round 2 research. Include citations.]

### [Theme 2 from Round 2]
[2-3 paragraphs of detailed analysis from targeted Round 2 research. Include citations.]

[Include 2-3 deep dive sections based on Round 2 targeted research. These go deeper than the key findings.]

## Contradictions & Debates

[This section is ALWAYS present, even if no contradictions were found.]

| Claim | Position A | Position B | Evidence Strength | Resolution |
|-------|-----------|-----------|-------------------|------------|
| [Area of disagreement] | [What side A says] [Source](url) | [What side B says] [Source](url) | [A: N sources, B: N sources] | [Reconciliation or "unresolved"] |

_If no contradictions: "No major contradictions were found across [N] sources consulted. The findings show broad agreement on [key points]."_

### Skeptic's Assessment

[Summary of what the dedicated skeptic agent found. Which claims survived scrutiny? Which were nuanced or weakened? Which were contradicted?]

## Knowledge Gaps & Uncertainties

- **[Gap 1]**: [What couldn't be determined and why] — _Suggested follow-up: [specific next step]_
- **[Gap 2]**: [What couldn't be determined and why] — _Suggested follow-up: [specific next step]_

[1-5 bullets. For each gap, explain why it couldn't be resolved and suggest how to investigate further.]

## ⚠️ Human Verification Recommended

[Optional — include only when findings touch medical, legal, financial, safety-critical, or highly technical domains]

The following findings should be independently verified by a domain expert:
- [Finding N]: [Why expert review is needed]

## Source Quality Assessment

| # | Source | URL | Credibility | Used By |
|---|--------|-----|-------------|---------|
| 1 | [Name] | [URL] | HIGH | Round 1 Agent 2, Round 2 Skeptic |
| 2 | [Name] | [URL] | MEDIUM | Round 1 Agent 1 |
...

[Top 20-30 most important sources. Include which round/agent used each source.]

## Methodology

- **Round 1**: [N] Sonnet agents conducted broad-sweep research across [N] themes
- **Gap Analysis**: Opus agent identified [N] gaps, [N] contradictions, and [N] claims requiring scrutiny
- **Round 2**: [N] Sonnet collector agents targeted specific gaps + 1 Opus skeptic agent challenged [N] claims
- **Synthesis**: Opus agent cross-referenced all findings and assigned per-finding confidence levels
- **Total sources consulted**: [N] unique sources across both rounds
- **Time taken**: ~[N] minutes
```
