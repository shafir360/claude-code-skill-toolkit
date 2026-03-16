---
name: improve-skill
description: Analyze and improve an existing Claude Code skill against best practices. Runs validation, identifies weaknesses, suggests or auto-applies improvements to SKILL.md, description, structure, and scripts. Use when improving, optimizing, fixing, refining, upgrading, or polishing an existing skill.
argument-hint: <path/to/skill-directory>
allowed-tools:
  - Read
  - Write
  - Bash(python *)
  - Grep
  - Glob
---

# Improve Skill: $ARGUMENTS

You are analyzing an existing Claude Code skill and improving it against Anthropic's official spec and best practices.

## Phase 1: Read and Understand

### 1a: Read skill files

Read the entire skill directory:

1. Read SKILL.md (frontmatter + body)
2. List and read all files in references/ (if exists)
3. List and read all files in scripts/ (if exists)

Do NOT skip any files — you need full context before reasoning about improvements.

### 1b: Assess improvement potential

Now that you have read the skill, reason through it:

- What is this skill's core purpose and domain? How well does the current implementation serve it?
- What are the most likely quality gaps? (description, structure, instruction clarity, error handling, missing patterns)
- What implicit constraints should be preserved? (the skill's personality, its users' expectations, integration points)
- What improvements would have the highest impact relative to effort?

Present a brief summary (3-5 sentences) of the skill's current state and your initial impression to the user.

### 1c: Clarify improvement scope

Based on your assessment, ask **2-4 targeted clarifying questions** about the user's improvement priorities — which aspects matter most, whether there are constraints on what can change, whether they want conservative fixes or aggressive restructuring, or any context about how the skill is used in practice. Bias toward asking rather than assuming. Only skip questions if the improvement need is obvious and unambiguous.

**Wait for the user's response before continuing.**

## Phase 2: Validate

Run the validation script:

```
python "${CLAUDE_SKILL_DIR}/../validate-skill/scripts/quick_validate.py" $ARGUMENTS
```

Capture the JSON output. If the script is unavailable, perform manual validation against the spec.

Then perform qualitative assessment beyond what the script checks:

- **Description quality**: third person, what+when, trigger keywords, "Use when..." clause
- **Instruction quality**: imperative voice, appropriate specificity, output template
- **Structure**: line count, reference organization, progressive disclosure
- **Patterns**: are the right patterns used for this task type?

Load [references/best-practices.md](references/best-practices.md) and [references/skill-spec.md](references/skill-spec.md) for the full checklist.

## Phase 3: Identify Improvements

Compare the skill against best practices and categorize every finding:

**Critical** (must fix — spec violations or functional issues):
- Invalid name format, description over 1024 chars, forbidden keys
- Body over 500 lines without references/ split
- Missing required fields (name, description)

**High priority** (should fix — significant quality issues):
- Description not in third person
- Description missing "when to use" component or trigger keywords
- No output format defined
- Suggestive language instead of imperative ("You might want to..." → "Always...")
- No edge case or error handling

**Medium priority** (nice to fix — best practice improvements):
- Could benefit from references/ (body over 300 lines)
- Could benefit from scripts/ (has deterministic validation steps)
- Missing concrete input/output examples
- Description could include "Use when..." clause with literal phrases
- Missing argument-hint

**Low priority** (polish):
- Formatting consistency
- Section ordering
- Terminology consistency
- Minor wording improvements

## Phase 4: Present Improvement Plan

Present findings in this format:

```markdown
# Improvement Plan: [skill-name]
_Analyzed: [today's date]_

## Current Assessment
[1-2 sentence summary of the skill's current state]
Overall: [EXCELLENT / GOOD / NEEDS WORK / SIGNIFICANT ISSUES]

## Proposed Changes

### Critical
1. **[What to change]**: [Specific change and why]

### High Priority
1. **[What to change]**: [Specific change and why]

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

**For description improvements specifically**: generate 2-3 description variants with different trigger keyword strategies. Present them with an explanation of the trade-offs (length, specificity, trigger coverage).

## Phase 5: Apply Changes

When the user approves:

1. **Backup**: Copy original SKILL.md to `SKILL.md.bak` in the same directory
2. **Apply**: Make the approved changes to SKILL.md (and other files if applicable)
3. **Re-validate**: Run quick_validate.py on the modified skill
4. If validation fails, fix and re-validate until it passes
5. Present the final result

## Phase 6: Summary

```markdown
# Improvement Summary: [skill-name]

## Changes Applied
- [List of each change made]

## Before/After
| Aspect | Before | After |
|--------|--------|-------|
| Description length | [old] chars | [new] chars |
| Body line count | [old] lines | [new] lines |
| Validation status | [old] | [new] |
| Trigger clause | [present/missing] | [present/missing] |

## Validation Result
[Paste final quick_validate.py JSON output or manual validation result]

## Next Steps
[Any remaining suggestions that weren't applied, or "No further improvements needed"]
```

## Rules

- Always validate BEFORE and AFTER changes
- Always create a .bak backup before modifying any file
- Never apply changes without user approval
- Present specific, actionable improvements — not vague suggestions like "improve the description"
- When suggesting description changes, provide complete replacement text
- Preserve the skill's intent and personality — improve execution, not purpose
- If the skill is already high quality, say so — don't invent problems to fix
- Generate 2-3 description variants when improving descriptions
- Do not add unnecessary complexity — simpler is better
