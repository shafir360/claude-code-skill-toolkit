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
- Gerund form preferred (e.g., `generating-tests` over `test-generator`)

## Description Rules

- Max 1024 characters (hard truncation — anything beyond is invisible)
- No `<` or `>` characters (breaks XML parsing)
- Third person voice required ("Generates..." not "Generate...")
- Must include BOTH what the skill does AND when to use it
- Must include a "Use when..." clause with literal trigger phrases
- 100-200 words is ideal
- Keep concise — all installed skills share a ~15,000 char combined budget for descriptions

### Activation Rate by Description Quality
| Description Style | Activation Rate |
|-------------------|----------------|
| Basic (what only) | ~20% |
| What + When | ~50% |
| What + When + literal trigger phrases | ~95% |

## YAML Validation

- Must start with `---`
- Must parse via `yaml.safe_load()`
- Only 6 base spec keys guaranteed; Claude Code extended fields are additive

## How Skills Load at Runtime

1. **Startup**: Only `name` + `description` loaded into system prompt (~15,000 char budget for all skills combined)
2. **Selection**: Claude's LLM reasoning matches user intent against descriptions (semantic, not regex)
3. **Loading**: Full SKILL.md content loaded when skill is selected
4. **Progressive disclosure**: References loaded on-demand when skill instructions reference them
5. **Scripts**: Executed via Bash, stdout/stderr enters context only

## Variable Substitution

| Variable | Value |
|----------|-------|
| `$ARGUMENTS` | All arguments passed to the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by index |
| `${CLAUDE_SKILL_DIR}` | Absolute path to skill directory |
| `${CLAUDE_SESSION_ID}` | Current session ID |

Shell preprocessing: `` !`command` `` runs before Claude sees content.
