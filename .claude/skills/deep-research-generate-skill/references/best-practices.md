# Claude Code Skill Best Practices

## Description Writing

### The "Use when..." Pattern (95% activation)

Embed literal trigger phrases in description:

```yaml
# ~20% activation
description: Processes documents and generates reports

# ~95% activation
description: Process PDF, Word, and Excel documents to generate formatted reports. Use when the user says "generate a report", "process this document", "convert this PDF", or asks about document processing.
```

### Description Checklist
- [ ] Third person ("Generates..." not "Generate...")
- [ ] Includes WHAT it does
- [ ] Includes WHEN to use it
- [ ] Has "Use when..." clause with literal trigger phrases
- [ ] Under 1024 characters
- [ ] No `<` or `>` characters
- [ ] 100-200 words

## SKILL.md Body Structure

```markdown
# [Action Verb]: $ARGUMENTS

[1-2 sentence intro]

## Phase 1: [Name]
[Imperative instructions]

## Phase 2: [Name]
...

## Output Format
[Exact markdown template in fenced code block]

## Rules
[5-8 specific, actionable constraints]
```

### Key Conventions
- **Imperative voice**: "Always run tests" NOT "You might want to..."
- **Max 500 lines** in SKILL.md (overflow to references/)
- Only include instructions Claude wouldn't know from general training
- Focus on project-specific logic, conventions, and post-cutoff information

## Structural Patterns

| Pattern | When to Use |
|---------|------------|
| Phase-based workflow | Multi-step sequential process |
| Decision tree | Branching workflows |
| Checklist-driven | Quality gates/review tasks |
| Template-based | Rigid output format required |
| Feedback loop | Quality-critical tasks |
| Pipeline/chain | Skills handing off to each other |

## Progressive Disclosure

```
SKILL.md          → Always loaded when skill activates
  references/     → Loaded on-demand when referenced
    specs.md      → Background knowledge
    examples.md   → Reference implementations
  scripts/        → Executed via Bash
    validate.py   → Deterministic checks
```

## Degrees of Freedom

| Level | When | Example |
|-------|------|---------|
| High freedom | Creative tasks | "Write a compelling description" |
| Medium freedom | Preferred pattern | "Use phase-based layout; adapt as needed" |
| Low freedom | Critical/exact | "Name MUST match `^[a-z0-9-]+$`" |

## Script Best Practices

- Standard library only (no pip installs)
- Explicit error handling with descriptive messages
- JSON output for structured results
- Descriptive filenames (not `run.py`)
- Document magic numbers as named constants
- Use forward slashes in all paths

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Windows-style paths (`scripts\helper.py`) | Always use forward slashes |
| Too many options | Provide a default + escape hatch |
| Time-sensitive information | Use relative terms or fetch dynamically |
| Inconsistent terminology | Pick one term and use it everywhere |
| Deeply nested references | Keep references one level deep |
| Over-explaining basics | Only include what Claude doesn't know |
| Vague descriptions | Include literal trigger phrases |
| First/second person | Use third person in descriptions |
| Magic numbers in scripts | Use named constants |
| Loading everything into SKILL.md | Use references/ for background knowledge |

## Quality Checklist

### Name
- [ ] kebab-case, no `--`, max 64 chars
- [ ] Gerund form preferred

### Description
- [ ] Third person
- [ ] What + When
- [ ] "Use when..." with trigger phrases
- [ ] Under 1024 chars
- [ ] No angle brackets

### Body
- [ ] Under 500 lines
- [ ] Imperative voice
- [ ] Phase-based or appropriate pattern
- [ ] Output format template
- [ ] Rules section (5-8 items)
- [ ] No over-explained basics

### References
- [ ] One level deep
- [ ] Descriptive names
- [ ] ToC for files over 100 lines

### Scripts
- [ ] Standard library only
- [ ] Explicit error handling
- [ ] JSON output
- [ ] Forward slashes
