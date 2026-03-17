---
name: research-improve-skill
description: Research a skill's domain and best practices, then improve it with research-backed insights. Spawns parallel Sonnet agents to find best-in-class examples and domain-specific gaps before suggesting improvements. Use when wanting research-backed improvement, or when saying "research and improve", "deep improve", "improve with research", or "research-powered improvement".
argument-hint: <path/to/skill-directory>
allowed-tools:
  - Read
  - Write
  - Bash(python *)
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Research & Improve Skill: $ARGUMENTS

You are analyzing an existing Claude Code skill and improving it with research-backed insights. Before suggesting changes, you investigate the skill's domain to find best-in-class examples and identify domain-specific gaps. Choose this over `/improve-skill` when the domain is unfamiliar or when quality matters more than speed.

**Time budget**: Phase 1 ~30s | Phases 2-4 ~4 min | Phases 5-8 ~3 min

## Phase 1: Read and Understand (~30 seconds)

### 1a: Read skill files

Read the entire skill directory:

1. Read SKILL.md (frontmatter + body)
2. List and read all files in references/ (if exists)
3. List and read all files in scripts/ (if exists)

Do NOT skip any files — you need full context before researching.

### 1b: Assess improvement potential

Now that you have read the skill, reason through it:

- What is this skill's core purpose and domain? How well does the current implementation serve it?
- What are the most likely quality gaps? (description, structure, instruction clarity, error handling, missing patterns)
- What implicit constraints should be preserved? (the skill's personality, its users' expectations, integration points)
- What improvements would have the highest impact relative to effort?
- Which aspects of this skill's domain are most uncertain and would benefit from research?

Present a brief summary (3-5 sentences) of the skill's current state and your initial impression to the user.

### 1c: Clarify improvement scope

Based on your assessment, ask **2-4 targeted clarifying questions** about the user's improvement priorities — which aspects matter most, whether there are constraints on what can change, whether they want conservative fixes or aggressive restructuring, or any context about how the skill is used in practice. Bias toward asking rather than assuming. Only skip questions if the improvement need is obvious and unambiguous.

**Wait for the user's response before continuing.**

## Phase 2: Research Scope (~30 seconds)

Based on the skill's identified domain and purpose, select **3-5 research lenses** from [references/research-lenses.md](references/research-lenses.md):

1. **Best-in-Class Examples** — the best tools/skills in this domain to benchmark against
2. **Domain Evolution** — whether best practices have changed since the skill was written
3. **Common Quality Issues** — frequent weaknesses in similar tools/skills
4. **Edge Cases & Robustness** — unusual inputs or scenarios the skill might not handle

Pick the lenses most relevant to this skill's domain. List them with 2-3 sub-questions each, then immediately proceed.

## Phase 3: Parallel Research (~3 minutes)

Spawn one **deep-researcher** agent per theme. Launch ALL agents in parallel in a single message. Always specify `subagent_type: "deep-researcher"` in every Agent tool call — this subagent type has NO Agent tool and NO Skill tool available, providing structural enforcement that the text instructions below reinforce.

**Critical rules for EVERY agent:**
- Set `model: "sonnet"` on every agent
- Give each agent a different research lens for coverage diversity
- Each agent's prompt MUST include:
  - The skill's name, purpose, and domain from Phase 1
  - Its assigned lens and 2-3 sub-questions
  - This instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs. IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Rate source credibility using the framework in [references/source-evaluation.md](references/source-evaluation.md).

Wait for all agents to return before proceeding.

**If fewer than 2 agents return usable results**: Skip synthesis and proceed directly to Phase 5 using only standard best-practice analysis. Note that research was limited.

## Phase 4: Synthesize into Improvement Context (~1 minute)

Merge agent findings into an **Improvement Context** — a structured analysis for informing skill improvements. Keep this in context (do NOT write to disk — the skill directory should not be modified before user approval).

```markdown
## Improvement Context: [skill-name]

### Best-in-Class Benchmarks
- [What excellent tools/skills in this domain do that this skill could learn from]

### Domain-Specific Gaps
- [Things the current skill is missing based on domain research]

### Quality Patterns
- [Research-backed patterns that would improve this skill]

### Priority Insights
- [Ranked list of the most impactful improvements based on research]

### Sources
| # | Source | URL | Credibility |
[Top 10 sources with credibility ratings]
```

**Only use URLs that agents explicitly returned. Never generate a citation URL from memory.**

## Phase 5: Validate

Run the validation script:

```
python "${CLAUDE_SKILL_DIR}/../validate-skill/scripts/quick_validate.py" $ARGUMENTS
```

Capture the JSON output. If the script is unavailable, perform manual validation against the spec.

Then perform qualitative assessment beyond what the script checks:

- **Description quality**: third person, what+when, trigger keywords, "Use when..." clause. Check description length against the ~15,000 char combined budget — verbose descriptions can silently prevent other skills from activating.
- **Instruction quality**: imperative voice, appropriate specificity, output template. Flag content Claude already knows from general training — only project-specific or post-cutoff information should remain.
- **Structure**: line count, reference organization, progressive disclosure
- **Patterns**: are the right patterns used for this task type?

Load [references/best-practices.md](references/best-practices.md) and [references/skill-spec.md](references/skill-spec.md) for the full checklist.

## Phase 6: Identify Improvements (Research-Enhanced)

Compare the skill against best practices AND the Improvement Context from Phase 4. Categorize every finding:

**Critical** (must fix — spec violations or functional issues):
- Invalid name format, description over 1024 chars, forbidden keys
- Body over 500 lines without references/ split
- Missing required fields (name, description)

**High priority** (should fix — significant quality issues):
- Description not in third person
- Description missing "when to use" component or trigger keywords
- No output format defined
- Suggestive language instead of imperative
- No edge case or error handling

**Medium priority** (nice to fix — best practice improvements):
- Could benefit from references/ (body over 300 lines)
- Could benefit from scripts/ (has deterministic validation steps)
- Missing concrete input/output examples
- Missing argument-hint

**Low priority** (polish):
- Formatting consistency
- Section ordering
- Terminology consistency
- Cross-platform issues: Windows-style paths, complex Bash chaining in allowed-tools (prefix matching is fragile across environments)

**Tag research-informed improvements with `[Research]`** so the user can distinguish between standard best-practice checks and domain-specific insights from the research phase.

## Phase 7: Present Improvement Plan

Present findings in this format:

```markdown
# Improvement Plan: [skill-name]
_Analyzed: [today's date] | Research: [count] sources consulted_

## Current Assessment
[1-2 sentence summary of the skill's current state]
Overall: [EXCELLENT / GOOD / NEEDS WORK / SIGNIFICANT ISSUES]

## Research-Informed Insights
[2-3 bullet summary of the most impactful findings from domain research, with source citations]

## Proposed Changes

### Critical
1. **[What to change]**: [Specific change and why]

### High Priority
1. **[What to change]**: [Specific change and why]
1. `[Research]` **[What to change]**: [Research-backed change with citation]

### Medium Priority
1. **[What to change]**: [Specific change and why]

### Low Priority
1. **[What to change]**: [Specific change and why]

## Apply Changes?
Reply with one of:
- **"apply all"** — apply everything
- **"apply critical"** — only critical fixes
- **"apply critical+high"** — critical and high priority
- **"show diff"** — show what would change without applying
- **Or specify items by number** (e.g., "apply Critical 1, High 2")
```

**For description improvements**: generate 2-3 description variants with different trigger keyword strategies. Present them with trade-off explanations.

## Phase 8: Apply & Summarize

When the user approves:

1. **Backup**: Copy original SKILL.md to `SKILL.md.bak` in the same directory
2. **Apply**: Make the approved changes to SKILL.md (and other files if applicable)
3. **Re-validate**: Run quick_validate.py on the modified skill
4. If validation fails, fix and re-validate until it passes
5. **Self-check**: Verify the changes preserve the skill's original intent from Phase 1. If improvements have drifted from the skill's purpose, revert the problematic changes.

Present the summary:

```markdown
# Improvement Summary: [skill-name]

## Changes Applied
- [List of each change made]
- [Research] [List of research-informed changes]

## Before/After
| Aspect | Before | After |
|--------|--------|-------|
| Description length | [old] chars | [new] chars |
| Body line count | [old] lines | [new] lines |
| Validation status | [old] | [new] |
| Trigger clause | [present/missing] | [present/missing] |
| Research insights applied | N/A | [count] |

## Validation Result
[Paste final quick_validate.py JSON output or manual validation result]

## Next Steps
[Any remaining suggestions that weren't applied, or "No further improvements needed"]
```

## Rules

- Always validate BEFORE and AFTER changes
- Always create a .bak backup before modifying any file
- Never apply changes without user approval
- Never write to the skill directory before user approval (keep Improvement Context in memory)
- Present specific, actionable improvements — not vague suggestions
- When suggesting description changes, provide complete replacement text
- Preserve the skill's intent and personality — improve execution, not purpose
- If the skill is already high quality, say so — don't invent problems to fix
- Generate 2-3 description variants when improving descriptions
- Tag research-sourced improvements with `[Research]` for transparency
- Only use URLs that agents explicitly returned — never fabricate citations
- If research returns limited results, proceed with standard improvement and note the limitation
- All research agents MUST specify `subagent_type: "deep-researcher"` in every Agent tool call — this structurally prevents sub-agents from spawning further agents. Never use a general-purpose subagent type.
