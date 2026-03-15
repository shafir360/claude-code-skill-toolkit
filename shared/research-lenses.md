# Research Lenses for Skill Generation & Improvement

Research lenses define the angles from which Sonnet agents investigate a skill's domain. Each lens targets a different type of insight. Use 3-5 lenses per research phase — pick the ones most relevant to the skill's domain.

## Lenses for Skill Generation

Use these when researching BEFORE generating a new skill.

### 1. Prior Art
**Purpose**: Discover existing tools, scripts, CLI utilities, or Claude Code skills that solve the same or similar problem.

Example sub-questions:
- What tools already exist for this task? What do they do well? What do they do poorly?
- Are there Claude Code skills, VS Code extensions, or CLI tools that overlap?
- What patterns do successful tools in this space share?

**How to use findings**: Inform the skill's approach — borrow proven patterns, avoid known failures, differentiate from existing tools.

### 2. Domain Patterns
**Purpose**: Identify established conventions, standards, and best practices in the skill's target domain.

Example sub-questions:
- What are the standard workflows practitioners follow for this task?
- Are there industry standards, specs, or conventions that apply?
- What input/output formats are expected?

**How to use findings**: Shape the skill's phase structure and output format to match domain conventions.

### 3. Pitfalls & Failure Modes
**Purpose**: Find common mistakes, edge cases, and failure modes when building or using tools in this domain.

Example sub-questions:
- What goes wrong most often when people attempt this task?
- What edge cases cause tools in this space to break?
- What are the security, performance, or correctness risks?

**How to use findings**: Add specific items to the skill's Rules section. Design phases to guard against known failure modes.

### 4. Input/Output Patterns
**Purpose**: Understand the data formats, structures, and variations the skill will encounter.

Example sub-questions:
- What input formats do users typically provide?
- What output format do users expect?
- What are the boundary cases (empty input, huge files, special characters)?

**How to use findings**: Define the skill's argument-hint, input validation, and output template.

### 5. User Workflow Context
**Purpose**: Understand how practitioners currently perform this task manually — what's tedious, error-prone, or time-consuming.

Example sub-questions:
- What steps do people follow when doing this manually today?
- Which steps are most error-prone or tedious?
- What would make this task 10x easier?

**How to use findings**: Prioritize automating the most painful steps. Design the skill to fit naturally into existing workflows.

---

## Lenses for Skill Improvement

Use these when researching BEFORE improving an existing skill.

### 1. Best-in-Class Examples
**Purpose**: Find the best tools, skills, or implementations in the skill's domain to benchmark against.

Example sub-questions:
- What do the most popular/respected tools in this domain look like?
- What features or patterns distinguish excellent implementations from average ones?
- What design decisions made the best tools successful?

**How to use findings**: Identify specific features or patterns the current skill is missing. Tag improvements as `[Research]`.

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

---

## Agent Prompt Template

When spawning research agents, each agent's prompt MUST include:

1. The overall research topic (what skill is being generated/improved)
2. The specific lens assigned to this agent (from above)
3. 2-3 sub-questions from that lens
4. This instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs."

## Fallback

If fewer than 2 agents return usable results, skip the synthesis step and proceed directly to generation/improvement using only existing knowledge. Note in the output that research was limited.
