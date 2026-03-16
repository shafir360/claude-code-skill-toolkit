# Exhaustive Research Report Template

Use this template for the final report output. All sections are required unless marked optional.

```markdown
# Exhaustive Research Report: [Topic]

_Generated: [date] | Depth: [Standard/Deep/Exhaustive] | Sources Screened: [N] | Sources Read: [N] | Rounds: 2 | Agents: [N] | Tree Levels: [N] | Time: ~[N] min | Overall Confidence: [High/Medium/Low]_

_Bootstrap: [Based on prior /deep-research report ([N] sources, [date]) | Started fresh]_

## Executive Summary

[3-5 paragraphs. Lead with the direct answer to the research question. State the overall confidence level and what it's based on. Highlight the most important findings, significant contradictions, and remaining uncertainties. Note the scale of research (X sources across Y agents). If human expert verification is recommended, mention it here.]

## Key Findings

1. **[Finding]** `[Confidence: HIGH]` `[Sources: N]` — [Detail] [Source1](url) [Source2](url)
2. **[Finding]** `[Confidence: MEDIUM]` `[Sources: N]` — [Detail] [Source](url)
3. **[Finding]** `[Confidence: LOW]` `[Sources: 1]` — [Detail] [Source](url) — Single source, verify independently

[20-40 numbered findings for Exhaustive depth; 12-20 for Standard. Each MUST have:
- Confidence tag: HIGH (3+ independent sources, no counter-evidence), MEDIUM (2 sources or counter-evidence exists), LOW (single source or successfully challenged)
- Source count
- At least one citation URL from a research agent
- LOW findings flagged with warning]

## Deep Dive Sections

### [Theme 1]
[3-5 paragraphs of detailed analysis with citations. Based on tree-merged findings.]

### [Theme 2]
[3-5 paragraphs]

[3-6 deep dive sections based on the most substantive themes from tree reduction]

## Contradictions & Debates

### Cross-Source Contradictions

| Claim | Position A | Position B | Evidence Strength | Circular? | Resolution |
|-------|-----------|-----------|-------------------|-----------|------------|
| [What's disputed] | [Source](url) says X | [Source](url) says Y | A: N sources, B: N sources | [Yes/No] | [Reconciliation or "unresolved"] |

_If no contradictions: "No major contradictions found across [N] sources. Findings show broad agreement."_

### Skeptic's Assessment

[Summary: which claims survived adversarial scrutiny, which were weakened, which were overturned. Include specific sources the skeptic used.]

### Circular Sourcing Detected

[Cases where apparent consensus traced back to a single original source. State: "N sources appeared to agree, but all cited [original source] — effective independent source count is 1."]

_If none: "No circular sourcing detected."_

## Confidence Assessment

### High-Confidence Findings (3+ independent, corroborated sources)
- [Bulleted list of finding numbers]

### Medium-Confidence Findings (2 sources, or counter-evidence exists)
- [Bulleted list]

### Low-Confidence Findings (single source, or successfully challenged)
- [Bulleted list with warnings]

## Knowledge Gaps & Uncertainties

- **[Gap]**: [Why it couldn't be resolved] — _Suggested follow-up: [action]_

[1-5 bullets]

## Human Verification Recommended

[Optional — include only for medical, legal, financial, safety-critical, or highly technical domains]

The following findings should be independently verified by a domain expert:
- Finding [N]: [Why expert review is needed]

## Source Quality Assessment

| # | Source | URL | Credibility | Pre-Screen Score | Tree Level | Round |
|---|--------|-----|-------------|------------------|------------|-------|
| 1 | [Name] | [URL] | HIGH | 48 | L0, L1 | R1 |
| 2 | [Name] | [URL] | MEDIUM | 32 | L0 | R2 |

[Top 40-60 sources for Exhaustive; 20-30 for Standard. Include pre-screen scores and which tree levels used them.]

## Methodology

- **Depth level**: [Standard/Deep/Exhaustive]
- **Bootstrap**: [/deep-research report with N sources | Fresh start]
- **Search queries**: [N] queries across [N] perspectives
- **Pre-screening**: [N] Haiku agents evaluated [N] candidates; [N] passed ([N]% pass rate)
- **Round 1**: [N] Sonnet reader agents processed [N] sources
- **Tree reduction**: [N] levels — Level 0 ([N] agents) → Level 1 ([N] agents) → [Root (1 Opus)]
- **Validation gates**: [N] gates, [N] reports flagged, [N] rejected
- **Gap Analysis**: Opus identified [N] gaps, [N] contradictions
- **Round 2**: [N] Sonnet collectors + [N] Opus skeptic(s)
- **Final synthesis**: Opus produced [N] key findings
- **Total unique sources**: [N] (after deduplication from [N] raw)
- **Total agents spawned**: [N] ([N] Haiku, [N] Sonnet, [N] Opus)
- **Total time**: ~[N] minutes
- **Partial completion**: [Yes/No — if Yes, list which phases completed]
```

## Report Save Structure

Save the report as 3 files at the user-confirmed location:

1. `report.md` — The full report above (main deliverable)
2. `sources.md` — Complete source list with all metadata (URL, credibility, pre-screen score, tree level, round, agent ID)
3. `methodology.md` — Detailed methodology (full agent counts, timing per phase, tree structure diagram, any failures/degradation)

If the pipeline failed partway, still save whatever was collected:
- Add `[PARTIAL]` to the report title
- In Methodology, list which phases completed and which were skipped
- In Executive Summary, note the limitation prominently
