---
name: validate-skill
description: Validate a Claude Code skill against the official spec and best practices. Runs deterministic checks (YAML, name format, description rules) via script, then performs qualitative assessment of instruction quality, structure, and patterns. Use when checking, validating, reviewing, auditing, or evaluating a skill directory.
argument-hint: <path/to/skill-directory>
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(python *)
---

# Validate Skill: $ARGUMENTS

You are performing a read-only validation of a Claude Code skill against the official spec and Anthropic best practices. Never modify any files.

## Phase 1: Deterministic Validation

Run the quick_validate.py script:

```
python "${CLAUDE_SKILL_DIR}/scripts/quick_validate.py" $ARGUMENTS
```

Capture the JSON output. The script checks: frontmatter exists, YAML parses, name format, name length, description exists, no angle brackets, description length, description voice, trigger clauses, allowed keys, body line count, directory structure.

If the script fails to run (Python not available, path issue, etc.), read the SKILL.md manually and perform equivalent checks by hand.

## Phase 2: Structural Assessment

Read the SKILL.md and assess:

1. **Line count**: PASS if under 400, WARN if 400-500, FAIL if over 500
2. **Directory structure**: Does it use references/ for large content? scripts/ for automation?
3. **Reference depth**: Are references one level deep? FAIL if nested directories inside references/
4. **File naming**: Are reference/script files descriptively named? WARN on generic names (doc1.md, helper.py)
5. **Path format**: All paths use forward slashes? WARN on backslashes

## Phase 3: Description Quality

Load [references/skill-spec.md](references/skill-spec.md) if needed for exact rules.

Assess the description field:
1. **Third person?** FAIL if first/second person ("I can...", "You can...")
2. **What + When?** Contains BOTH what it does AND when to use it? WARN if missing either
3. **Trigger keywords?** Includes specific verbs/nouns users would say? WARN if vague
4. **"Use when..." clause?** Has explicit trigger phrases? INFO if missing (highest-impact optimization)
5. **Length?** WARN if over 800 chars, FAIL if over 1024

## Phase 4: Instruction Quality

Assess the SKILL.md body:

1. **Clarity**: Are instructions imperative ("Always do X") not suggestive ("You might want to X")?
2. **Structure**: Clear phase/step pattern? Numbered sections?
3. **Output format**: Is there a defined output template showing exact markdown structure?
4. **Examples**: Are there concrete input/output examples where the task warrants them?
5. **Edge cases**: Does it handle error scenarios and edge cases?
6. **Degrees of freedom**: Are instructions appropriately specific for the task's fragility?
   - High freedom for creative tasks
   - Low freedom for critical/destructive operations

Load [references/best-practices.md](references/best-practices.md) if needed for pattern matching.

## Phase 5: Script Assessment

Only if scripts/ directory exists:

1. **Standard library only?** WARN if imports non-standard packages without documenting requirement
2. **Error handling?** WARN if bare try/except or no error handling at all
3. **Descriptive messages?** WARN if error messages are cryptic
4. **No magic constants?** WARN if unexplained numbers without comments
5. **Clean directory?** WARN if __pycache__ or .pyc files present

## Output Format

Produce this exact structure:

```markdown
# Skill Validation Report: [skill-name]
_Validated: [today's date] | Path: [path]_

## Summary
| Category | Status | Issues |
|----------|--------|--------|
| Spec Compliance | [PASS/WARN/FAIL] | [count] |
| Structure | [PASS/WARN/FAIL] | [count] |
| Description | [PASS/WARN/FAIL] | [count] |
| Instructions | [PASS/WARN/FAIL] | [count] |
| Scripts | [PASS/WARN/FAIL/N/A] | [count] |
| **Overall** | **[PASS/WARN/FAIL]** | **[total]** |

## Script Output
[Paste the JSON output from quick_validate.py or note if manual validation was used]

## Detailed Findings

### Spec Compliance
- [PASS/WARN/FAIL] [Check]: [Detail]
- ...

### Structure
- ...

### Description Quality
- ...

### Instruction Quality
- ...

### Scripts (if applicable)
- ...

## Recommendations
1. [Highest priority fix — explain what to change and why]
2. [Second priority fix]
3. ...
```

## Rules

- **Never modify any files** — this is a read-only assessment
- **FAIL** = violates official spec or will cause errors
- **WARN** = does not follow best practices but technically valid
- **PASS** = meets or exceeds best practices
- **INFO** = suggestion for optimization (not a problem)
- **Overall status** = worst individual status (any FAIL = overall FAIL)
- Be specific in recommendations — say exactly what to change, not "improve the description"
- If the skill is already high quality, say so — don't invent issues
