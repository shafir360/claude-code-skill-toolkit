---
name: implement-skill
description: Install a generated skill from the output folder to the global ~/.claude/skills/ directory. Lists available skills in output/ and installs the selected one. Use when implementing, installing, deploying, or activating a previously generated skill.
argument-hint: <skill-name>
allowed-tools:
  - Read
  - Glob
  - Bash(mkdir *)
  - Bash(cp *)
  - Bash(ls *)
  - Bash(python *)
---

# Implement Skill: $ARGUMENTS

Install a previously generated skill from the `output/` folder to the global `~/.claude/skills/` directory.

## Phase 1: List Available Skills

Search for generated skills:

```
Glob output/*/SKILL.md
```

For each skill found, read its SKILL.md frontmatter and extract the `name` and `description` fields.

If no skills are found in `output/`, inform the user: "No generated skills found in output/. Use `/generate-skill` to create one first."

Display available skills:

```markdown
## Available Skills in output/

| # | Name | Description |
|---|------|-------------|
| 1 | [name] | [description (first 100 chars)] |
| 2 | ... | ... |
```

## Phase 2: Select

**If `$ARGUMENTS` is provided** and matches a skill name in output/, use it directly.

**If `$ARGUMENTS` is not provided** or doesn't match, show the list from Phase 1 and ask the user to pick by name or number.

## Phase 3: Validate

Run the validation script on the selected skill before installing:

```
python "${CLAUDE_SKILL_DIR}/../validate-skill/scripts/quick_validate.py" output/<skill-name>
```

If validation reports any FAIL, warn the user and ask if they want to proceed anyway or fix the issues first.

If validation passes, proceed to install.

## Phase 4: Install

1. Create the target directory: `~/.claude/skills/<skill-name>/`
2. Copy all files from `output/<skill-name>/` to `~/.claude/skills/<skill-name>/`:
   - SKILL.md
   - references/ directory (if exists)
   - scripts/ directory (if exists)
   - assets/ directory (if exists)

```bash
mkdir -p ~/.claude/skills/<skill-name>
cp -r output/<skill-name>/* ~/.claude/skills/<skill-name>/
```

## Phase 5: Confirm

```markdown
## Skill Installed

**[skill-name]** has been installed to `~/.claude/skills/[skill-name]/`.

Files installed:
- [list of files copied]

Restart Claude Code to pick up the new skill, then use it with:
- `/[skill-name] [example usage based on argument-hint]`
```

## Rules

- Never install a skill that fails validation without explicit user approval
- Always show what will be installed before copying
- If the skill already exists at the target, warn the user and ask to overwrite or skip
- Do not remove the skill from output/ after installing — keep it as a local backup
