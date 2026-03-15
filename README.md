# Claude Code Skill Toolkit

Create, validate, improve, and install Claude Code skills — with optional research-first modes that investigate the domain before generating or improving. Powered by research from 34 sources including Anthropic's own eval pipeline.

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
| `/research-generate-skill` | Research-first generation. Investigates the domain with parallel Sonnet agents, then generates a skill informed by real-world findings. |
| `/validate-skill` | Read-only checker. 13+ deterministic checks via Python script, then qualitative assessment of instructions and structure. |
| `/improve-skill` | Analyze a skill against best practices. Categorizes issues by priority, presents a plan, auto-applies approved changes with `.bak` backup. |
| `/research-improve-skill` | Research-first improvement. Investigates the skill's domain for best-in-class examples and gaps, then suggests research-backed improvements. |
| `/implement-skill` | Install a generated skill from `output/` to `~/.claude/skills/`. Validates before installing. |
| `/research` | Conduct multi-source research on any topic. Spawns parallel agents, synthesizes findings, produces a cited report. |

## Workflow

```
/generate-skill "a skill that..."          standard generation
        — or —
/research-generate-skill "a skill that..."  research-first generation
        |
        v
  output/<skill-name>/          saved locally
        |
        v
/validate-skill output/<name>   13+ quality checks
        |
        v
/improve-skill output/<name>              standard improvement
        — or —
/research-improve-skill output/<name>      research-first improvement
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
│   ├── generate-skill/              5-phase skill creator
│   ├── research-generate-skill/     7-phase research-first creator
│   ├── validate-skill/              5-phase validator + quick_validate.py
│   ├── improve-skill/               6-phase skill improver
│   ├── research-improve-skill/      8-phase research-first improver
│   ├── implement-skill/             output/ to global installer
│   └── research/                    multi-source research tool
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
