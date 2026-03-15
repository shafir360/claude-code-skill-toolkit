# Claude Code Skill Generator

> Create, validate, improve, and install Claude Code skills — powered by research from 34 sources including Anthropic's own eval pipeline.

Stop writing skills by hand. This toolkit generates spec-compliant, activation-optimized Claude Code skills in seconds, then validates and improves them automatically.

## Quick Start

```bash
git clone https://github.com/shafir360/skill-generator.git
cd skill-generator
```

The 4 skills are project-level — they activate automatically when Claude Code runs in this directory.

```
/generate-skill a skill that formats JSON files with configurable indentation
```

That's it. The skill is generated, validated, and saved to `output/`. Install it globally with `/implement-skill`.

## The 4 Skills

| Command | What It Does |
|---------|-------------|
| `/generate-skill` | Create a new skill from a plain-English description. Gathers requirements, designs structure, generates SKILL.md + references + scripts, auto-validates, and saves to `output/`. |
| `/validate-skill` | Read-only quality checker. Runs 13+ deterministic checks via Python script (YAML, naming, description rules), then qualitative assessment of instructions, patterns, and structure. |
| `/improve-skill` | Analyze any existing skill against best practices. Prioritizes issues (Critical/High/Medium/Low), presents an improvement plan, and auto-applies approved changes with `.bak` backup. |
| `/implement-skill` | Browse skills in `output/` and install the selected one globally to `~/.claude/skills/`. Validates before installing. |

## Workflow

```
/generate-skill "a skill that..."
        |
        v
   output/<skill-name>/         <-- saved locally
        |
        v
/validate-skill output/<name>   <-- check quality (13+ checks)
        |
        v
/improve-skill output/<name>    <-- polish (optional)
        |
        v
/implement-skill <name>         <-- install to ~/.claude/skills/
```

## Example Usage

**Generate a skill:**
```
> /generate-skill a skill that converts CSV files to formatted markdown tables

Phase 1: Requirements gathered (purpose, triggers, tools, complexity)
Phase 2: Design chosen (simple structure, phase-based pattern)
Phase 3: SKILL.md generated at output/csv-to-markdown/
Phase 4: Validated - PASS (13/13 checks)
Phase 5: Presented with tree view, content, and test invocations
```

**Validate any skill:**
```
> /validate-skill ~/.claude/skills/my-skill

# Skill Validation Report: my-skill
| Category        | Status | Issues |
|-----------------|--------|--------|
| Spec Compliance | PASS   | 0      |
| Description     | WARN   | 1      |  <-- missing "Use when..." clause
| Instructions    | PASS   | 0      |
| Overall         | WARN   | 1      |
```

**Improve an existing skill:**
```
> /improve-skill ~/.claude/skills/my-skill

# Improvement Plan
- [HIGH] Add "Use when..." trigger clause to description (20% -> 95% activation)
- [MEDIUM] Add output format template
- [LOW] Minor wording polish

Apply changes? "apply all" / "apply critical+high" / "show diff"
```

## Install to Other Projects

```bash
# Copy skills to another project (they become project-level there)
powershell -ExecutionPolicy Bypass -File install.ps1 -Target /path/to/project

# Or install globally (available everywhere)
powershell -ExecutionPolicy Bypass -File install.ps1 -Global
```

## Project Structure

```
.
├── .claude/skills/                  # The 4 skills (project-level)
│   ├── generate-skill/
│   │   ├── SKILL.md                 # 5-phase skill creator
│   │   └── references/
│   │       ├── skill-spec.md        # Official spec reference
│   │       ├── best-practices.md    # Patterns + quality checklist
│   │       └── example-skills.md    # Annotated exemplar skills
│   ├── validate-skill/
│   │   ├── SKILL.md                 # 5-phase read-only validator
│   │   ├── references/
│   │   └── scripts/
│   │       └── quick_validate.py    # Deterministic checks -> JSON
│   ├── improve-skill/
│   │   ├── SKILL.md                 # 6-phase skill improver
│   │   └── references/
│   └── implement-skill/
│       └── SKILL.md                 # Install from output/ to global
├── output/                          # Generated skills land here
├── shared/                          # Source-of-truth references (dev only)
├── install.ps1                      # Install skills to other projects
└── RESEARCH_FINDINGS.md             # 18 sections, 34 sources
```

## What Makes This Different

**Eval-driven** — Every generated skill is validated against the official [agentskills.io](https://agentskills.io/specification) spec before being presented. The Python validation script checks 13+ rules including YAML format, name conventions, description quality, and body length.

**Activation-optimized** — Generated descriptions always include "Use when..." trigger clauses with literal user phrases. This technique was proven across [650+ trials](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1) to push activation rates from ~20% to ~95%.

**Research-backed** — Built on analysis of Anthropic's [skill-creator 2.0](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) eval pipeline, [official best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and top community skill collections (4,400+ stars combined). Full research with 34 sources in [RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md).

**Not bloated** — Skills stay under 500 lines. Large content goes in `references/` (loaded on demand). Scripts go in `scripts/` (executed, not loaded into context). Follows the progressive disclosure pattern used by all top skill creators.

## Standalone Validation Script

The `quick_validate.py` script works independently — no Claude Code required:

```bash
python .claude/skills/validate-skill/scripts/quick_validate.py path/to/any-skill

# Output: structured JSON with pass/warn/fail for each check
# Exit code: 0 = valid, 1 = has failures
```

**Checks performed:**
- Frontmatter exists and YAML parses correctly
- Name format: kebab-case, no consecutive hyphens, max 64 chars
- Description: no angle brackets, max 1024 chars, third-person voice, trigger clause
- Frontmatter keys: spec + Claude Code extended keys validated
- Body line count: warn at 400, fail at 500
- Directory structure: reference depth, clean scripts/

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Python 3.6+ (for validation script — stdlib only, no pip dependencies)

## Contributing

1. Fork the repo
2. Make your changes
3. Run `python .claude/skills/validate-skill/scripts/quick_validate.py` against any modified skills
4. Submit a PR

## License

MIT
