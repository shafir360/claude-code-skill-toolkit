---
name: generate-skill
description: Generate a complete Claude Code skill from a description of what it should do. Creates the full directory structure with SKILL.md, references, and scripts following Anthropic best practices. Use when creating, building, making, scaffolding, or writing a new Claude Code skill or slash command.
argument-hint: <description of what the skill should do>
allowed-tools:
  - Read
  - Write
  - Bash(python *)
  - Bash(mkdir *)
  - Grep
  - Glob
---

# Generate Skill: $ARGUMENTS

You are creating a new Claude Code skill based on the user's description. Follow Anthropic's official spec and best practices to produce a high-quality, well-structured skill.

## Phase 1: Requirements

Analyze the user's description and determine:

1. **Purpose**: What does this skill do? (one sentence)
2. **Trigger scenarios**: When should a user invoke this? (3-5 scenarios)
3. **Input**: What does the user provide? (arguments, files, context)
4. **Output**: What does the user get back? (report, files, changes, chat output)
5. **Tools needed**: Which tools does this skill require? (Read, Write, Bash, WebSearch, etc.)
6. **Complexity**: Simple (single-phase), moderate (multi-phase), or complex (agents, scripts)?
7. **Task fragility**: High freedom (creative), medium (preferred pattern), or low (critical/exact)?

If the description is too vague to determine these, ask **at most 3** targeted clarifying questions. Do not ask more — infer reasonable defaults for anything unclear.

Present the requirements summary and get user confirmation before proceeding.

## Phase 2: Design

Based on requirements, make these design decisions:

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
- Only override `model:` in frontmatter if the skill specifically needs a different model

Read [references/skill-spec.md](references/skill-spec.md) for spec constraints and [references/best-practices.md](references/best-practices.md) for pattern details.

## Phase 3: Generate

Save the generated skill to the `output/` folder in the project root:
- Path: `output/<skill-name>/SKILL.md` (+ references/, scripts/ as needed)
- Create `output/` directory if it doesn't exist
- Create `output/<skill-name>/` directory

### 3a: Write SKILL.md

**Frontmatter** — follow these rules exactly:
- `name`: kebab-case, gerund form preferred (e.g., `processing-pdfs`), max 64 chars
- `description`: Third person. Include WHAT it does + WHEN to use it. ALWAYS include a "Use when..." clause with literal trigger phrases. 100-200 words, max 1024 chars. No angle brackets.
- `argument-hint`: show expected input format
- `allowed-tools`: only the tools actually needed — never include extras

**Body** — follow these conventions:
1. H1 title: `# [Action Verb]: $ARGUMENTS`
2. Brief intro (1-2 sentences)
3. Numbered phases with imperative instructions
4. Output Format section with exact markdown template in fenced code block
5. Rules section with 5-8 specific, actionable constraints

Read [references/example-skills.md](references/example-skills.md) for style reference.

### 3b: Create references/ (if Standard or Full structure)

For skills needing background knowledge:
- Create reference files with descriptive names (e.g., `api-reference.md`, not `ref.md`)
- Include a table of contents for files over 100 lines
- Keep references one level deep — no nesting

### 3c: Create scripts/ (if Full structure)

For skills with deterministic validation or automation:
- Python scripts, standard library only
- Explicit error handling with descriptive messages
- JSON output for structured results
- Comment every non-obvious constant

## Phase 4: Validate

Run the validate-skill script against the generated skill:

```
python "${CLAUDE_SKILL_DIR}/../validate-skill/scripts/quick_validate.py" <generated-skill-path>
```

If the script is not available, manually verify:
- Name: kebab-case, no `--`, max 64 chars
- Description: third person, no angle brackets, max 1024 chars, includes what + when
- Body: under 500 lines
- All frontmatter keys are valid

If validation reports any FAIL or WARN, fix the issues and re-validate. Do not present until validation passes with no FAILs.

## Phase 5: Present

Show the user:

```markdown
## Generated Skill: [skill-name]

### Directory Structure
[tree view of generated files]

### SKILL.md
[full content of the generated SKILL.md]

### Design Decisions
- **Structure**: [simple/standard/full] — [why]
- **Pattern**: [phase/decision tree/checklist] — [why]
- **Tools**: [list] — [why each is needed]

### Try It
- `/[skill-name] [example input 1]`
- `/[skill-name] [example input 2]`
- `/[skill-name] [example input 3]`
```

The skill has been saved to `output/[skill-name]/`.

Ask: "Would you like me to install this skill globally to ~/.claude/skills/ now, or keep it in output/ for later? You can install it later with `/implement-skill [skill-name]`."

If the user wants to install now, copy the entire skill directory from `output/[skill-name]/` to `~/.claude/skills/[skill-name]/`.

## Rules

- ALWAYS save generated skills to `output/<skill-name>/` in the project root
- ALWAYS validate before presenting to the user
- SKILL.md body MUST be under 500 lines
- Description MUST be third person and include both "what" and "when"
- Description MUST include a "Use when..." clause with literal trigger phrases
- Name MUST be kebab-case
- Use the simplest structure that works — do not add references/ or scripts/ unless genuinely needed
- Never generate skills with non-standard Python dependencies in scripts/
- Prefer concrete examples over abstract rules in generated instructions
- Match instruction specificity to task fragility (high freedom for creative, low for critical)
- Follow the user's existing skill style (see example-skills.md reference)
