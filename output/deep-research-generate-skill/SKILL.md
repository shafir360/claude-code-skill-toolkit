---
name: deep-research-generate-skill
description: 'Generates a Claude Code skill backed by exhaustive two-round research with tiered model strategy. Round 1 spawns broad-sweep Sonnet agents across the skill domain. An Opus gap-analysis identifies weak spots, then Round 2 launches targeted collectors plus a dedicated Opus skeptic agent. Produces a research-informed skill with enhanced design brief containing per-finding confidence levels and contradiction analysis. Use when saying "deep research generate", "deep generate skill", "exhaustive skill generation", or when maximum research quality matters more than speed.'
argument-hint: "description of what the skill should do"
allowed-tools:
  - Read
  - Write
  - Bash(python *)
  - Bash(mkdir *)
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Deep Research & Generate Skill: $ARGUMENTS

You are creating a new Claude Code skill backed by exhaustive two-round research. This premium-tier skill generation uses a **tiered model strategy**: Sonnet agents for fast parallel data collection, Opus agents for gap analysis, skeptic review, and synthesis. Choose this over `/research-generate-skill` when the domain is unfamiliar, complex, or when maximum quality matters more than speed.

**Time budget**: Phase 1 ~1min | Phases 2-5 ~8min | Phase 6 ~1.5min | Phases 7-9 ~5min

## Phase 1: Requirements (~1 minute)

Analyze the user's description and determine:

1. **Purpose**: What does this skill do? (one sentence)
2. **Trigger scenarios**: When should a user invoke this? (3-5 scenarios)
3. **Input**: What does the user provide? (arguments, files, context)
4. **Output**: What does the user get back? (report, files, changes, chat output)
5. **Tools needed**: Which tools does this skill require? (Read, Write, Bash, WebSearch, etc.)
6. **Complexity**: Simple (single-phase), moderate (multi-phase), or complex (agents, scripts)?
7. **Task fragility**: High freedom (creative), medium (preferred pattern), or low (critical/exact)?

If the description is vague, ambiguous, or contains contradictory requirements, ask **at most 3** targeted clarifying questions. Do not ask more — infer reasonable defaults for anything unclear.

Present the requirements summary and get user confirmation before proceeding.

## Phase 2: Research Plan (~30 seconds)

Based on the confirmed requirements, identify **5-7 research themes** specific to the skill's domain. Select lenses from [references/research-lenses.md](references/research-lenses.md):

1. **Prior Art** — existing tools, skills, or scripts that solve this problem
2. **Domain Patterns** — conventions, standards, and best practices in this space
3. **Pitfalls & Failure Modes** — common mistakes and edge cases
4. **Input/Output Patterns** — data formats and boundary cases
5. **User Workflow Context** — how practitioners do this task today

For each theme, define:
- A clear research question (1 sentence)
- 2-3 sub-questions to guide the agent
- A research lens (technical, skeptic/critic, industry, academic, practitioner)

Present the research plan briefly, then proceed immediately.

## Phase 3: Broad Sweep — Round 1 (~3 minutes)

Spawn one **deep-researcher** agent for EACH theme. Launch ALL agents in parallel in a single message.

**Critical rules for EVERY Round 1 agent:**
- Set `model: "sonnet"` on every agent (Sonnet handles search/fetch efficiently)
- Each agent gets a unique theme and lens — NO overlap between agents
- Each agent's prompt MUST include this instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs. IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Each agent's prompt must also include:
- The skill topic and purpose from Phase 1
- Its specific assigned theme, lens, and 2-3 sub-questions
- Instruction to note any surprising contradictions or claims that seem under-sourced

Rate source credibility using the framework in [references/source-evaluation.md](references/source-evaluation.md).

Wait for all agents to return before proceeding.

**If an agent fails or returns empty**: Skip it. If fewer than 3 agents return usable results, note the coverage gap and consider launching 1-2 replacement agents before proceeding.

## Phase 4: Gap Analysis & Round 2 Planning (~1 minute)

Spawn a single **deep-researcher** agent with `model: "opus"` to analyze Round 1 findings.

The agent's prompt MUST include all Round 1 findings and these instructions:

"You are analyzing Round 1 research findings about a skill domain to plan Round 2 targeted deep dives. Perform:

1. **Coverage Assessment**: Which aspects are well-covered (3+ sources)? Which are thin (single source)?
2. **Contradiction Detection**: Where do findings conflict? List specific contradictions.
3. **Single-Source Claims**: Flag findings backed by only one source.
4. **Missing Angles**: What important aspects were NOT covered?
5. **Strongest Claims to Challenge**: Identify 2-3 confident claims the skeptic should try to disprove or nuance.

Return:
- 3-5 specific research targets for Round 2 collectors (with clear questions and why each matters)
- 2-3 specific claims for the skeptic to challenge (with exact claim text)
- Confidence assessment of research so far

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

## Phase 5: Targeted Deep Dives — Round 2 (~3 minutes)

Based on the gap analysis, spawn two types of agents in parallel in a single message:

### Collector Agents (3-4 agents, `model: "sonnet"`)
Each targets a specific gap identified in Phase 4. Their prompts MUST:
- Reference the specific gap or question from the gap analysis
- Include relevant context from Round 1 that should inform their search
- Follow citation chains: search for papers/articles that cite or respond to key Round 1 sources
- Include the same data-collection instruction as Round 1 (verbatim block above)
- Include: "Also look for evidence that CONTRADICTS the prevailing findings from Round 1."

### Skeptic Agent (1 **deep-researcher** agent, `model: "opus"`)
A dedicated adversarial agent that challenges the strongest claims. Its prompt MUST include the 2-3 claims from Phase 4 and this instruction verbatim:

"You are a skeptic and devil's advocate. Your job is NOT to confirm existing findings — it is to challenge them. For each claim:
1. Search for evidence that CONTRADICTS or NUANCES the claim
2. Look for criticisms, rebuttals, or alternative explanations
3. Check if the claim's sources have been disputed or retracted
4. Consider whether the claim overgeneralizes or omits important caveats

Challenge the majority position regardless of how confident it seems. Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 600 words. Return: challenges/counter-evidence for each claim (with citation URLs), and your top 5 source URLs with credibility ratings.

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Wait for all Round 2 agents to return before proceeding.

## Phase 6: Synthesize into Enhanced Design Brief (~1.5 minutes)

Spawn a single **deep-researcher** agent with `model: "opus"` to produce the final synthesis.

The agent's prompt MUST include all Round 1 findings, the gap analysis, all Round 2 findings (collectors + skeptic), and these instructions:

"You are synthesizing two rounds of research into a Design Brief for generating a Claude Code skill. Perform:

1. **Cross-Validation**: For each finding, count independent sources. Note agreements and conflicts.
2. **Per-Finding Confidence**: High (3+ independent sources, no counter-evidence), Medium (2 sources or counter-evidence exists), Low (single source — flag it).
3. **Contradiction Resolution**: Present both sides with evidence strength.
4. **Skeptic Integration**: Which claims survived scrutiny? Which were nuanced?
5. **Skill Design Implications**: How should each finding influence the skill's design?

Return a structured Design Brief with: Prior Art, Domain Patterns, Pitfalls to Avoid (with confidence tags), Recommended Approach, Contradictions, Knowledge Gaps, and complete source list with credibility ratings.

IMPORTANT: Do NOT use the Agent tool to spawn sub-agents. Do NOT invoke any skills via the Skill tool. You are a leaf-node agent — complete your analysis and return your findings directly."

Write the Design Brief to `output/<skill-name>/RESEARCH_BRIEF.md`:

```markdown
# Enhanced Design Brief: [skill topic]
_Generated: [today's date] | Sources: [count] | Rounds: 2 | Confidence: [overall]_

## Prior Art
- [Existing tools/skills — what they do well and poorly] `[Confidence: H/M/L]`

## Domain Patterns
- [Best practices, conventions, standards] `[Confidence: H/M/L]`

## Pitfalls to Avoid
- [Failure modes with confidence tags — prioritize HIGH confidence pitfalls]

## Recommended Approach
- [Synthesis: how should this skill be built, informed by all findings?]

## Contradictions & Open Questions
- [Areas of disagreement across sources]
- [Claims the skeptic successfully challenged or nuanced]

## Knowledge Gaps
- [What couldn't be determined and why]

## Sources
| # | Source | URL | Credibility | Round |
[Top 15-20 sources with credibility ratings and which round found them]
```

**Only use URLs that agents explicitly returned. Never generate a citation URL from memory.**

## Phase 7: Design (Research-Informed)

Make design decisions informed by the Enhanced Design Brief:

### Skill structure
- **Simple** (SKILL.md only): focused, single-purpose tasks under 200 lines
- **Standard** (SKILL.md + references/): tasks needing background knowledge or specs
- **Full** (SKILL.md + references/ + scripts/): tasks with deterministic validation steps

### Instruction pattern
- **Phase-based workflow**: multi-step sequential processes (most common)
- **Decision tree**: branching workflows
- **Checklist-driven**: quality gate / review tasks
- **Template-based**: tasks with rigid output format

### Model strategy
- Default: inherit parent model (no `model:` field)
- If spawning agents for parallel I/O: set agent `model: "sonnet"`
- For critical analysis agents: set agent `model: "opus"`

Read [references/skill-spec.md](references/skill-spec.md) for spec constraints and [references/best-practices.md](references/best-practices.md) for pattern details.

**Research integration** — use the Enhanced Design Brief to inform every decision:
- Prior Art → instruction pattern (what patterns work)
- Domain Patterns → reference files needed
- Pitfalls (HIGH confidence) → Rules section items (mandatory)
- Pitfalls (MEDIUM confidence) → Rules section items (recommended)
- Contradictions → areas requiring flexibility in the skill
- Recommended Approach → phase breakdown

## Phase 8: Generate

Save the generated skill to `output/<skill-name>/`:
- Create `output/<skill-name>/` directory if it doesn't exist

### 8a: Write SKILL.md

**Frontmatter** — follow these rules exactly:
- `name`: kebab-case, gerund form preferred, max 64 chars
- `description`: Third person. Include WHAT + WHEN. ALWAYS include a "Use when..." clause with literal trigger phrases. 100-200 words, max 1024 chars. No angle brackets. Keep descriptions concise — all installed skills share a ~15,000 char combined budget.
- `argument-hint`: show expected input format
- `allowed-tools`: only the tools actually needed

**Body** — follow these conventions:
1. H1 title: `# [Action Verb]: $ARGUMENTS`
2. Brief intro (1-2 sentences)
3. Numbered phases with imperative instructions
4. Output Format section with exact markdown template in fenced code block
5. Rules section with 5-10 specific, actionable constraints
6. Only include instructions Claude wouldn't know from general training

**Research incorporation**: Rules section MUST address at least 3 HIGH-confidence pitfalls from the Design Brief. Instruction phases SHOULD reflect domain best practices found in research. If the skeptic challenged a common approach, note the alternative.

Read [references/example-skills.md](references/example-skills.md) for style reference.

### 8b: Create references/ (if Standard or Full structure)

For skills needing background knowledge:
- Create reference files with descriptive names
- Include a table of contents for files over 100 lines
- Keep references one level deep

### 8c: Create scripts/ (if Full structure)

For skills with deterministic validation or automation:
- Python scripts, standard library only
- Explicit error handling with descriptive messages
- JSON output for structured results
- Use forward slashes in all paths

### 8d: Write README.md

Create `output/<skill-name>/README.md` with full documentation. The README should be clear enough that someone who's never used Claude Code can understand what the skill does, why it's useful, and how to use it.

```markdown
# [skill-name]

> [One-line pitch — what this does in plain English.]

[2-3 sentence description for a newcomer. Explain what problem it solves.]

## Why Use This

- [What problem it solves]
- [What makes it better than doing it manually]
- [Key differentiator]

## Quick Start

```
/[skill-name] [simplest possible example]
```

## Usage

```
/[skill-name] [full syntax with argument-hint]
```

### Examples

- `/[skill-name] [concrete example 1]`
- `/[skill-name] [concrete example 2]`
- `/[skill-name] [concrete example 3]`

## How It Works

[Step-by-step explanation. For multi-phase skills, use a table with phase, timing, and description.]

## Example Output

[Abbreviated but realistic example of what the skill produces — fenced code block.]

## Deep Research Insights

[5-8 bullet points from the Enhanced Design Brief. Include `[Confidence: H/M/L]` tags and source URLs where available.]

## When to Use This vs Alternatives

[Comparison with lighter/heavier alternatives in the toolkit.]

## Tools Used

| Tool | Purpose |
|------|---------|
| [tool] | [why] |

## Limitations & Edge Cases

- [Time cost, failure modes, when to use simpler alternatives]

## Sources & References

[List the most important source URLs from the Enhanced Design Brief as clickable links. Every major design decision should be traceable to a source. Format as bullet list with linked titles and one-line descriptions.]

## Installation

```bash
cp -r output/[skill-name] ~/.claude/skills/[skill-name]
```

Or: `/implement-skill [skill-name]`

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- [Any other requirements]

---

_Generated by [Claude Code Skill Toolkit](https://github.com/shafir360/claude-code-skill-toolkit) (deep-research mode)_
```

## Phase 9: Validate & Present

Run the validate-skill script:

```
python "${CLAUDE_SKILL_DIR}/../validate-skill/scripts/quick_validate.py" output/<skill-name>
```

If validation reports any FAIL or WARN, fix the issues and re-validate.

**Self-check before presenting**: Verify the generated SKILL.md matches the original requirements from Phase 1. Check that purpose, triggers, inputs, and outputs align. If context drift has caused divergence, fix before presenting.

Present the result:

```markdown
## Generated Skill: [skill-name]

### Directory Structure
[tree view of generated files]

### SKILL.md
[full content of the generated SKILL.md]

### Deep Research Insights Applied
- **[Insight]** `[Confidence: H/M/L]`: [How it influenced the skill design]
- ...

### Skeptic's Impact
- [Which research findings were nuanced or changed by the skeptic agent]

### Design Decisions
- **Structure**: [simple/standard/full] — [why]
- **Pattern**: [phase/decision tree/checklist] — [why]
- **Tools**: [list] — [why each is needed]
- **Research depth**: [N] sources across 2 rounds

### Try It
- `/[skill-name] [example input 1]`
- `/[skill-name] [example input 2]`
```

The skill and enhanced research brief have been saved to `output/[skill-name]/`.

Ask: "Would you like me to install this skill to `.claude/skills/` now, or keep it in output/ for later? You can install it later with `/implement-skill [skill-name]`."

## Rules

- ALWAYS save generated skills to `output/<skill-name>/` in the project root
- ALWAYS save the RESEARCH_BRIEF.md alongside the generated skill
- ALWAYS validate before presenting to the user
- SKILL.md body MUST be under 500 lines
- Description MUST be third person and include both "what" and "when"
- Description MUST include a "Use when..." clause with literal trigger phrases
- Name MUST be kebab-case
- Use the simplest structure that works — do not add references/ or scripts/ unless genuinely needed
- Never generate skills with non-standard Python dependencies in scripts/
- Rules section MUST address at least 3 HIGH-confidence pitfalls from the Design Brief
- NEVER generate citation URLs from memory — only use URLs agents explicitly returned
- Use tiered models: `model: "sonnet"` for data-gathering agents, `model: "opus"` for gap analysis, synthesis, and skeptic. All agents MUST use the **deep-researcher** subagent type — never use general-purpose.
- If Round 1 returns fewer than 3 usable results, skip Round 2 and note the limitation
- If research returns limited results, proceed with generation and note the limitation
