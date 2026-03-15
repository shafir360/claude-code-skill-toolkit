# Claude Code Skill Toolkit

Create, validate, improve, and install Claude Code skills — powered by research from 34 sources including Anthropic's own eval pipeline.

## Quick Start

```bash
git clone https://github.com/shafir360/claude-code-skill-toolkit.git
cd claude-code-skill-toolkit
```

Skills activate automatically when Claude Code runs in this directory.

```
/generate-skill a skill that formats JSON files with configurable indentation
```

Generated skill is validated and saved to `output/`. Install globally with `/implement-skill`.

## Skills

| Command | Description |
|---------|-------------|
| `/generate-skill` | Create a skill from a plain-English description. Gathers requirements, generates SKILL.md + references + scripts, auto-validates, saves to `output/`. |
| `/validate-skill` | Read-only checker. 13+ deterministic checks via Python script, then qualitative assessment of instructions and structure. |
| `/improve-skill` | Analyze a skill against best practices. Categorizes issues by priority, presents a plan, auto-applies approved changes with `.bak` backup. |
| `/implement-skill` | Install a generated skill from `output/` to `~/.claude/skills/`. Validates before installing. |

## Workflow

```
/generate-skill "a skill that..."
        |
        v
  output/<skill-name>/          saved locally
        |
        v
/validate-skill output/<name>   13+ quality checks
        |
        v
/improve-skill output/<name>    polish (optional)
        |
        v
/implement-skill <name>         install to ~/.claude/skills/
```

## Install to Other Projects

```powershell
# Install to a specific project
powershell -ExecutionPolicy Bypass -File install.ps1 -Target C:\path\to\project

# Install globally
powershell -ExecutionPolicy Bypass -File install.ps1 -Global
```

## Project Structure

```
.
├── .claude/skills/
│   ├── generate-skill/          5-phase skill creator
│   ├── validate-skill/          5-phase validator + quick_validate.py
│   ├── improve-skill/           6-phase skill improver
│   └── implement-skill/         output/ to global installer
├── output/                      generated skills land here
├── shared/                      source-of-truth references (dev only)
├── install.ps1                  install to other projects
└── RESEARCH_FINDINGS.md         18 sections, 34 sources
```

## What Makes This Different

**Eval-driven** — Every generated skill is validated against the [agentskills.io](https://agentskills.io/specification) spec. The validation script checks 13+ rules including YAML format, naming, description quality, and body length.

**Activation-optimized** — Descriptions include "Use when..." trigger clauses with literal user phrases, pushing activation rates from ~20% to ~95% ([source](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1)).

**Research-backed** — Built on Anthropic's [skill-creator 2.0](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) eval pipeline, [official best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and top community collections. Full research in [RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md).

**Not bloated** — Skills stay under 500 lines. Large content in `references/`, scripts in `scripts/`. Progressive disclosure pattern throughout.

## Standalone Validation

`quick_validate.py` works without Claude Code:

```bash
python .claude/skills/validate-skill/scripts/quick_validate.py path/to/any-skill
# JSON output with pass/warn/fail per check. Exit 0 = valid, 1 = failures.
```

## Requirements

- [Claude Code](https://claude.ai/download) CLI
- Python 3.6+ (stdlib only, no pip dependencies)

## Contributing

1. Fork the repo
2. Make changes
3. Validate modified skills with `quick_validate.py`
4. Submit a PR

## License

MIT
