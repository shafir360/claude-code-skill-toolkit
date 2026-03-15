---
name: research-generate-skill
description: Research a domain thoroughly, then generate a best-practice Claude Code skill informed by real-world findings. Spawns parallel Sonnet research agents to investigate existing tools, domain patterns, and common pitfalls before creating the skill. Use when wanting research-backed skill quality, or when saying "research and generate", "deep generate", "generate with research", or "research-powered skill".
argument-hint: <description of what the skill should do>
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

# Research & Generate Skill: $ARGUMENTS

You are creating a new Claude Code skill with a research-first approach. Before generating, you investigate the skill's domain to produce a better-informed, higher-quality result. Choose this over `/generate-skill` when the domain is unfamiliar or when quality matters more than speed.

**Time budget**: Phase 1 ~1 min | Phases 2-4 ~4 min | Phases 5-7 ~3 min

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

## Phase 2: Research Scope (~30 seconds)

Based on the confirmed requirements, identify **3-5 research themes** specific to the skill's domain. Select lenses from [references/research-lenses.md](references/research-lenses.md):

1. **Prior Art** — existing tools, skills, or scripts that solve this problem
2. **Domain Patterns** — conventions, standards, and best practices in this space
3. **Pitfalls & Failure Modes** — common mistakes and edge cases
4. **Input/Output Patterns** — data formats and boundary cases
5. **User Workflow Context** — how practitioners do this task today

Pick the 3-5 lenses most relevant to this skill. List them with 2-3 sub-questions each, then immediately proceed.

## Phase 3: Parallel Research (~3 minutes)

Spawn one **deep-researcher** agent per theme. Launch ALL agents in parallel in a single message.

**Critical rules for EVERY agent:**
- Set `model: "sonnet"` on every agent
- Give each agent a different research lens for coverage diversity
- Each agent's prompt MUST include:
  - The skill topic and purpose from Phase 1
  - Its assigned lens and 2-3 sub-questions
  - This instruction verbatim:

"Prioritize extracting facts from WebSearch result snippets. Only use WebFetch on 1-2 pages that truly need full-text reading. Do not exceed 2 WebFetch calls total. Keep your entire response under 500 words. Return ONLY: 3-5 key findings (one sentence each with an inline citation URL), and a list of your top 5 source URLs with credibility ratings (HIGH/MEDIUM/LOW). Do NOT include source tables, contradictions tables, or lengthy analysis paragraphs."

Rate source credibility using the framework in [references/source-evaluation.md](references/source-evaluation.md).

Wait for all agents to return before proceeding.

**If fewer than 2 agents return usable results**: Skip synthesis and proceed directly to Phase 5 using only existing knowledge. Note that research was limited.

## Phase 4: Synthesize into Design Brief (~1 minute)

Merge agent findings into a **Design Brief** — a structured document for informing skill generation. Do NOT produce a standalone research report.

Write the Design Brief to `output/<skill-name>/RESEARCH_BRIEF.md`:

```markdown
# Design Brief: [skill topic]
_Generated: [today's date] | Sources: [count]_

## Prior Art
- [Existing tools/skills found — what they do well and poorly]

## Domain Patterns
- [Best practices, conventions, standards discovered]

## Pitfalls to Avoid
- [Common mistakes, failure modes, edge cases from research]

## Recommended Approach
- [Synthesis: given the above, how should this skill be built?]
- [Specific techniques or patterns from the research to adopt]

## Sources
| # | Source | URL | Credibility |
[Top 10 sources with credibility ratings]
```

**Only use URLs that agents explicitly returned. Never generate a citation URL from memory.**

## Phase 5: Design (Research-Informed)

Make design decisions informed by the Design Brief:

### Skill structure
- **Simple** (SKILL.md only): focused, single-purpose tasks under 200 lines
- **Standard** (SKILL.md + references/): tasks needing background knowledge or specs
- **Full** (SKILL.md + references/ + scripts/): tasks with deterministic validation steps

### Instruction pattern
- **Phase-based workflow**: multi-step sequential processes (most common)
- **Decision tree**: branching workflows ("creating new vs. editing existing")
- **Checklist-driven**: quality gate / review tasks
- **Template-based**: tasks with rigid output format

### Model strategy
- Default: inherit parent model (no `model:` field)
- If spawning agents for parallel I/O: set agent `model: "sonnet"`

Read [references/skill-spec.md](references/skill-spec.md) for spec constraints and [references/best-practices.md](references/best-practices.md) for pattern details.

**Research integration**: Use the Design Brief to inform every decision:
- Prior Art → instruction pattern (what patterns work in this domain)
- Domain Patterns → reference files needed
- Pitfalls → Rules section items
- Recommended Approach → phase breakdown

## Phase 6: Generate

Save the generated skill to `output/<skill-name>/`:
- Create `output/<skill-name>/` directory if it doesn't exist

### 6a: Write SKILL.md

**Frontmatter** — follow these rules exactly:
- `name`: kebab-case, gerund form preferred, max 64 chars
- `description`: Third person. Include WHAT + WHEN. ALWAYS include a "Use when..." clause with literal trigger phrases. 100-200 words, max 1024 chars. No angle brackets. Keep descriptions concise — all installed skills share a ~15,000 char combined budget. Verbose descriptions can silently prevent other skills from activating.
- `argument-hint`: show expected input format
- `allowed-tools`: only the tools actually needed

**Body** — follow these conventions:
1. H1 title: `# [Action Verb]: $ARGUMENTS`
2. Brief intro (1-2 sentences)
3. Numbered phases with imperative instructions
4. Output Format section with exact markdown template in fenced code block
5. Rules section with 5-8 specific, actionable constraints
6. Only include instructions Claude wouldn't know from general training — do not over-explain basics. Focus on project-specific logic, conventions, and post-training-cutoff information.

**Research incorporation**: The Rules section MUST address at least 2 pitfalls from the Design Brief. Instruction phases SHOULD reflect domain best practices found in research.

Read [references/example-skills.md](references/example-skills.md) for style reference.

### 6b: Create references/ (if Standard or Full structure)

For skills needing background knowledge:
- Create reference files with descriptive names
- Include a table of contents for files over 100 lines
- Keep references one level deep

### 6c: Create scripts/ (if Full structure)

For skills with deterministic validation or automation:
- Python scripts, standard library only
- Explicit error handling with descriptive messages
- JSON output for structured results
- Use forward slashes in all paths. Avoid complex Bash chaining (`cmd1 && cmd2`) in allowed-tools as prefix matching is fragile across environments.

## Phase 7: Validate & Present

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

### Research Insights Applied
- **[Insight]**: [How it influenced the skill design]
- ...

### Design Decisions
- **Structure**: [simple/standard/full] — [why]
- **Pattern**: [phase/decision tree/checklist] — [why]
- **Tools**: [list] — [why each is needed]

### Try It
- `/[skill-name] [example input 1]`
- `/[skill-name] [example input 2]`
```

The skill and research brief have been saved to `output/[skill-name]/`.

Ask: "Would you like me to install this skill globally to ~/.claude/skills/ now, or keep it in output/ for later? You can install it later with `/implement-skill [skill-name]`."

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
- Research Rules section MUST address at least 2 pitfalls from the Design Brief
- Only use URLs that agents explicitly returned — never fabricate citations
- If research returns limited results, proceed with generation and note the limitation
