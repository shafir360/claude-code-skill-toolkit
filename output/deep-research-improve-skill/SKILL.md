---
name: deep-research-improve-skill
description: 'Analyzes and improves an existing Claude Code skill using exhaustive two-round research with tiered model strategy. Round 1 spawns broad-sweep Sonnet agents to benchmark against best-in-class tools. An Opus gap-analysis identifies weak spots, then Round 2 launches targeted collectors plus a dedicated Opus skeptic that challenges improvement assumptions. Produces research-backed improvements with per-finding confidence and contradiction analysis. Use when saying "deep research improve", "deep improve skill", "exhaustive skill improvement", or when maximum improvement quality matters more than speed.'
argument-hint: "path/to/skill-directory"
allowed-tools:
  - Read
  - Write
  - Bash(python *)
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Deep Research & Improve Skill: $ARGUMENTS

You are analyzing an existing Claude Code skill and improving it with exhaustive two-round research. This premium-tier improvement uses a **tiered model strategy**: Sonnet agents for fast parallel data collection, Opus agents for gap analysis, skeptic review, and synthesis. Choose this over `/research-improve-skill` when the domain is unfamiliar, complex, or when maximum improvement quality matters more than speed.

**Time budget**: Phase 1 ~30s | Phases 2-5 ~8min | Phase 6 ~1.5min | Phases 7-10 ~5min

## Phase 1: Read and Understand (~30 seconds)

Read the entire skill directory:

1. Read SKILL.md (frontmatter + body)
2. List and read all files in references/ (if exists)
3. List and read all files in scripts/ (if exists)
4. Note the skill's purpose, domain, target use cases, and overall approach

Do NOT skip any files — you need full context before researching.

## Phase 2: Research Plan (~30 seconds)

Based on the skill's domain and purpose, identify **4-6 research themes**. Prefer fewer, deeper themes over more shallow ones. Select lenses from [references/research-lenses.md](references/research-lenses.md):

1. **Best-in-Class Examples** — best tools/skills in this domain to benchmark against
2. **Domain Evolution** — whether best practices have changed since the skill was written
3. **Common Quality Issues** — frequent weaknesses in similar tools/skills
4. **Edge Cases & Robustness** — unusual inputs or scenarios the skill might not handle
5. **Prior Art** — existing tools that solve the same problem differently

For each theme, define:
- A clear research question (1 sentence)
- 2-3 sub-questions to guide the agent
- A research lens (benchmarking, critic, evolution, edge-case, practitioner)

Present the research plan briefly, then proceed immediately.

## Phase 3: Broad Sweep — Round 1 (~3 minutes)

Spawn one **deep-researcher** agent for EACH theme. Launch ALL agents in parallel in a single message.

**Critical rules for EVERY Round 1 agent:**
- Set `model: "sonnet"` on every agent (Sonnet handles search/fetch efficiently)
- Each agent gets a unique theme and lens — NO overlap between agents
- Each agent's prompt MUST include this instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Structure your response using these exact sections:

FINDINGS:
- [3-5 bullet points, one sentence each with an inline citation URL]

SOURCES:
- [Top 5 source URLs, each with a credibility rating: HIGH/MEDIUM/LOW]

SURPRISES:
- [Any contradictions, under-sourced claims, or unexpected discoveries — or 'None']

Do NOT include source tables, contradiction tables, or lengthy analysis paragraphs. Keep each section concise. IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Each agent's prompt must also include:
- The skill's name, purpose, and domain from Phase 1
- Its specific assigned theme, lens, and 2-3 sub-questions
- Instruction to note surprising contradictions or under-sourced claims

Rate source credibility using the framework in [references/source-evaluation.md](references/source-evaluation.md).

Wait for all agents to return before proceeding.

**If an agent fails or returns empty**: Skip it. If fewer than 3 agents return usable results, note the coverage gap and consider launching 1-2 replacement agents before proceeding.

## Phase 4: Gap Analysis & Round 2 Planning (~1 minute)

Spawn a single **deep-researcher** agent with `model: "opus"` to analyze Round 1 findings.

The agent's prompt MUST include all Round 1 findings and these instructions:

"You are analyzing Round 1 research findings about a skill's domain to plan Round 2 improvement research. Perform:

1. **Coverage Assessment**: Which improvement areas are well-covered (3+ sources)? Which are thin?
2. **Contradiction Detection**: Where do findings conflict? List specific contradictions.
3. **Single-Source Claims**: Flag improvement suggestions backed by only one source.
4. **Missing Angles**: What important improvement areas were NOT covered?
5. **Strongest Assumptions to Challenge**: Identify 2-3 confident improvement assumptions the skeptic should try to disprove — sometimes the current approach is already optimal.

Return:
- 3-5 specific research targets for Round 2 collectors
- 2-3 specific improvement assumptions for the skeptic to challenge
- Confidence assessment of improvement potential so far

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

## Phase 5: Targeted Deep Dives — Round 2 (~3 minutes)

Based on the gap analysis, spawn two types of agents in parallel in a single message:

### Collector Agents (3-4 agents, `model: "sonnet"`)
Each targets a specific gap identified in Phase 4. Their prompts MUST:
- Reference the specific gap or question from the gap analysis
- Include relevant context from Round 1 that should inform their search
- Follow citation chains: search for papers/articles that cite or respond to key Round 1 sources
- Include the same data-collection instruction as Round 1 (verbatim block above), BUT raise the WebFetch limit to 3 calls (Round 2 agents do targeted deep dives and may need more full-page reads)
- Include: "Also look for evidence that CONTRADICTS the prevailing improvement suggestions from Round 1. The current skill might already be doing things the right way."

### Skeptic Agent (1 **deep-researcher** agent, `model: "opus"`)
A dedicated adversarial agent that challenges improvement assumptions. Its prompt MUST include the 2-3 assumptions from Phase 4 and this instruction verbatim:

"You are a skeptic reviewing proposed improvements to an existing skill. Your job is NOT to confirm improvements are needed — it is to challenge them. For each assumption:
1. Search for evidence that the CURRENT approach might actually be optimal
2. Look for cases where the proposed improvement caused problems elsewhere
3. Check if the improvement suggestion is based on outdated or disputed best practices
4. Consider whether the improvement adds complexity without proportional benefit

Sometimes the best improvement is no change. Challenge every suggestion regardless of how reasonable it seems. Every challenge MUST reference a specific source URL. Do not speculate without evidence — unsupported challenges will be discarded. Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 600 words. Return: challenges/counter-evidence for each assumption (with citation URLs), and your top 5 source URLs with credibility ratings.

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Wait for all Round 2 agents to return before proceeding.

## Phase 6: Synthesize into Enhanced Improvement Context (~1.5 minutes)

Spawn a single **deep-researcher** agent with `model: "opus"` to produce the final synthesis.

The agent's prompt MUST include all Round 1 findings, the gap analysis, all Round 2 findings (collectors + skeptic), and these instructions:

"You are synthesizing two rounds of research into an Improvement Context for enhancing a Claude Code skill. Perform:

1. **Cross-Validation**: For each improvement suggestion, count independent sources. Note agreements and conflicts.
2. **Per-Finding Confidence**: High (3+ sources agree), Medium (2 sources or counter-evidence exists), Low (single source — flag it).
3. **Contradiction Resolution**: Present both sides with evidence strength.
4. **Skeptic Integration**: Which improvements survived scrutiny? Which were challenged? Which should be abandoned?
5. **Priority Ranking**: Rank improvements by confidence level AND expected impact.

Return a structured Improvement Context with: Best-in-Class Benchmarks, Domain-Specific Gaps, Quality Patterns, Contradictions, Skeptic's Assessment, Priority Improvements (ranked by confidence x impact), and complete source list.

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Keep the Improvement Context in memory (do NOT write to disk before user approval).

## Phase 7: Validate

Run the validation script:

```
python "${CLAUDE_SKILL_DIR}/../validate-skill/scripts/quick_validate.py" $ARGUMENTS
```

Capture the JSON output. If the script is unavailable, perform manual validation against the spec.

Then perform qualitative assessment:

- **Description quality**: third person, what+when, trigger keywords, "Use when..." clause. Check description length against the ~15,000 char combined budget.
- **Instruction quality**: imperative voice, appropriate specificity, output template. Flag content Claude already knows from general training.
- **Structure**: line count, reference organization, progressive disclosure
- **Patterns**: are the right patterns used for this task type?

Load [references/best-practices.md](references/best-practices.md) and [references/skill-spec.md](references/skill-spec.md) for the full checklist.

## Phase 8: Identify Improvements (Deep Research-Enhanced)

Compare the skill against best practices AND the Enhanced Improvement Context from Phase 6. Categorize every finding:

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
- Cross-platform issues

**Tag research-informed improvements** with `[Research: Confidence H/M/L]` so the user can distinguish between standard checks and research-backed insights, and see how well-supported each suggestion is.

**Skeptic-challenged improvements**: If the skeptic successfully challenged an improvement assumption, note it explicitly: `[Skeptic: challenged — see rationale]`.

## Phase 9: Present Improvement Plan

Present findings in this format:

```markdown
# Deep Research Improvement Plan: [skill-name]
_Analyzed: [today's date] | Research: [count] sources | Rounds: 2 | Confidence: [overall]_

## Current Assessment
[1-2 sentence summary]
Overall: [EXCELLENT / GOOD / NEEDS WORK / SIGNIFICANT ISSUES]

## Deep Research Insights
[3-5 bullet summary of the most impactful findings with confidence levels and citations]

## Skeptic's Assessment
[Which proposed improvements were challenged and why — helps user make informed decisions]

## Proposed Changes

### Critical
1. **[What to change]**: [Specific change and why]

### High Priority
1. **[What to change]**: [Specific change and why]
1. `[Research: HIGH]` **[What to change]**: [Research-backed change with citation]

### Medium Priority
1. **[What to change]**: [Specific change and why]
1. `[Skeptic: challenged]` **[What to change]**: [Why skeptic challenged this and current recommendation]

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

## Phase 10: Apply & Summarize

When the user approves:

1. **Backup**: Copy original SKILL.md to `SKILL.md.bak` in the same directory
2. **Apply**: Make the approved changes to SKILL.md (and other files if applicable)
3. **Re-validate**: Run quick_validate.py on the modified skill
4. If validation fails, fix and re-validate until it passes
5. **Self-check**: Verify the changes preserve the skill's original intent from Phase 1

Present the summary:

```markdown
# Deep Research Improvement Summary: [skill-name]

## Changes Applied
- [List of each change made]
- [Research: H/M/L] [List of research-informed changes with confidence]
- [Skeptic-survived] [Changes that passed skeptic scrutiny]

## Before/After
| Aspect | Before | After |
|--------|--------|-------|
| Description length | [old] chars | [new] chars |
| Body line count | [old] lines | [new] lines |
| Validation status | [old] | [new] |
| Trigger clause | [present/missing] | [present/missing] |
| Research insights applied | N/A | [count] (H:[n] M:[n] L:[n]) |

## Validation Result
[Final validation output]

## Research Brief
[Saved to output/<skill-name>/RESEARCH_BRIEF.md for reference]

## Next Steps
[Remaining suggestions not applied, or "No further improvements needed"]
```

Save the research brief to `output/<skill-name>/RESEARCH_BRIEF.md` for future reference.

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
- Tag research-sourced improvements with `[Research: Confidence H/M/L]` for transparency
- Tag skeptic-challenged improvements with `[Skeptic: challenged]` so users can make informed decisions
- NEVER generate citation URLs from memory — only use URLs agents explicitly returned
- Use tiered models: `model: "sonnet"` for data-gathering, `model: "opus"` for gap analysis, synthesis, and skeptic. All agents MUST use the **deep-researcher** subagent type — never use general-purpose.
- If Round 1 returns fewer than 3 usable results, skip Round 2 and note limitation
- If research returns limited results, proceed with standard improvement and note the limitation
- Rules section improvements MUST prioritize HIGH-confidence pitfalls from research
