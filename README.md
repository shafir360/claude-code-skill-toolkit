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

For research-backed generation (slower, higher quality):

```
/research-generate-skill a skill that manages database migrations with rollback support
```

## Skills

### Skill Generation & Improvement

| Command | Tier | Description |
|---------|------|-------------|
| `/generate-skill` | Standard | Create a skill from a plain-English description. Gathers requirements, generates SKILL.md + references + scripts, auto-validates, saves to `output/`. |
| `/research-generate-skill` | Research | Research-first generation. Investigates the domain with parallel Sonnet agents, then generates a skill informed by real-world findings. |
| `/deep-research-generate-skill` | Deep Research | Exhaustive two-round research with tiered models (Sonnet for collection, Opus for analysis + skeptic). Produces skills backed by per-finding confidence levels and contradiction analysis. |
| `/improve-skill` | Standard | Analyze a skill against best practices. Categorizes issues by priority, presents a plan, auto-applies approved changes with `.bak` backup. |
| `/research-improve-skill` | Research | Research-first improvement. Investigates the skill's domain for best-in-class examples and gaps, then suggests research-backed improvements. |
| `/deep-research-improve-skill` | Deep Research | Exhaustive two-round improvement with tiered models. Dedicated Opus skeptic challenges improvement assumptions — sometimes the current approach is already optimal. |

### Utilities & Research

| Command | Description |
|---------|-------------|
| `/validate-skill` | Read-only checker. 13+ deterministic checks via Python script, then qualitative assessment of instructions and structure. |
| `/implement-skill` | Install a generated skill from `output/` to `~/.claude/skills/`. Validates before installing. |
| `/research` | Conduct multi-source research on any topic. Spawns parallel agents, synthesizes findings, produces a cited report. |
| `/deep-research` | Exhaustive two-round research with tiered models. Round 1 broad sweep, Opus gap analysis, Round 2 targeted dives + Opus skeptic. Per-finding confidence and contradiction analysis. |

## Use Cases

**Build a deployment skill from scratch:**
```
/generate-skill a skill that deploys to AWS using CDK, runs tests first, and rolls back on failure
```
Asks up to 3 clarifying questions, generates SKILL.md + references, validates, saves to `output/deploy-aws/`.

**Research-generate a skill in an unfamiliar domain:**
```
/research-generate-skill a skill that converts OpenAPI specs to Claude Code skills
```
Spawns 3-5 Sonnet agents to research OpenAPI patterns, existing converters, and common pitfalls. Produces a research brief + higher-quality skill.

**Validate a skill you found online:**
```
/validate-skill ~/.claude/skills/some-community-skill
```
Runs 13+ checks (YAML format, naming, description quality, body length) and gives a PASS/WARN/FAIL report.

**Improve your skill's activation rate:**
```
/improve-skill ~/.claude/skills/my-skill
```
Analyzes against best practices, generates 2-3 description variants with trigger keywords, applies approved changes with `.bak` backup.

**Full pipeline — generate, polish, install:**
```
/generate-skill a skill that runs ESLint with auto-fix
/validate-skill output/run-eslint
/improve-skill output/run-eslint
/implement-skill run-eslint
```

**Deep research-generate for maximum quality:**
```
/deep-research-generate-skill a skill that manages Kubernetes deployments with canary releases
```
Runs two rounds of research: Round 1 spawns 5-7 Sonnet agents for broad domain coverage, Opus analyzes gaps, Round 2 launches targeted collectors + Opus skeptic. Produces an enhanced design brief with per-finding confidence, then generates the skill.

**Deep research-improve with skeptic review:**
```
/deep-research-improve-skill .claude/skills/deploy-k8s
```
Same two-round architecture but for improvement. The Opus skeptic specifically challenges improvement assumptions — defending the current approach when it's already optimal.

**Pure deep research on any topic:**
```
/deep-research What are the security implications of WebAssembly in production?
```
Two-round investigation with per-finding confidence, contradiction analysis, and source credibility assessment.

## Standard vs Research-First vs Deep Research

| | Standard | Research-First | Deep Research-First |
|---|---------|----------------|---------------------|
| **Speed** | ~2 minutes | ~8 minutes | ~15-17 minutes |
| **When to use** | Familiar domains, simple skills | Unfamiliar domains, complex skills | Maximum quality, critical skills |
| **Research rounds** | None | 1 round (Sonnet only) | 2 rounds (Sonnet + Opus) |
| **Model strategy** | Inherit parent | All Sonnet agents | Tiered: Sonnet collect, Opus analyze |
| **Skeptic agent** | No | No | Yes (Opus devil's advocate) |
| **Confidence levels** | No | No | Per-finding (High/Medium/Low) |
| **Contradiction analysis** | No | No | Always included |
| **Output** | SKILL.md + references | + RESEARCH_BRIEF.md | + Enhanced RESEARCH_BRIEF.md with confidence |
| **Generate** | `/generate-skill` | `/research-generate-skill` | `/deep-research-generate-skill` |
| **Improve** | `/improve-skill` | `/research-improve-skill` | `/deep-research-improve-skill` |

Use **standard** for quick iterations. Use **research-first** when the domain is unfamiliar. Use **deep research-first** when building critical skills where incorrect domain understanding leads to poorly designed outputs.

## Workflow

```
/generate-skill "a skill that..."                    standard generation
        — or —
/research-generate-skill "a skill that..."            research-first generation
        — or —
/deep-research-generate-skill "a skill that..."       deep research-first generation
        |
        v
  output/<skill-name>/                    saved locally
        |
        v
/validate-skill output/<name>             13+ quality checks
        |
        v
/improve-skill output/<name>                          standard improvement
        — or —
/research-improve-skill output/<name>                  research-first improvement
        — or —
/deep-research-improve-skill output/<name>             deep research-first improvement
        |
        v
/implement-skill <name>                   install to ~/.claude/skills/
```

## What Gets Generated

Running `/generate-skill` or `/research-generate-skill` produces:

```
output/my-skill/
├── SKILL.md              # Skill definition (frontmatter + instructions)
├── RESEARCH_BRIEF.md     # Domain research findings (research-first only)
├── references/           # Background knowledge (if needed)
│   └── api-reference.md
└── scripts/              # Automation scripts (if needed)
    └── validate.py
```

Example SKILL.md frontmatter:

```yaml
---
name: my-skill
description: Does X when Y happens. Use when saying "do X", "run X", or "X this file".
argument-hint: <input description>
allowed-tools:
  - Read
  - Write
  - Bash(python *)
---
```

## Skill Gallery

The [`output/`](output/) folder is a browsable gallery of generated skills. Each skill includes its own README with usage examples, installation instructions, and design decisions.

Browse the gallery to find skills you can install directly, or use them as examples when building your own.

To add a skill you've generated to the gallery, just commit it — `output/` is tracked by git.

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
│   ├── deep-research-generate-skill/ 9-phase deep research-first creator
│   ├── validate-skill/              5-phase validator + quick_validate.py
│   ├── improve-skill/               6-phase skill improver
│   ├── research-improve-skill/      8-phase research-first improver
│   ├── deep-research-improve-skill/ 10-phase deep research-first improver
│   ├── implement-skill/             output/ to global installer
│   ├── research/                    multi-source research tool
│   └── deep-research/              two-round exhaustive research
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
