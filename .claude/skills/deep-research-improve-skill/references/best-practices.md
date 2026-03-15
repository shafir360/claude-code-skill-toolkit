# Claude Code Skill Best Practices

## Description Writing

### The "Use when..." Pattern (95% activation)

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

## Structural Patterns

| Pattern | When to Use |
|---------|------------|
| Phase-based workflow | Multi-step sequential process |
| Decision tree | Branching workflows |
| Checklist-driven | Quality gates/review tasks |
| Template-based | Rigid output format required |
| Feedback loop | Quality-critical tasks |
| Pipeline/chain | Skills handing off to each other |

## Improvement-Specific Best Practices

### Categorizing Improvements
- **Critical**: Spec violations, functional issues (must fix)
- **High**: Significant quality issues (should fix)
- **Medium**: Best practice improvements (nice to fix)
- **Low**: Polish items (when time permits)

### Research-Backed Improvements
- Always tag with `[Research: Confidence H/M/L]`
- Skeptic-challenged improvements tagged with `[Skeptic: challenged]`
- Provide citation for research-backed changes
- Higher confidence = higher priority

### Preserving Skill Intent
- Read the ENTIRE skill before suggesting changes
- Improve execution, not purpose
- If the skill is high quality, say so — don't invent problems
- Create .bak backup before any modifications

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Windows-style paths | Always use forward slashes |
| Too many options | Provide a default + escape hatch |
| Over-explaining basics | Only include what Claude doesn't know |
| Vague descriptions | Include literal trigger phrases |
| First/second person | Use third person in descriptions |
| Loading everything into SKILL.md | Use references/ for background knowledge |
| Inventing problems | Only suggest changes that add genuine value |
| Ignoring skeptic findings | Present challenged improvements transparently |

## Quality Checklist

### Name
- [ ] kebab-case, no `--`, max 64 chars

### Description
- [ ] Third person, what + when, "Use when..." clause
- [ ] Under 1024 chars, no angle brackets

### Body
- [ ] Under 500 lines, imperative voice
- [ ] Phase-based or appropriate pattern
- [ ] Output format template, Rules section

### References
- [ ] One level deep, descriptive names
