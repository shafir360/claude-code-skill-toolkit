# Claude Code Skill Specification Reference

## Directory Structure

```
my-skill/
├── SKILL.md              # REQUIRED — entry point, contains frontmatter + instructions
├── references/           # Optional — docs loaded into context on demand via Read tool
├── scripts/              # Optional — executed via Bash tool, output enters context (code does NOT)
└── assets/               # Optional — templates/images referenced by path (never loaded)
```

- References MUST be one level deep from SKILL.md (no nesting)
- Reference files over 100 lines should include a table of contents
- All paths use forward slashes (even on Windows)

## Frontmatter Fields

### Base Spec Fields (agentskills.io)

| Field | Required | Type | Constraints |
|-------|----------|------|-------------|
| `name` | YES | string | kebab-case `[a-z0-9-]+`, no `--`, no leading/trailing `-`, max 64 chars |
| `description` | YES | string | Max 1024 chars, no `<` or `>`, non-empty |
| `license` | no | string | SPDX identifier (e.g., `Apache-2.0`) |
| `allowed-tools` | no | list | Tool names, supports globs: `Bash(python *)` |
| `metadata` | no | mapping | Arbitrary key-value pairs |
| `compatibility` | no | string | Max 500 chars |

### Claude Code Extended Fields

| Field | Type | Purpose |
|-------|------|---------|
| `argument-hint` | string | Hint shown during autocomplete (e.g., `<topic or question>`) |
| `disable-model-invocation` | boolean | `true` = only user can invoke (prevents auto-trigger) |
| `user-invocable` | boolean | `false` = hidden from `/` menu (background knowledge only) |
| `model` | string | Override model for this skill |
| `context` | string | `fork` = run in isolated subagent context |
| `agent` | string | Subagent type (`Explore`, `Plan`, `general-purpose`, or custom) |
| `hooks` | mapping | Hooks scoped to this skill's lifecycle |

## Name Validation Rules

```
Pattern: ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$
```

- Lowercase letters, digits, and hyphens only
- No consecutive hyphens (`--`)
- Cannot start or end with a hyphen
- Maximum 64 characters
- Gerund form preferred (e.g., `processing-pdfs`, `analyzing-data`)

## Description Rules

- **Max 1024 characters** (hard truncation — content past 1024 is lost)
- **Ideal length**: 100-200 words
- **No angle brackets** (`<` or `>`)
- **Third person voice** required ("Processes files..." not "I process files...")
- **Must include BOTH**:
  - **What** it does (action/capability)
  - **When** to use it (trigger conditions, keywords)
- Include explicit "Use when..." clause with literal user phrases for best activation

## YAML Validation

1. File MUST start with `---` on first line
2. YAML between first `---` and second `---` must parse via `yaml.safe_load()`
3. Only the 6 base spec keys are guaranteed valid; extended keys are Claude Code-specific

## How Skills Load at Runtime

1. **Startup**: Only `name` + `description` from ALL installed skills loaded into system prompt as `<available_skills>`. Budget: 2% of context window (~16,000 chars fallback)
2. **Selection**: Claude's native LLM reasoning matches user intent against descriptions (no regex/keyword matching — pure semantic understanding)
3. **Loading**: Claude invokes the `Skill` meta-tool → two messages injected (loading indicator + full SKILL.md body)
4. **Progressive disclosure**: Referenced files loaded ONLY when Claude uses the Read tool on them
5. **Scripts**: Executed via Bash, only stdout/stderr enters context — source code never loaded

## Variable Substitution

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SKILL_DIR}` | Absolute path to the directory containing SKILL.md |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### Shell Preprocessing

The `` !`command` `` syntax runs shell commands BEFORE the skill content reaches Claude:
```markdown
- Current branch: !`git branch --show-current`
- PR diff: !`gh pr diff`
```
Output replaces the placeholder. Claude only sees the final rendered text.

If `$ARGUMENTS` is not present anywhere in the skill content, arguments are appended as `ARGUMENTS: <value>`.
