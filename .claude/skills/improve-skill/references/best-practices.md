# Claude Code Skill Best Practices

## 1. Description Writing

### Rules
- **Always third person**: "Processes files..." NOT "I process files..." or "You can use this to..."
- **Include BOTH what AND when**: what it does + when/why to use it
- **Include trigger keywords**: specific verbs and nouns users would say
- **Keep concise**: 100-200 words ideal; max 1024 chars (hard truncation)

### The "Use when..." Pattern (highest-impact technique)

Embed explicit trigger clauses with literal user phrases:

```yaml
# ~20% activation — what only
description: Processes documents and generates reports

# ~50% activation — what + when
description: Process PDF, Word, and Excel documents to generate formatted reports. Use when working with document files or when asked to create reports from files.

# ~95% activation — what + when + literal trigger phrases
description: Process PDF, Word, and Excel documents to generate formatted reports. Use when the user says "generate a report", "process this document", "convert this PDF", or asks about document processing.
```

**Data**: 650+ trial study confirmed activation rates scale from ~20% (basic) to ~95% (optimized with trigger phrases).

### Activation Rate Reference

| Description Quality | Activation Rate |
|---------------------|----------------|
| What only (no trigger context) | ~20% |
| What + when | ~50% |
| What + when + examples in SKILL.md | 72% → 90% |
| What + when + literal "Use when..." phrases | ~90-95% |

## 2. SKILL.md Body Structure

### Standard Layout
```markdown
# [Action Verb]: $ARGUMENTS

[1-2 sentence intro — what this skill does]

## Phase 1: [Name]
[Imperative instructions]

## Phase 2: [Name]
[Imperative instructions]

## Output Format
[Exact markdown template the skill should produce]

## Rules
[5-8 specific, actionable constraints]
```

### Key Principles
- **Imperative voice**: "Always run tests" NOT "You might want to consider running tests"
- **Max 500 lines**: overflow goes to references/
- **Phase-based workflow**: numbered phases for multi-step processes
- **Output template**: include the exact markdown structure to produce
- **Rules section**: specific constraints, not vague guidelines

## 3. Structural Patterns

### Progressive Disclosure (use for ALL skills)
```
SKILL.md body       → Core instructions (always loaded when triggered)
references/*.md     → Detailed docs (loaded only when Read is called)
scripts/*.py        → Automation (executed, output only enters context)
assets/*            → Templates (referenced by path, never loaded)
```

### When to Use Each Pattern

| Pattern | Use When |
|---------|----------|
| **Phase-based workflow** | Multi-step sequential process (most common) |
| **Decision tree** | Branching workflows ("creating vs. editing") |
| **Checklist-driven** | Quality gate / review tasks |
| **Template-based** | Rigid output format required |
| **Feedback loop** | Quality-critical tasks needing validation |
| **Pipeline/chain** | Skills that hand off to each other |

### Decision Tree Example
```markdown
## Determine approach:
**Creating new?** → Follow "Creation workflow" below
**Editing existing?** → Follow "Editing workflow" below
**Troubleshooting?** → See [troubleshooting.md](references/troubleshooting.md)
```

### Feedback Loop Example
```markdown
1. Make changes
2. Run validation: `python scripts/validate.py`
3. If validation fails: review errors, fix, re-validate
4. Only proceed when validation passes
```

## 4. Degrees of Freedom

Match instruction specificity to task fragility:

| Level | When to Use | Example |
|-------|-------------|---------|
| **High freedom** | Creative tasks, multiple valid approaches | "Analyze the code and suggest improvements" |
| **Medium freedom** | Preferred pattern exists | "Use this template and customize as needed: ..." |
| **Low freedom** | Critical/destructive operations | "Run exactly this command: `python migrate.py --verify --backup`" |

## 5. Script Best Practices

- **Standard library only** — no pip dependencies (yaml fallback to regex if PyYAML unavailable)
- **Explicit error handling** — catch specific exceptions, descriptive messages
- **JSON output** — structured results for Claude to parse
- **No magic constants** — every number has a comment explaining why
- **Descriptive file names** — `form_validation_rules.md` not `doc2.md`

## 6. Anti-Patterns

| Anti-Pattern | Why It's Bad |
|-------------|--------------|
| Windows-style paths (`scripts\helper.py`) | Fails on Unix systems |
| Offering too many options | Confusing; provide a default with escape hatch |
| Time-sensitive information | Will become wrong; use "old patterns" section |
| Inconsistent terminology | Confuses Claude; pick one term and stick to it |
| Deeply nested references | Claude may only `head -100` nested files |
| Over-explaining basics | Claude already knows what PDFs are |
| Vague descriptions | "Helps with documents" won't activate reliably |
| First/second person in descriptions | Causes discovery problems |
| Magic numbers in scripts | Claude can't determine right values either |
| Punting errors to Claude | Handle errors explicitly in scripts |
| Loading everything into SKILL.md | Wastes context window; use references/ |

## 7. Quality Checklist

### Core Quality
- [ ] Name: kebab-case, gerund form preferred, max 64 chars
- [ ] Description: third person, what + when, trigger keywords, max 1024 chars
- [ ] Description: includes "Use when..." clause with literal user phrases
- [ ] SKILL.md body: under 500 lines
- [ ] Large content split into references/ files
- [ ] References one level deep (no nesting)
- [ ] Long reference files have table of contents
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Imperative language ("Always do X" not "You might want to X")
- [ ] Concrete input/output examples
- [ ] Forward slashes in all paths

### Instructions
- [ ] Appropriate degrees of freedom for task fragility
- [ ] Decision trees for branching workflows
- [ ] Checklists for multi-step workflows
- [ ] Feedback loops for quality-critical tasks
- [ ] Edge cases with explicit handling
- [ ] Error recovery guidance

### Scripts
- [ ] Standard library only when possible
- [ ] Scripts handle errors explicitly
- [ ] All constants documented with rationale
- [ ] Descriptive names
- [ ] Clear distinction: execute vs. read as reference

### Evaluation
- [ ] Tested with real usage scenarios
- [ ] Description activation rate verified
- [ ] Tested across target models if applicable
