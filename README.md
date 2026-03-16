# Claude Code Skill Toolkit

> Build, validate, improve, and install Claude Code skills — from a plain-English description to a production-ready slash command.

**Claude Code skills** are custom slash commands (like `/deploy`, `/lint`, `/research`) that extend what Claude Code can do. They're markdown files with structured instructions that Claude follows when you invoke them. This toolkit automates creating those skills — so instead of writing SKILL.md files by hand, you describe what you want and get a validated, best-practice skill back.

## Why Use This

- **Skip the boilerplate** — Describe your skill in plain English, get a complete SKILL.md with frontmatter, phases, output templates, and rules
- **Research-backed quality** — Optional modes investigate your skill's domain before generating, finding best practices and pitfalls you'd miss
- **Validated by default** — Every generated skill is checked against 13+ spec rules before you see it
- **Three quality tiers** — Standard (fast), Research-First (informed), and Deep Research-First (exhaustive with adversarial review)

## Prerequisites

- [Claude Code](https://claude.ai/download) CLI installed
- Python 3.6+ (stdlib only — no pip dependencies needed)

## Quick Start

```bash
git clone https://github.com/shafir360/claude-code-skill-toolkit.git
cd claude-code-skill-toolkit
```

Skills activate automatically when Claude Code runs in this directory.

```
/generate-skill a skill that formats JSON files with configurable indentation
```

That's it. The skill is validated and saved to `output/`. Install it globally with `/implement-skill`.

## Skills

### Skill Generation & Improvement

| Command | Tier | Time | Description |
|---------|------|------|-------------|
| `/generate-skill` | Standard | ~2 min | Create a skill from a plain-English description. Reasons through intent, asks clarifying questions, generates SKILL.md + references + scripts, auto-validates. |
| `/research-generate-skill` | Research | ~8 min | Research-first generation. Spawns parallel Sonnet agents to investigate the domain, then generates informed by findings. |
| `/deep-research-generate-skill` | Deep Research | ~15 min | Two-round research with tiered models. Opus gap analysis + skeptic agent. Produces skills with per-finding confidence levels. |
| `/improve-skill` | Standard | ~3 min | Reads skill, reasons about improvements, asks priorities, then analyzes against best practices. Applies approved changes with `.bak` backup. |
| `/research-improve-skill` | Research | ~8 min | Research-first improvement. Finds best-in-class examples and domain-specific gaps before suggesting changes. |
| `/deep-research-improve-skill` | Deep Research | ~15 min | Two-round improvement with Opus skeptic that challenges improvement assumptions — defends the current approach when it's already optimal. |

### Utilities & Research

| Command | Time | Description |
|---------|------|-------------|
| `/validate-skill` | ~30s | Read-only checker. 13+ deterministic checks via Python script + qualitative assessment. |
| `/implement-skill` | ~10s | Install a generated skill from `output/` to `~/.claude/skills/`. Validates before installing. |
| `/research` | ~5 min | Multi-source research on any topic. Reasons through intent, clarifies scope, then spawns parallel Sonnet agents for synthesized cited report. |
| `/deep-research` | ~12 min | Exhaustive two-round research. Reasons through intent, clarifies scope, then broad sweep, Opus gap analysis, targeted dives + Opus skeptic. Per-finding confidence levels. |

## How It Works

```
   You describe a skill in plain English
                    |
                    v
        ┌───────────────────────┐
        │   GENERATE / RESEARCH │  Analyzes requirements, (optionally) researches
        │                       │  the domain, designs and writes SKILL.md
        └───────────┬───────────┘
                    |
                    v
          output/<skill-name>/       Saved locally with README + RESEARCH_BRIEF
                    |
                    v
        ┌───────────────────────┐
        │      VALIDATE         │  13+ automated checks (YAML, naming, description
        │                       │  quality, body length, references depth)
        └───────────┬───────────┘
                    |
                    v
        ┌───────────────────────┐
        │      IMPROVE          │  Compares against best practices, suggests
        │                       │  improvements by priority, applies with backup
        └───────────┬───────────┘
                    |
                    v
        ┌───────────────────────┐
        │     IMPLEMENT         │  Copies to ~/.claude/skills/ so it works
        │                       │  in any project on your machine
        └───────────────────────┘
```

## Standard vs Research-First vs Deep Research

| | Standard | Research-First | Deep Research-First |
|---|---------|----------------|---------------------|
| **Speed** | ~2 min | ~8 min | ~15-17 min |
| **Best for** | Familiar domains, simple skills | Unfamiliar domains, complex skills | Critical skills, maximum quality |
| **Research rounds** | None | 1 round (Sonnet only) | 2 rounds (Sonnet + Opus) |
| **Model strategy** | Inherit parent | All Sonnet agents | Tiered: Sonnet collect, Opus analyze |
| **Skeptic agent** | No | No | Yes — dedicated Opus devil's advocate |
| **Confidence levels** | No | No | Per-finding (High/Medium/Low) |
| **Contradiction analysis** | No | No | Always included |
| **Output** | SKILL.md + references | + RESEARCH_BRIEF.md | + Enhanced brief with confidence |
| **Generate** | `/generate-skill` | `/research-generate-skill` | `/deep-research-generate-skill` |
| **Improve** | `/improve-skill` | `/research-improve-skill` | `/deep-research-improve-skill` |

**Rule of thumb**: Start with Standard. Use Research-First when you're building a skill in a domain you don't know well. Use Deep Research-First when the skill is important enough to spend 15 minutes getting it right.

## Use Cases

**Build a skill from scratch:**
```
/generate-skill a skill that deploys to AWS using CDK, runs tests first, and rolls back on failure
```

**Research an unfamiliar domain first:**
```
/research-generate-skill a skill that converts OpenAPI specs to Claude Code skills
```

**Maximum quality with adversarial review:**
```
/deep-research-generate-skill a skill that manages Kubernetes deployments with canary releases
```

**Validate a community skill:**
```
/validate-skill ~/.claude/skills/some-community-skill
```

**Improve activation rate:**
```
/improve-skill ~/.claude/skills/my-skill
```

**Full pipeline — generate, polish, install:**
```
/generate-skill a skill that runs ESLint with auto-fix
/validate-skill output/run-eslint
/improve-skill output/run-eslint
/implement-skill run-eslint
```

**Deep research on any topic:**
```
/deep-research What are the security implications of WebAssembly in production?
```

## Example Output

Running `/generate-skill` produces a directory like this:

```
output/format-json/
├── SKILL.md              # Complete skill definition
├── README.md             # Documentation with usage examples
├── RESEARCH_BRIEF.md     # Domain findings (research modes only)
└── references/           # Background knowledge (if needed)
    └── json-standards.md
```

The generated SKILL.md looks like:

```yaml
---
name: format-json
description: 'Formats JSON files with configurable indentation and sorting.
  Handles nested objects, arrays, and edge cases like empty files or invalid
  JSON. Use when saying "format JSON", "pretty print JSON", "indent JSON",
  or "fix JSON formatting".'
argument-hint: "file path or glob pattern"
allowed-tools:
  - Read
  - Write
  - Glob
---

# Format JSON: $ARGUMENTS

[Phases with imperative instructions...]

## Rules
1. Always create a backup before modifying files
2. Validate JSON before and after formatting
...
```

## Skill Gallery

The [`output/`](output/) folder contains generated skills you can browse, install, or use as examples:

| Skill | Description |
|-------|-------------|
| [deep-research](output/deep-research/) | Two-round exhaustive research with tiered models and skeptic agent |
| [deep-research-generate-skill](output/deep-research-generate-skill/) | Premium skill generation backed by deep research |
| [deep-research-improve-skill](output/deep-research-improve-skill/) | Premium skill improvement with adversarial review |

Each skill includes its own README with usage examples, design decisions, and research insights. To add your own, just commit to `output/`.

## What Makes This Different

**Eval-driven** — Every generated skill is validated against the [agentskills.io](https://agentskills.io/specification) spec. The validation script checks 13+ rules including YAML format, naming, description quality, and body length.

**Activation-optimized** — Descriptions include "Use when..." trigger clauses with literal user phrases, pushing activation rates from ~20% to ~95% ([source](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1)).

**Research-backed** — Built on Anthropic's [skill-creator 2.0](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) eval pipeline, [official best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and top community collections.

**Adversarial review** — Deep research modes use a dedicated Opus skeptic agent that actively tries to disprove findings, countering the ["Chat-Chamber effect"](https://arxiv.org/html/2511.07784v1) where AI confirms assumptions rather than challenging them.

**Not bloated** — Skills stay under 500 lines. Large content goes in `references/`, scripts in `scripts/`. Progressive disclosure pattern throughout.

## Install to Other Projects

```bash
# Copy toolkit skills to a specific project
powershell -ExecutionPolicy Bypass -File install.ps1 -Target C:\path\to\project

# Install toolkit skills globally
powershell -ExecutionPolicy Bypass -File install.ps1 -Global
```

## Standalone Validation

`quick_validate.py` works without Claude Code — use it in CI or as a pre-commit check:

```bash
python .claude/skills/validate-skill/scripts/quick_validate.py path/to/any-skill
# JSON output with pass/warn/fail per check. Exit 0 = valid, 1 = failures.
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
│   ├── implement-skill/             output/ → global installer
│   ├── research/                    multi-source research tool
│   └── deep-research/              two-round exhaustive research
├── output/                      generated skills gallery
├── shared/                      source-of-truth references (dev only)
├── install.ps1                  install to other projects
└── RESEARCH_FINDINGS.md         18 sections, 34 sources
```

## Sources & Research

This toolkit's design is informed by research across 34+ sources. Key references:

- [agentskills.io Specification](https://agentskills.io/specification) — Official SKILL.md format and validation rules
- [Anthropic Skill-Creator 2.0](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) — Eval pipeline for testing and refining agent skills
- [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Official guidance on writing effective skills
- [Skill Activation Research](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1) — Why "Use when..." clauses push activation from ~20% to ~95%
- [Deep Research Agent Survey (arXiv)](https://arxiv.org/pdf/2508.12752) — Survey of autonomous research agent architectures
- [FlowSearch: Dynamic Knowledge Flow (arXiv)](https://arxiv.org/html/2510.08521v1) — Multi-round research with progressive knowledge accumulation
- [Multi-agent Debate for Factuality (arXiv)](https://arxiv.org/abs/2305.14325) — How adversarial agents improve accuracy
- [Heterogeneous Agent Debate (Springer)](https://link.springer.com/article/10.1007/s44443-025-00353-3) — ~91% vs ~82% accuracy with diverse model tiers
- [LLM Debate Limitations (arXiv)](https://arxiv.org/html/2511.07784v1) — "Minority correction asymmetry" in multi-agent systems
- [D3: Debate, Deliberate, Decide (arXiv)](https://arxiv.org/abs/2410.04663) — Role-specialized adversarial evaluation framework

Full research compilation: [RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md)

## FAQ

**Do I need to install anything beyond Claude Code?**
Just Python 3.6+ for the validation script. No pip packages needed — everything uses the standard library.

**Does this work with VS Code?**
Yes. Claude Code runs in any terminal. If you're using the Claude Code VS Code extension, these skills work there too.

**How long does generation take?**
Standard: ~2 min. Research-first: ~8 min. Deep research-first: ~15 min. The extra time goes to domain research — the actual generation step is similar across all tiers.

**Can I customize generated skills after creation?**
Absolutely. Generated skills are just markdown files. Edit them however you like, then run `/validate-skill` to make sure they still pass spec checks.

**What if I don't like the generated skill?**
Run `/improve-skill` on it. Or regenerate with a more specific description. The research-first modes produce better results for unfamiliar domains.

**Can I use this toolkit's skills in other projects?**
Yes. Use `install.ps1` to copy the toolkit skills to any project, or install them globally to `~/.claude/skills/`.

## Contributing

1. Fork the repo
2. Make changes
3. Validate modified skills with `quick_validate.py`
4. Submit a PR

## License

MIT
