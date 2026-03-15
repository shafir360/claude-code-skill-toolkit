# Claude Code Skill Specification Reference

## Directory Structure

```
skill-name/
  SKILL.md          # REQUIRED — entry point with frontmatter + instructions
  references/       # Optional — background knowledge, specs, examples
    *.md            # One level deep only (no nesting)
  scripts/          # Optional — deterministic automation
    *.py            # Executed via Bash, output enters context
  assets/           # Optional — templates, images
    *.*             # Referenced by path, never loaded automatically
```

All paths use forward slashes (even on Windows).

## Frontmatter Fields

### Base Spec Fields
| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | kebab-case `[a-z0-9-]+`, no `--`, max 64 chars, gerund form preferred |
| `description` | Yes | Max 1024 chars (hard truncation), no `<` or `>`, third person |
| `license` | No | SPDX identifier |
| `allowed-tools` | No | List of tool names; supports globs like `Bash(python *)` |
| `metadata` | No | Arbitrary key-value pairs |
| `compatibility` | No | Minimum runtime version |

### Claude Code Extended Fields
| Field | Default | Notes |
|-------|---------|-------|
| `argument-hint` | `""` | Autocomplete hint (e.g., `<topic or question>`) |
| `disable-model-invocation` | `false` | `true` = user-only invoke (no auto-trigger) |
| `user-invocable` | `true` | `false` = hidden from user, system-only |
| `model` | inherit | Override model for this skill |
| `context` | `""` | `"fork"` = isolated subagent context |
| `agent` | `""` | Custom agent configuration |
| `hooks` | `{}` | Lifecycle hooks |

## Name Validation

Pattern: `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`
- Only lowercase letters, numbers, hyphens
- No consecutive hyphens (`--`)
- No leading/trailing hyphens
- Max 64 characters
- Gerund form preferred

## Description Rules

- Max 1024 characters (hard truncation)
- No `<` or `>` characters
- Third person voice required
- Must include BOTH what + when
- Must include "Use when..." clause with literal trigger phrases
- 100-200 words ideal

## How Skills Load at Runtime

1. **Startup**: Only `name` + `description` loaded into system prompt (~15,000 char budget)
2. **Selection**: LLM reasoning matches user intent against descriptions (semantic matching)
3. **Loading**: Full SKILL.md content loaded when skill is selected
4. **Progressive disclosure**: References loaded on-demand when referenced
5. **Scripts**: Executed via Bash, stdout/stderr enters context only

## Variable Substitution

| Variable | Value |
|----------|-------|
| `$ARGUMENTS` | All arguments passed to the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by index |
| `${CLAUDE_SKILL_DIR}` | Absolute path to skill directory |
| `${CLAUDE_SESSION_ID}` | Current session ID |
