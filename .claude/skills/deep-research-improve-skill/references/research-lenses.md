# Research Lenses for Deep Research Skill Improvement

Research lenses define the angles from which agents investigate a skill's domain for improvement. Each lens targets a different type of insight. Use 4-6 lenses for the two-round deep research process.

## Lenses for Skill Improvement (Round 1: Broad Sweep)

### 1. Best-in-Class Examples
**Purpose**: Find the best tools, skills, or implementations in the skill's domain to benchmark against.

Example sub-questions:
- What do the most popular/respected tools in this domain look like?
- What features or patterns distinguish excellent implementations from average ones?
- What design decisions made the best tools successful?

**How to use findings**: Identify specific features or patterns the current skill is missing. Tag improvements as `[Research: H/M/L]`.

### 2. Domain Evolution
**Purpose**: Check whether best practices in the skill's domain have changed since the skill was written.

Example sub-questions:
- Have there been new tools, standards, or approaches in this domain recently?
- Are any patterns used by the skill now considered outdated or deprecated?
- What emerging trends should the skill adapt to?

**How to use findings**: Identify outdated approaches in the current skill and suggest modern alternatives.

### 3. Common Quality Issues
**Purpose**: Find frequent weaknesses in similar tools or skills — systematic problems that affect many implementations.

Example sub-questions:
- What are the most common complaints about tools in this domain?
- What quality issues do code reviewers typically flag?
- What reliability or consistency problems appear?

**How to use findings**: Check the current skill for each identified weakness. Propose targeted fixes.

### 4. Edge Cases & Robustness
**Purpose**: Discover unusual inputs, environments, or scenarios the skill might not handle.

Example sub-questions:
- What unusual inputs could break this type of tool?
- What environment-specific issues exist (OS, permissions, encoding)?
- What happens under stress or with adversarial input?

**How to use findings**: Add missing edge case handling to the skill's instructions or Rules section.

### 5. Prior Art
**Purpose**: Discover existing tools that solve the same problem — sometimes the skill needs to change its fundamental approach.

Example sub-questions:
- What alternative approaches exist for this problem?
- Are there tools that take a fundamentally different approach and succeed?
- What can we learn from tools that failed in this space?

**How to use findings**: Consider whether the skill's core approach is optimal or needs rethinking.

---

## Lenses for Round 2: Targeted Deep Dives

Round 2 lenses are dynamically determined by the Opus gap analysis agent. Common patterns:

### Gap-Filling Collector Lenses
- **Thin Coverage Areas**: Topics where Round 1 found only 1 source — seek independent verification
- **Citation Chain Following**: From key Round 1 sources, find articles that cite or respond to them
- **Contradictory Evidence**: Seek evidence challenging prevailing improvement suggestions

### Skeptic Lens (Improvement-Specific)
- **Current-Approach Defense**: Search for evidence that the skill's CURRENT approach is actually optimal
- **Improvement Risk Assessment**: Look for cases where proposed improvements caused regressions elsewhere
- **Complexity-Benefit Analysis**: Challenge whether improvement adds enough value to justify added complexity
- **Outdated Suggestions**: Check if improvement suggestions are based on deprecated or disputed practices

The skeptic for skill improvement is especially important because **not all changes are improvements**. The best optimization is sometimes no change at all.

---

## Agent Prompt Template

When spawning research agents, each agent's prompt MUST include:

1. The skill's name, purpose, and domain
2. The specific lens assigned to this agent (from above)
3. 2-3 sub-questions from that lens
4. This instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs."

## Fallback

If fewer than 3 agents return usable results in Round 1, skip Round 2 and proceed with standard improvement analysis. Note that research was limited.
